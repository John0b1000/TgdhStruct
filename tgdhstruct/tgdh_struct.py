# file: tgdh_struct.py
#
'''This file contains the tgdhstruct driver class.'''

# import modules
#
from tgdhstruct.binary_tree import BinaryTree

# class: Tgdhstruct
#
class TgdhStruct:
    '''
    Description
    -----------
    This is the driver class for implementation of the TGDH scheme.

    Attributes
    ----------
    initial_size : int
        The initial size of the group
    unique_ID : int
        The unique ID of this node

    Methods
    -------
    tree_initialize(self) -> BinaryTree:
        This method creates a binary tree structure.
    join_protocol(self) -> None:
        This method faciliates a new member joining the group.
    leave_protocol(self) -> None:
        This method faciliates a member leaving the group.
    get_events(self) -> None:
        This method is to demonstrate tree functionality.
    '''

    # constructor
    #
    def __init__(self, initial_size: int, unique_id: int):
        '''This is the constructor.'''

        self.initial_size = initial_size
        self.unique_id = unique_id
        self.btree = self.tree_initialize()
    #
    # end constructor

    # method: tree_initialize
    #
    def tree_initialize(self) -> BinaryTree:
        '''This method creates a binary tree structure.'''

        btree = BinaryTree(self.initial_size, self.unique_id)
        return btree
    #
    # end method: tree_initialize
#
# end class: TgdhStruct
#
# end file: tgdh_struct.py
