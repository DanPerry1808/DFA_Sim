from DFA import DFA
from os import path

# List of loaded DFA objects, stored as key value pairs
# filename is key, object is value
dfa_dict = {}

# Checks if a dfa with the name given exists in dfa_dict
def dfa_exists(dfa_name):
    if dfa_name in dfa_dict.keys():
        return True
    else:
        return False

# Command list
# quit - closes program
# show - Lists all currently loaded DFAs
# info [dfa_name] - Prints info about that DFA object
# load [filename] - loads a DFA object from a .dfa file
# run [dfa_name] [input_string] - Runs the named DFA using the string input_string
# (optional parameter -v - outputs full log of all transitions)

# Takes in a list of lines from a .dfa file and tries
# to construct a DFA object from it
def parse_dfa(dfa_file, name):
    alphabet = None
    # Parse alphabet
    # split by spaces
    alpha_line = dfa_file[0].split(" ")
    if alpha_line[0] == "ALPHABET":
        alphabet = tuple(alpha_line[1].split(","))
    else:
        print("ALPHABET missing")
        return None

    # Get number of states
    num_states = 0
    state_line = dfa_file[1].split(" ")
    if state_line[0] == "STATES":
        try:
            num_states = int(state_line[1])
        except ValueError:
            print("Number of states cannot be read as an integer")
            return None
    else:
        print("STATE missing")
        return None
        
    # Get start state
    start_state = None
    start_line = dfa_file[2].split(" ")
    if start_line[0] == "START":
        try:
            start_state = int(start_line[1])
        except ValueError:
            print("Start state cannot be read as an integer")
            return None
    else:
        print("START missing")
        return None
    
    # Get accept states
    accept_line = dfa_file[3].split(" ")
    if accept_line[0] == "ACCEPT":
        accept_states = accept_line[1].split(",")
        # Check number of accept states is not more than the number of states
        if len(accept_states) > num_states:
            print("There are more accept states than available states")
            return None
            
        # Creates an array filled with False values, each value corresponds to that state
        accept_bools = [False] * num_states
        # Convert each accept state to an integer and append to list
        for accept in accept_states:
            try:
                accept_int = int(accept)
                # Once converted to Integer, add to list
                accept_bools[accept_int] = True
            except ValueError:
                print("Could not read an accept state as an integer")
                return None
            
    else:
        print("ACCEPT missing")
        return None
        
    # Check next line is "TRANSITIONS"
    trans_line = dfa_file[4]
    if trans_line == "TRANSITIONS":
        # Transitions takes up rest of file
        transitions = dfa_file[5:]
        # Check END_TRANSITIONS was included at end of file
        if transitions[-1] == "END_TRANSITIONS":
            # Remove "END_TRANSITIONS" from the list, leaving only the transition info
            transitions = transitions[:-1]
            final_transitions = []
            for trans in transitions:
                trans = trans.split(",")
                # Check there are 3 parts to the transitions
                if len(trans) == 3:
                    try:
                        trans[0] = int(trans[0])
                        trans[1] = int(trans[1])
                        final_transitions.append(trans)
                    except ValueError:
                        print("Could not convert state to integer for a transition")
                        return None
                else:
                    print("Invalid length for a transition")
                    return None
            
        else:
            print("END_TRANSITIONS is missing")
            return None
    else:
        print("TRANSITIONS line is missing")
    
    # Creates new DFA
    new_dfa = DFA(alphabet)
    # Adds states
    for b in accept_bools:
        new_dfa.add_state(b)
        
    # Adds transitions
    for trans in final_transitions:
        new_dfa.add_connection(trans[0], trans[1], trans[2])
       
    return new_dfa
       
# Loads in a .dfa file and returns the contents as a list where each element
# of the list is a line from the file
# If file cannot be found, None is returned
def load_file(filepath):
    # Check file exists
    if path.exists(filepath):
        with open(filepath, "r") as f:
            # Split file contents by new line character
            return f.read().split("\n")

    else:
        print("Could not find file at " + filepath)
        return None

       
def parse_line(line):
    split_line = line.split(" ")
    command = split_line[0]
    
    if command == "quit":
        quit()
    elif command == "show":
        print("Listing all currently loaded DFAs")

        # Outputs special message if no DFAs loaded
        if len(dfa_dict) == 0:
            print("No DFAs loaded")
        else:
            for key in dfa_dict:
                print("- " + key)
    elif command == "info":
        if len(split_line) == 2:
            if dfa_exists(split_line[1]):
                print("Info about " + split_line[1])
                dfa_dict[split_line[1]].print_info()
            else:
                print("Could not find DFA with name " + split_line[1])
        else:
            print("Incorrect number of arguments for the info command")
            print("Correct usage: info [dfa_name]")
    elif command == "load":
        if len(split_line) == 2:
            dfa_text = load_file(split_line[1])
            # filename is file name but without extension
            filename = path.basename(split_line[1]).split(".")[0]
            dfa = parse_dfa(dfa_text, filename)

            # Check if DFA was parsed successfully
            if dfa != None:
                dfa_dict[filename] = dfa
                print('Loaded new DFA called "' + filename + '"')
            else:
                # Inform user of error
                print("There was an error trying to parse the DFA")
        else:
            print("Please specify a filepath without spaces")
    elif command == "run":
        # Check if command is correct length
        if len(split_line) > 2:
            # Check if DFA exists in dictionary
            if dfa_exists(split_line[1]):
                # Check if verbose mode active
                verbose = False
                if split_line[-1] == "-verbose" or split_line[-1] == "-v":
                    verbose = True

                # Output result of string                    
                print(dfa_dict[split_line[1]].run(split_line[2], verbose))
            else:
                print("Cannot find DFA called " + split_line[1])
        else:
            print("Incorrect number of arguments for the 'run' command")
            print("Correct usage: 'run [dfa_name] [input_string] (optional) -verbose")
        

while(True):
    next_line = input("DFA-Sim> ")
    parse_line(next_line)
