# file: command_demo.py
#
'''
This example demonstrates instantiation of a TgdhStruct object.
The simulation of events from the command line is also shown.
'''

# import modules
#
from tgdhstruct import TgdhStruct

# function: main
#
def main():
    '''This is the main function.'''

    # instantiate a TgdhStruct object
    # The first argument is the initial size of the tree: 2
    # The second argument is our unique member ID: 1
    #
    my_tree = TgdhStruct(2, 1)

    # simulate events from the command line
    #
    return my_tree.get_events()
#
# end function: main

# begin gracefully
#
if __name__ == "__main__":
    main()

#
# end file: command_demo.py
