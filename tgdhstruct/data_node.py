# file: DataNode.py
#
'''This file contains the DataNode class.'''

# import modules
#
from __future__ import annotations
import gc
from typing import Optional
from anytree import NodeMixin
from Crypto.Random.random import randint

# class: DataNode
#
class DataNode(NodeMixin):
    '''
    Description
    -----------
    This is the node class for use in the binary tree structure.

    Global Data
    -----------
    int: g
        The generator for Diffie-Hellman algorithm
    int: p
        The modulus for Diffie-Hellman algorithm

    Attributes
    ----------
    pos : str
        The position of the node relative to parent (left or right child)
    l : int
        The level index of the node
    v : int
        The position index of the node
    parent: DataNode
        The parent of the node
    ntype : str
        The type of the node: root, inter, mem, spon
    mid : int
        The member ID of the node
    rchild : DataNode
        The left child of the node
    lchild : DataNode
        The right child of the node
    name : str
        The level and position index of the node <l,v>
    key: int
        The private key of the node
    b_key: int
        The blind (public) key of the node

    Methods
    -------
    get_sibling(self) -> DataNode
        This method returns the sibling of any node in the binary tree.
     calculate_name(self) -> None
        This method determines the name of a node based on the name of its parent.
    gen_private_key(self) -> None
        This method generates a random private key.
    gen_blind_key(self) -> None
        This method generates the blind key.
    get_key_path(self) -> list[DataNode]
        This method gets the path from the current node up to the root.
     get_co_path(self) -> list[DataNode]
        This method gets the co-path from the current node up to the root.
    sponsor_assign(self, mid: Optional[int]=None, key: Optional[int]=None, b_key: Optional[int]=None, join: bool=True) -> None
        This method tags a node as the sponsor node.
    insertion_assign(self) -> None
        This method tags a node as the insertion node.
    new_memb_assign(self, mid: int) -> None
        This method tags a node as the new member node.
    transfer_data_remove(self, node: DataNode) -> None
        This method transfers data from a specified node and then removes that node.
    make_root(self) -> None
        This method makes the current node the root.
    print_attributes(self) -> None
        This method prints all node attributes.
    '''

    # define global Diffie-Hellman Data
    #
    g = 5
    p = 23

    # constructor
    #
    def __init__(self, pos: str='NA', l: int=0, v: int=0, parent: Optional[DataNode]=None, ntype: str='root', mid: Optional[int]=None, rchild: Optional[DataNode]=None, lchild: Optional[DataNode]=None) -> None:
        '''This is the constructor.'''

        # tree data
        #
        self.pos = pos
        self.l = l
        self.v = v
        self.parent = parent
        self.ntype = ntype
        self.mid = mid
        self.rchild = rchild
        self.lchild = lchild
        self.name = self.calculate_name()

        # Diffie-Hellman encryption data
        #
        self.key = None
        self.b_key = None
    #
    # end constructor

    # method: get_sibling
    #
    def get_sibling(self) -> DataNode:
        '''This method returns the sibling of any node in the binary tree.'''

        return self.siblings[0]
    #
    # end method: get_sibling

    # method: calculate_name
    #
    def calculate_name(self) -> None:
        '''This method determines the name of a node based on the name of its parent.'''

        if self.pos == 'left':
            self.l = self.parent.l+1
            self.v = 2*self.parent.v
            return '<' + str(self.l) + ',' + str(self.v) + '>'
        elif self.pos == 'right':
            self.l = self.parent.l+1
            self.v = 2*self.parent.v+1
            return '<' + str(self.l) + ',' + str(self.v) + '>'
        else:
            return '<' + str(self.l) + ',' + str(self.v) + '>'
    #
    # end method: calculate_name

    # method: gen_private_key
    #
    def gen_private_key(self) -> None:
        '''This method generates a random private key.'''

        self.key = randint(1, int(DataNode.p-1))
    #
    # end method: gen_private_key

    # method: gen_blind_key
    #
    def gen_blind_key(self) -> None:
        '''This method generates the blind key.'''

        self.b_key = pow(DataNode.g, self.key, DataNode.p)
    #
    # end method: gen_blind_key

    # method: get_key_path
    #
    def get_key_path(self) -> list[DataNode]:
        '''This method gets the path from the current node up to the root.'''

        return(list(reversed(self.path)))
    #
    # end method: get_key_path

    # method: get_co_path
    #
    def get_co_path(self) -> list[DataNode]:
        '''This method gets the co-path from the current node up to the root.'''

        return [node.get_sibling() for node in self.get_key_path() if node.ntype != 'root']
    #
    # end method: get_co_path

    # method: sponsor_assign
    #
    def sponsor_assign(self, mid: Optional[int]=None, key: Optional[int]=None, b_key: Optional[int]=None, join: bool=True) -> None:
        '''This method tags a node as the sponsor node.'''

        self.ntype = 'spon'
        if join:
            self.mid = mid
            self.key = key
            self.b_key = b_key
    #
    # end method: sponsor_assign

    # method: insertion_assign
    #
    def insertion_assign(self) -> None:
        '''This method tags a node as the insertion node.'''

        self.ntype = 'inter'
        self.mid = None
        self.key = None
        self.b_key = None
    #
    # end method: insertion_assign

    # method: new_memb_assign
    #
    def new_memb_assign(self, mid: int) -> None:
        '''This method tags a node as the new member node.'''

        self.ntype = 'mem'
        self.mid = mid
    #
    # end method: new_memb_assign

    # method: transfer_data_remove
    #
    def transfer_data_remove(self, node: DataNode) -> None:
        '''This method transfers data from a specified node and then removes that node.'''

        self.ntype = node.ntype
        self.mid = node.mid
        self.rchild = node.rchild
        self.lchild = node.lchild
        self.children = node.children
        self.key = node.key
        self.b_key = node.b_key
        del node
        gc.collect()
    #
    # end method: transfer_data_remove

    # method: make_root
    #
    def make_root(self) -> None:
        '''This method makes the current node the root.'''

        self.pos = 'NA'
        self.ntype = 'root'
        self.mid = None
        self.parent = None
        self.l = 0
        self.v = 0
        self.name = '<0,0>'
        self.key = None
        self.b_key = None
    #
    # end method: make_root

    # method: print_attributes
    #
    def print_attributes(self) -> None:
        '''This method prints all node attributes.'''

        print(f"\n{'//'.center(80, '-')}")
        print(f"Node Name: {self.name}")
        if self.parent is not None:
            print(f"Node Parent: {self.parent.name}")
        print(f"Node index: <{str(self.l)},{str(self.v)}>")
        print(f"Node Type: {self.ntype}")
        if self.mid is not None:
            print(f"Node id: {str(self.mid)}")
        if self.lchild is not None:
            print(f"Node left child: {self.lchild.name}")
        if self.rchild is not None:
            print(f"Node right child: {self.rchild.name}")
        print(f"Private key: {str(self.key)}")
        print(f"Blind key: {str(self.b_key)}")
        print("Key path:")
        for node in self.get_key_path():
            print(node.name)
        print("Key co-path:")
        for node in self.get_co_path():
            print(node.name)
        print(f"{'//'.center(80, '-')}")
    #
    # end method: print_attributes
#
# end class: DataNode
#
# end file: DataNode.py
