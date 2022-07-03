# file: binary_tree.py
#
'''This file contains the BinaryTree class.'''

# import modules
#
import sys
import gc
from typing import Optional
import math
import itertools
from anytree.exporter import DotExporter
from anytree import RenderTree
from anytree import search
from anytree import PreOrderIter
from tgdhstruct.data_node import DataNode

# class: BinaryTree
#
class BinaryTree:
    '''
    Description
    -----------
    This class manages the binary tree data structure used to faciliate the TGDH scheme.

    Attributes
    ----------
    size : int
        The number of members in the initial group
    uid : int
        The unique member ID for my node
    my_node : DataNode
        My node in the tree
    nodetrack : int
        The number of nodes that have been generated at initialization
    nodemax : int
        The maximum number of nodes in the initial tree with <size> members
    nextmemb : int
        The member ID of the next member to join the tree
    height : int
        The height of the initial tree
    root : DataNode
        The root of the tree
    refresh_path :
        The path of the keys that need to be updated after a join or leave event

    Methods
    ----------
    add_nodes(self, curr_n: DataNode) -> None
        This method adds two children nodes to a specified parent node.
    get_leaves(self) -> tuple[DataNode]
        This method returns all of the leaves in the tree.
    walk_tree_build(self, curr_n: DataNode) -> None
        This method is called recursively to build the tree.
    walk_pre_order(self, root: DataNode) -> PreOrderIter
        This method returns the pre-order traversal of the tree.
    type_assign(self) -> None
        This method assigns the 'ntype' attribute for the nodes in the tree.
    id_assign(self) -> None
        This method assigns the 'mid' attribute for the nodes in the initial tree.
    find_me(self) -> None:
        This function finds the node in the tree that corresponds to this user.
    key_generation(self) -> None
        This method generates keys only for my node.
    get_key(self, name: str) -> int
        This method retrieves a key that has been sent.
    send_key(self, node: DataNode) -> None
        This method sends a blind key to the rest of the group
    initial_calculate_send_group_key(self) -> None
        This method calculates the group key; it sends blind keys along the way.
    sponsor_calculate_send_group_key(self) -> None
        This method calculates the group key; the sponsor sends updated blind keys.
    calculate_group_key(self) -> None
        This method calculates the group key.
    build_tree(self) -> None
        This method builds the initial tree from the constructor.
    find_node(self, iden: int, memflag: bool) -> DataNode
        This method finds a specific node in the tree.
    recalculate_names(self) -> None
        This method recalculates the names (position indices) for each node.
    find_insertion(self) -> DataNode
        This method finds the point of insertion for a joining node.
    sponsor_communication_protocol(self, node: Optional[DataNode], join: bool) -> None
        This method initiates sponsor protocol for the sponsor node.
    grab_updated_keys(self) -> None
        This method determines which keys need to be updated and receives them.
    empty_check(self) -> None
        This method determines if I am the only member left in the group and exits if so.
    tree_refresh(self, event: str) -> None
        This method refreshes tree attributes and keys after an event.
    join_event(self) -> None
        This method updates the tree when a new member joins the group.
    leave_event(self, eid: str) -> None
        This method updates the tree when a member leaves the tree
    new_member_protocol(self) -> None
        This method is used by the new member when joining the group.
    tree_export(self) -> None
        This method exports the tree as a png file using Graphviz.
    tree_print(self) -> None
        This method prints the tree to the terminal.
     verbose_node_print(self) -> None
        This method prints all attributes of all nodes in the tree.
    '''

    # constructor
    #
    def __init__(self, size: int, uid: int) -> None:
        '''This is the constructor.'''

        self.size = size
        self.uid = uid
        self.my_node = None
        self.nodetrack = 1
        self.nodemax = (2*size)-1
        self.nextmemb = size+1
        self.height = math.floor(math.log((self.nodemax-1),2))
        self.root = DataNode()
        self.refresh_path = None

        # build the initial tree
        #
        self.build_tree()
    #
    # end constructor

    # method: add_nodes
    #
    def add_nodes(self, curr_n: DataNode) -> None:
        '''This method adds two children nodes to a specified parent node.'''

        curr_n.lchild = DataNode(
            pos='left', l=curr_n.l+1, v=2*curr_n.v, parent=curr_n, ntype='inter')
        curr_n.rchild = DataNode(
            pos='right', l=curr_n.l+1, v=(2*curr_n.v)+1, parent=curr_n, ntype='inter')
    #
    # end method: add_nodes

    # method: get_leaves
    #
    def get_leaves(self) -> tuple[DataNode]:
        '''This method returns all of the leaves in the tree.'''

        return self.root.leaves
    #
    # end method: get_leaves

    # method: walk_tree_build
    #
    def walk_tree_build(self, curr_n: DataNode) -> None:
        '''This method is called recursively to build the tree.'''

        if not curr_n.is_leaf:
            self.walk_tree_build(curr_n.rchild)
            if self.nodetrack is not self.nodemax:
                self.walk_tree_build(curr_n.lchild)
        else:
            self.add_nodes(curr_n)
            self.nodetrack = self.nodetrack + 2
    #
    # end method: walk_tree_build

    # method: walk_pre_order
    #
    def walk_pre_order(self, root: DataNode) -> PreOrderIter:
        '''This method returns the pre-order traversal of the tree.'''

        return PreOrderIter(root)
    #
    # end method: WalkPreOrer

    # method: type_assign
    #
    def type_assign(self) -> None:
        '''This method assigns the 'ntype' attribute for the nodes in the tree.'''

        for node in self.get_leaves():
            node.ntype = 'mem'
    #
    # end method: type_assign

    # method: id_assign
    #
    def id_assign(self) -> None:
        '''This method assigns the 'mid' attribute for the nodes in the initial tree.'''

        # generate member ID lists
        #
        baselist = [1,2]
        if self.height >= 1:
            for i in range(0, self.height-1):
                templist = list(reversed(range(pow(2,i+2)+1)))
                newlist = templist[0:pow(2,i+1)]
                baselist = list(itertools.chain(*zip(baselist, newlist)))
        max_size = pow(2,self.height)
        hlist = list(reversed(range(max_size+1)))
        rm_nodes = hlist[0:max_size-self.size]
        for num in rm_nodes:
            baselist.remove(num)

        # assign the ID numbers
        #
        idlist = list(reversed(baselist))
        count = len(baselist)-1
        for node in self.get_leaves():
            node.mid = idlist[count]
            count = count-1
    #
    # end method: id_assign

    # method: find_me
    #
    def find_me(self) -> None:
        '''This function finds the node in the tree that corresponds to this user.'''

        # function: me_finder
        #
        def me_finder(node: DataNode) -> DataNode:
            '''This helper function is utilized to search the tree for my node.'''

            if node.mid == self.uid:
                return node
        #
        # end function: me_finder

        # find the node that matches this members's unique ID
        #
        self.my_node = search.find(self.root, me_finder)
    #
    # end method: find_me

    # method: key_generation
    #
    def key_generation(self) -> None:
        '''This method generates keys only for my node.'''

        print("\nGenerating New Keys ...")
        self.my_node.gen_private_key()
        self.my_node.gen_blind_key()
        print("New keys generated!")
    #
    # end method: key_generation

    # method: get_key
    #
    def get_key(self, name: str) -> int:
        '''This method retrieves a key that has been sent.'''

        print(f"\nReceiving blind key for node {name}...")
        while True:
            try:
                key = int(input("Enter blind key here: "))
                break
            except ValueError:
                print("**> Error: Invalid input! (int expected)")
        print(f"Key received: {str(key)} for node {name}")
        return key
    #
    # end method: get_key

    # method: send_key
    #
    def send_key(self, node: DataNode) -> None:
        '''This method sends a blind key to the rest of the group'''

        print(f"\nSending blind key for node {node.b_key} ...")
        print(f"\tBlind key: {node.name}")
    #
    # end method: send_key

    # method: initial_calculate_send_group_key
    #
    def initial_calculate_send_group_key(self) -> None:
        '''This method calculates the group key; it sends blind keys along the way.'''

        print("\nCalculating the group key ...")
        key_path = self.my_node.get_key_path()
        co_path = self.my_node.get_co_path()
        self.send_key(self.my_node)
        for i, node in enumerate(co_path):
            node.b_key = self.get_key(node.name)
            key_path[i+1].key = pow(int(node.b_key), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].gen_blind_key()
                self.send_key(key_path[i+1])
        print(f"New group key computed: {self.root.key}")
    #
    # end method: initial_calculate_send_group_key

    # method: sponsor_calculate_send_group_key
    #
    def sponsor_calculate_send_group_key(self) -> None:
        '''This method calculates the group key; the sponsor sends updated blind keys.'''

        print("\nCalculating the group key ...")
        key_path = self.my_node.get_key_path()
        co_path = self.my_node.get_co_path()
        self.send_key(self.my_node)
        for i, node in enumerate(co_path):
            key_path[i+1].key = pow(int(node.b_key), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].gen_blind_key()
                self.send_key(key_path[i+1])
        print(f"New group key computed: {self.root.key}")
    #
    # end method: sponsor_calculate_send_group_key

    # method: calculate_group_key
    #
    def calculate_group_key(self) -> None:
        '''This method calculates the group key.'''

        print("\nCalculating the group key ...")
        key_path = self.my_node.get_key_path()
        co_path = self.my_node.get_co_path()
        for i, node in enumerate(co_path):
            key_path[i+1].key = pow(int(node.b_key), key_path[i].key, DataNode.p)
            if key_path[i+1].ntype != 'root':
                key_path[i+1].gen_blind_key()
        print(f"New group key computed: {self.root.key}")
    #
    # end method: calculate_group_key

    # method: build_tree
    #
    def build_tree(self) -> None:
        '''This method builds the initial tree from the constructor.'''

        # recursively build the tree
        #
        print(f"\nGenerating Tree with {str(self.size).rjust(2)} members ...")
        print(f"I am member {str(self.uid).rjust(2)}")
        while self.nodetrack is not self.nodemax:
            self.walk_tree_build(self.root)

        # set node attributes
        #
        self.type_assign()
        self.id_assign()
        self.find_me()

        # generate keys and calculate the group key
        #
        self.key_generation()
        self.initial_calculate_send_group_key()

        # view the tree
        #
        self.tree_export()
        self.tree_print()
    #
    # end method: build_tree

    # method: find_node
    #
    def find_node(self, iden: int, memflag: bool) -> DataNode:
        '''This method finds a specific node in the tree.'''

        # function: mem_finder
        #
        def mem_finder(node: DataNode) -> DataNode:
            '''This helper function is utilized to search the tree by member ID.'''

            if node.mid == iden:
                return node
        #
        # end function: mem_finder

        # function: node_funder
        #
        def node_finder(node: DataNode) -> DataNode:
            '''This helper function is utilized to search the tree by position index.'''

            if f'{str(node.l)},{str(node.v)}' == iden:
                return node
        #
        # end function: node_finder

        # find a specific node by member number or index
        #
        if memflag:
            return search.find(self.root, mem_finder)
        else:
            return search.find(self.root, node_finder)
    #
    # end method: find_node

    # method: recalculate_names
    #
    def recalculate_names(self) -> None:
        '''This method recalculates the names (position indices) for each node.'''

        for node in self.walk_pre_order(self.root):
            node.name = node.calculate_name()
    #
    # end method: recalculate_names

    # method: find_insertion
    #
    def find_insertion(self) -> DataNode:
        '''This method finds the point of insertion for a joining node.'''

        # find the shallowest level
        #
        llist = []
        plist = []
        for node in self.get_leaves():
            llist.append(node.l)
            plist.append(node)
        slevel = min(llist)

        # find the rightmost node on the shallowest level with no children
        #
        slist = [node for node in plist if node.l == slevel]
        olist = [node for node in slist if node.is_leaf]
        return olist[len(olist)-1]
    #
    # end method: find_insertion

    # method: sponsor_communication_protocol
    #
    def sponsor_communication_protocol(self, node: Optional[DataNode], join: bool) -> None:
        '''This method initiates sponsor protocol for the sponsor node.'''

        if join:
            # if this is a join, send the serialized tree and get the blind key from the new member
            #
            print("\nSerializing and sending tree ...")
            node.b_key = self.get_key(node.name)
            self.sponsor_calculate_send_group_key()
            self.calculate_group_key()
        else:
            # otherwise, just calculate and send (sponsor calculates new private key)
            #
            self.key_generation()
            self.sponsor_calculate_send_group_key()
    #
    # end method: sponsor_communication_protocol

    # method: grab_updated_keys
    #
    def grab_updated_keys(self) -> None:
        '''This method determines which keys need to be updated and receives them.'''

        new_path = set(self.refresh_path)
        our_path = set(self.my_node.get_co_path())
        update_path = our_path.intersection(new_path)
        for node in update_path:
            node.b_key = self.get_key(node.name)
    #
    # end method: grab_updated_keys

    # method: empty_check
    #
    def empty_check(self) -> None:
        '''This method determines if I am the only member left in the group and exits if so.'''

        if self.root.lchild.is_leaf and self.root.rchild.is_leaf:
            print("\nThis group is empty! Program will terminate.")
            sys.exit(0)
    #
    # end method: empty_check

    # method: tree_refresh
    #
    def tree_refresh(self, event: str) -> None:
        '''This method refreshes tree attributes and keys after an event.'''

        self.find_me()
        self.recalculate_names()
        self.tree_export()
        if self.my_node.ntype != 'spon':
            self.grab_updated_keys()
            self.calculate_group_key()
        else:
            print("\nI am the sponsor!")
            print("Entering sponsor protocol ...")
            if event == 'j':
                self.sponsor_communication_protocol(self.my_node.get_sibling(), True)
            else:
                self.sponsor_communication_protocol(None, False)
        self.tree_print()
    #
    # end method: tree_refresh

    # method: join_event
    #
    def join_event(self) -> None:
        '''This method updates the tree when a new member joins the group.'''

        # signal that a member is joining
        #
        print("\nNew member is joining the group!")

        # prepare the tree by assigning types
        #
        self.type_assign()

        # create two new nodes at the insertion node
        #
        inserti_node = self.find_insertion()
        self.add_nodes(inserti_node)
        sponsor_node = inserti_node.lchild
        newmemb_node = inserti_node.rchild
        self.refresh_path = newmemb_node.get_key_path()

        # transfer data to the sponsor node (the insertion node data is transferred to sponsor node)
        #
        sponsor_node.sponsor_assign(
            mid=inserti_node.mid, key=inserti_node.key,
            b_key=inserti_node.b_key, join=True)

        # assign attributes for new intermediate node and new member node
        #
        inserti_node.insertion_assign()
        newmemb_node.new_memb_assign(self.nextmemb)

        # signal that a new member has been added
        #
        self.nextmemb = self.nextmemb+1

        # refresh the tree
        #
        self.tree_refresh('j')
    #
    # end method: join_event

    # method: leave_event
    #
    def leave_event(self, eid: str) -> None:
        '''This method updates the tree when a member leaves the tree'''

        # signal that a member is leaving
        #
        print(f"\nMember {str(eid)} is leaving the group!")

        # determine if the tree is empty
        #
        self.empty_check()

        # prepare the tree by assigning types
        #
        self.type_assign()

        # find the member to be erased
        #
        for node in self.get_leaves():
            if node.mid == eid:
                if node.parent.ntype == 'root':
                    # if the parent of the leaving node is the root, the root must be relocated
                    #
                    new_root = node.get_sibling()
                    new_root.make_root()
                    self.root = new_root
                    sponsor_node = list(self.walk_pre_order(self.root))[-1]
                    sponsor_node.sponsor_assign(join=False)
                    del node
                    gc.collect()

                else:
                    # assign the sponsor and transfer data
                    #
                    sponsor_node = list(self.walk_pre_order(node.get_sibling()))[-1]
                    sponsor_node.sponsor_assign(join=False)
                    node.parent.transfer_data_remove(node.get_sibling())
                    del node
                    gc.collect()

        # determine the keys that need to be refreshed
        #
        self.refresh_path = self.find_node(sponsor_node.mid, True).get_key_path()

        # refresh the tree
        #
        self.tree_refresh('l')
    #
    # end method: leave_event

    # method: new_member_protocol
    #
    def new_member_protocol(self) -> None:
        '''This method is used by the new member when joining the group.'''

        # determine unique member ID and find me in the tree
        #
        self.uid = self.nextmemb-1
        self.find_me()

        # generate keys and send blind key
        #
        self.key_generation()
        self.send_key(self.my_node)

        # get the blind key from the sponsor
        #
        self.my_node.get_sibling().b_key = self.get_key(self.my_node.get_sibling().name)

        # calculate the group key
        #
        self.calculate_group_key()
    #
    # end method: new_member_protocol

    # method: tree_export
    #
    def tree_export(self) -> None:
        '''This method exports the tree as a png file using Graphviz.'''

        # function: nodeattrfunc
        #
        def nodeattrfunc(node: DataNode) -> DataNode:
            '''This helper function is utilized to print node attributes.'''

            if node is self.my_node:
                return f'label="{node.name}\n{node.ntype}: {node.mid} (me)"'
            elif node.mid is not None:
                return f'label="{node.name}\n{node.ntype}: {node.mid}"'
            else:
                return f'label="{node.name}\n{node.ntype}"'
        #
        # end function: nodeattrfunc

        # use graphics module to export the tree
        #
        DotExporter(self.root, nodeattrfunc=nodeattrfunc).to_picture("tree_export.png")
    #
    # end method: tree_export

    # method: tree_print
    #
    def tree_print(self) -> None:
        '''This method prints the tree to the terminal.'''

        print("\nDisplaying the tree and key information ...")
        for pre, _, node in RenderTree(self.root):
            treestr = f'{pre}{node.name}'
            datastr = f'type: {node.ntype}, ID: {node.mid}, key: {node.key}, b_key: {node.b_key}'
            print(treestr.ljust(8), datastr)
    #
    # end method: tree_print

    # method: verbose_node_print
    #
    def verbose_node_print(self) -> None:
        '''This method prints all attributes of all nodes in the tree.'''

        for node in self.walk_pre_order(self.root):
            node.print_attributes()
    #
    # end method: verbose_node_print
#
# end class: BinaryTree
#
# end file: BinaryTree.py
