# file: member_agent.py
#

# import modules
#
import time
from math import floor, log
from copy import copy
from osbrain import run_agent
from osbrain import run_nameserver
from tgdhstruct.tgdh_struct import TgdhStruct

# class: MemberAgent
#
class MemberAgent():

    # constructor
    #
    def __init__(self, size):
        
        # define class data
        #
        self.size = size
        self.agents = []
        self.addr = []
        nodemax = (2*self.size)-1
        self.max_height = floor(log((nodemax-1),2))
        self.level = 0
        self.sponsor = None
        self.new_memb = None
        self.spon_id = None
        self.new_id = None

        # system deployment
        #
        self.ns = run_nameserver()

        # initialize the tree
        #
        self.initial_key_exchange()
    #
    # end constructor

    # method: send_keys
    #
    def send_info(self, agent, channel, data_message):
        agent.send(channel, data_message)
    #
    # end method: send_keys

    # method: receive_bkeys
    #
    def receive_bkeys(self, agent, message):

        agent.log_info(f"Received: {message}")
        data = message.split(':')
        node = agent.data.btree.find_node(data[0].lstrip('<').rstrip('>'), False)
        node.b_key = int(data[1])
    #
    # end method: receive_bkeys

    # method: receive_tree
    #
    def receive_tree(self, agent, tree):

        agent.log_info("Tree received!")
        agent.data = tree
    #
    # end method: receive_tree

    # method: update_size
    #
    def update_size(self):

        # update the size attributes
        #
        self.size = self.size+1
        nodemax = (2*self.size)-1
        self.max_height = floor(log((nodemax-1),2))
    #
    # end method: update_size

    # method: close_connections
    #
    def close_connections(self):

        for agent in self.agents:
            agent.close_all()
    #
    # end method: close_connections

    # method: initial_key_exchange
    #
    def initial_key_exchange(self):

        print(f"\n{'Key Exchange (Init)'.center(80, '=')}")

        # initialize all agents with their trees and co-paths
        #
        key_paths = []
        co_paths = []
        iters = [0]*self.size
        for i in range(self.size):
            mem = f'mem_{i+1}'
            self.agents.append(run_agent(mem))
            self.agents[i].data = TgdhStruct(self.size, i+1)
            temp_key_path = []
            for node in self.agents[i].data.btree.my_node.get_key_path():
                temp_key_path.append(node.name)
            key_paths.append(temp_key_path)
            temp_co_path = []
            for node in self.agents[i].data.btree.my_node.get_co_path():
                temp_co_path.append(node.name)
            co_paths.append(temp_co_path)

        # pad the co-path lists to account for co-paths of varying lengths
        #
        for i in range(self.size):
            if len(co_paths[i]) < self.max_height:
                co_padding = [None]*(self.max_height-len(co_paths[i]))
                key_padding = [None]*(self.max_height-len(key_paths[i])+1)
                co_paths[i] = co_padding + co_paths[i]
                key_paths[i] = key_padding + key_paths[i]

        # perform the send-receive communication protocol
        #
        while self.level < self.max_height:    

            # establish publishers (each node will publish)
            #
            self.addr = []
            for i in range(self.size):
                mem = f'mem_{i+1}'
                self.addr.append(self.agents[i].bind('PUB', alias=mem))

            # establish subscribers (proper co-path member)
            #
            for i in range(self.size):
                dest_name = co_paths[i][self.level]
                if dest_name is not None:
                    dest_node = self.agents[i].data.btree.find_node(dest_name.lstrip('<').rstrip('>'), False)
                    dest_mem = dest_node.leaves[0].mid
                    self.agents[i].connect(self.addr[dest_mem-1], handler=self.receive_bkeys)

            # send blind keys for the proper node
            #
            print('')
            for i in range(self.size):
                mem = f'mem_{i+1}'
                key_node = key_paths[i][self.level]
                if key_node is not None:
                    blind_key = self.agents[i].data.btree.find_node(key_node.lstrip('<').rstrip('>'), False).b_key
                    message = f'{key_node}:{blind_key}'
                    self.send_info(self.agents[i], mem, message)

            # calculate appropriate blind keys
            #
            time.sleep(1)
            for i in range(self.size):
                if co_paths[i][self.level] is not None:
                    newtree = self.agents[i].data
                    newtree.btree.initial_calculate_group_key(iters[i])
                    iters[i] = iters[i]+1
                    self.agents[i].data = newtree
                    self.agents[i].data.btree.tree_print()

            # close connections to prevent unnecessary sending/receiving
            #
            self.close_connections()

            time.sleep(1)
            print(f"\nLevel {self.max_height-self.level} finished!")
            self.level = self.level+1

        print("\nTree initialization completed!\nAll initial members have computed the group key.")
    #
    # end method: initial_key_exchange

    # method: join_key_exchange
    #
    def join_key_exchange(self):

        print(f"\n{'Key Exchange (Join)'.center(80, '=')}")

        # start at level 1 of the tree
        #
        self.level = 1

        # get the update paths of all members
        #
        update_paths = []
        for i in range(self.size):
            if i not in (self.spon_id-1, self.new_id-1):
                temp_update_path = []
                for node in self.agents[i].data.btree.get_update_path():
                    temp_update_path.append(node.name)
                update_paths.append(list(reversed(temp_update_path)))
            else:
                update_paths.append(None)

        # get the sponsor's key path
        #
        spon_key_path = []
        for node in self.sponsor.data.btree.my_node.get_key_path():
            spon_key_path.append(node.name)
        
        while self.level < self.max_height:    

            # only the sponsor will publish
            #
            mem = f'mem_{self.spon_id}'
            self.addr[self.spon_id-1] = self.sponsor.bind('PUB', alias=mem)

            # establish subscribers (sponsor will publish)
            #
            key_node = spon_key_path[self.level]
            for i in range(self.size):
                if update_paths[i] is not None:
                    if key_node in update_paths[i]:
                        dest_name = key_node
                        if dest_name is not None:
                            self.agents[i].connect(self.addr[self.spon_id-1], handler=self.receive_bkeys)

            # sponsor sends appropriate blind keys
            #
            blind_key = self.sponsor.data.btree.find_node(key_node.lstrip('<').rstrip('>'), False).b_key
            message = f'{key_node}:{blind_key}'
            print('')
            self.send_info(self.sponsor, mem, message)

            # close connections to prevent unnecessary sending/receiving
            #
            self.close_connections()

            time.sleep(1)
            print(f"\nLevel {self.max_height-self.level} finished!")
            self.level = self.level+1
        #
        # end method: join_key_exchange

    # method: join_protocol
    #
    def join_protocol(self):

        print(f"\n{'Join Event'.center(80, '=')}")

        # alert current members that a new member is joining; find the sponsor
        #
        for i in range(self.size):
            newtree = self.agents[i].data
            newtree.btree.join_event()
            self.agents[i].data = newtree
            if self.agents[i].data.btree.my_node.ntype == 'spon':
                self.sponsor = self.agents[i]

        # update the size of the tree
        #
        self.update_size()

        # initialize the joining member
        #
        mem = f'mem_{self.sponsor.data.btree.nextmemb-1}'
        self.agents.append(run_agent(mem))
        self.agents[-1].data = None
        self.new_memb = self.agents[-1]

        # joining member subscribes to the sponsor
        #
        mem = f'mem_{self.sponsor.data.btree.uid}'
        self.addr.insert(self.sponsor.data.btree.uid-1, self.sponsor.bind('PUB', alias=mem))
        dest_mem = self.sponsor.data.btree.uid
        self.new_memb.connect(self.addr[dest_mem-1], handler=self.receive_tree)

        # sponsor sends the tree to the joining member
        #
        self.spon_id = self.sponsor.data.btree.uid
        stree = copy(self.sponsor.data)
        stree.btree.my_node.key = None
        print(f"\nMember {self.sponsor.data.btree.uid} is sending the tree ...\n")
        self.send_info(self.sponsor, mem, stree)

        # allow new member to update its tree
        #
        time.sleep(1)
        newtree = self.new_memb.data
        newtree.btree.new_member_protocol()
        self.new_memb.data = newtree
        self.new_id = self.new_memb.data.btree.uid

        # close connections
        #
        self.close_connections()

        # new member shares blind key with sponsor
        #
        mem = f'mem_{self.new_memb.data.btree.uid}'
        self.addr[-1] = self.new_memb.bind('PUB', alias=mem)
        self.sponsor.connect(self.addr[-1], handler=self.receive_bkeys)
        blind_key = self.new_memb.data.btree.my_node.b_key
        message = f'{self.new_memb.data.btree.my_node.name}:{blind_key}'
        print('')
        self.send_info(self.new_memb, mem, message)

        # allow the sponsor and new member to calculate the group key
        #
        time.sleep(1)
        newtree_s = self.sponsor.data
        newtree_s.btree.calculate_group_key()
        self.sponsor.data = newtree_s
        self.sponsor.data.btree.tree_print()
        newtree_n = self.new_memb.data
        newtree_n.btree.calculate_group_key()
        self.new_memb.data = newtree_n
        self.new_memb.data.btree.tree_print()

        # sponsor sends updated blind keys
        #
        self.join_key_exchange()

        # allow all remaining members to calculate the group key
        #
        time.sleep(1)
        for i in range(self.size):
            if i not in (self.spon_id-1, self.new_id-1):
                newtree = self.agents[i].data
                newtree.btree.calculate_group_key()
                self.agents[i].data = newtree
                self.agents[i].data.btree.tree_print()
    #
    # end method: join_protocol

    # method: close
    #
    def close(self):

        # shutdown the system
        #
        print(f"\n{'Exiting Program'.center(80, '=')}\n")
        self.ns.shutdown()
    #
    # end method: close
#
# end class: MemberAgent
#
# end file: member_agent.py