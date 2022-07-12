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

    # method: join_protocol
    #
    def join_protocol(self) -> None:
        '''This method faciliates a new member joining the group.'''

        print("\nSending a join message to the group ...")
        print("Receiving serial tree object ...")
        print("Tree object received and loaded!")
    #
    # end method: join_protocol

    # method: leave_protocol
    #
    def leave_protocol(self) -> None:
        '''This method faciliates a member leaving the group.'''

        print("\nSending a leave message to the group ...")

    #
    # end method: leave_protocol

    # method: get_events
    #
    def get_events(self) -> None:
        '''This method simulates tree functionality.'''

        while True:
            instruct = input("\n>> Enter event here: ")
            if instruct in ('join', 'j'):
                self.btree.join_event()
            elif instruct in ('leave', 'l'):
                lmem = int(input(">> Enter leaving member ID: "))
                self.btree.leave_event(lmem)
            elif instruct in ('quit', 'q'):
                self.leave_protocol()
                print("Freeing resources and exiting ...")
                return 0
            elif instruct in ('find', 'f'):
                ans = input(">> Would you like to find a member (m) or node (n)? ")
                if ans in ('member', 'm'):
                    iden = input(">> Enter the member ID: ")
                    fmem = self.btree.find_node(int(iden), True)
                    fmem.print_attributes()
                elif ans in ('node', 'n'):
                    iden = input(">> Enter node index (l,v): ")
                    fnode = self.btree.find_node(iden, False)
                    fnode.print_attributes()
                else: print("**> Error: Invalid response!")
            elif instruct in ('print', 'p'):
                self.btree.tree_print()
            elif instruct in ('verbose print', 'vp'):
                self.btree.tree_print()
                self.btree.verbose_node_print()
            elif instruct in ('print group key', 'pg'):
                print(f"\nCurrent Group Key: {str(self.btree.root.key)}")
            elif instruct in ('help', 'h'):
                print("\nValid events:\n join, j\n leave, l\n find, f\n print, p\n verbose print, vp\n print group key, pg\n quit, q")
            else:
                print("\n**> Error: Invald input!\nEnter 'help' or 'h' for a support message.")
    #
    # end method: get_events
#
# end class: TgdhStruct
#
# end file: tgdh_struct.py
