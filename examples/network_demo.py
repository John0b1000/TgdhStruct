# file: network_demo.py
#
'''
This example demonstrates instantiation of a MemberAgent class.
A TGDH scheme is carried out using the multi-agent system.
'''

# import modules
#
import sys
from tgdhstruct import MemberAgent

# function: main
#
def main(argv):
    '''This is the main function.'''

    # create an initial tree
    #
    group_tree = MemberAgent(int(argv[1]))

    # demonstrate a join event
    #
    input("\n>> Press 'enter' or 'return' to trigger a join event ")
    group_tree.join_protocol()

    # do another join
    #
    input("\n>> Press 'enter' or 'return' to trigger a join event ")
    group_tree.join_protocol()

    # demonstrate a leave event
    #
    input("\n>> Press 'enter' or 'return' to trigger a leave event ")
    group_tree.leave_protocol(3)

    # demonstrate another leave event
    #
    input("\n>> Press 'enter' or 'return' to trigger a leave event ")
    group_tree.leave_protocol(5)

    input("\n>> Press 'enter' or 'return' to trigger a leave event ")
    group_tree.leave_protocol(2)

    input("\n>> Press 'enter' or 'return' to trigger a leave event ")
    group_tree.leave_protocol(6)

    # exit gracefully
    #
    group_tree.close()

# begin gracefully
#
if __name__ == '__main__':
    main(sys.argv)

#
# end file: network_demo.py
