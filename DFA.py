class DFA:

    # Creates a new DFA with the alphabet alpha
    def __init__(self, alpha):
        self.current_state = None
        self.start_state = None
        self.alphabet = alpha
        self.accept_states = []
        # Connection list keeps track of connections between states
        # con_list[i] contains a list of tuples of (new_state, character) values for state i
        self.con_list = []
        
    def print_info(self):
        print("Total number of states: " + str(len(self.con_list)))
        print("Current state: " + str(self.current_state))
        print("Start state: " + str(self.start_state))
        print("Alphabet:")
        print(self.alphabet)
        print("Accept States:")
        print(self.accept_states)

    def get_num_states(self):
        return len(self.con_list)

    def is_valid_state(self, state):
        if state >= 0 and state < self.get_num_states():
            return True
        else:
            return False

    # Adds a new state to the connection matrix, by default is not an accept state
    def add_state(self, accept = False):
        # If first state, make start state by default
        if self.get_num_states() == 0:
            self.set_start_state(0)

        # Add a new entry to the bottom of the connection list
        self.con_list.append([])

        # Append accept status to list of accept states
        self.accept_states.append(accept)


    # Checks if the character given is in the alphabet of the DFA
    def is_valid_character(self, char):
        if char in self.alphabet:
            return True
        else:
            return False
            

    # Creates a new connection between old_state and new_state when character is entered
    def add_connection(self, old_state, new_state, character):
        if self.is_valid_state(old_state):
            if self.is_valid_state(new_state):
                if self.is_valid_character(character):
                    self.con_list[old_state].append((new_state, character))
                else:
                    print("Character is invalid: " + character)
            else:
                print("New state is invalid: " + str(new_state))
        else:
            print("Original state is invalid: " + str(old_state))

            
    # Checks if a DFA has the correct number of connections to be usable
    def is_valid_DFA(self):
        # Each state must have a connection for each character in the alphabet
        for state in self.con_list:
            # Creates an empty set to hold characters of transitions for this state
            state_set = set()
            for conn in state:
                # Add the character from each transition
                state_set.add(conn[1])

            # Checks if number of connections = length of alphabet
            if len(state_set) != len(self.alphabet):
                print("DFA invalid, incorrect number of connections")
                return False

            # Checks if state_list is same as the alphabet set
            if state_set != set(self.alphabet):
                print("DFA invalid, not a connection for every alphabet character")
                return False

        # Check if DFA has start state set
        if self.start_state == None:
            print("DFA invalid, cannot find start state")
            return False

        # If all checks passed, return true
        return True


    # By default, start state is 0 but this will change it
    def set_start_state(self, state):
        self.start_state = state


    # Returns the next state given the current state and the next character input
    def find_next_state(self, char):
        current_transitions = self.con_list[self.current_state]
        i = 0
        for t in current_transitions:
            if t[1] == char:
                return i
            else:
                i += 1

        print("Could not find next state")
        return None


    # Transitions from current state to a new state depending on char
    def transition(self, char):
        next_state = self.find_next_state(char)
        self.current_state = self.con_list[self.current_state][next_state][0]


    # Checks if string only contains characters from alphabet
    def is_valid_string(self, string):
        for char in string:
            if char not in self.alphabet:
                print("Character " + char + " not in alphabet")
                return False
        return True
    

    # Runs the DFA with string as the input
    # Returns "accept" if string is accepted, "reject" otherwise
    # Verbose mode outputs info on each transition
    def run(self, string, verbose = False):
        if self.is_valid_DFA():
            if self.is_valid_string(string):
                self.current_state = self.start_state
                for char in string:
                    # Tracking previous state for verbos mode
                    last_state = self.current_state
                    self.transition(char)
                    # Output verbose mode info
                    if verbose:
                        print("Old state: " + str(last_state) + ", new state: " + str(self.current_state) + ", character: " + str(char))
                        

                # Check if final state is accept state
                if self.accept_states[self.current_state]:
                    result = "accept"
                else:
                    result = "reject"
            else:
                result = "Error in string"
        else:
            result = "Error in DFA"

        # Set current state back to None as the DFA finishes
        self.current_state = None
        return "Input string: " + string + " Result: " + result

        
if __name__ == "__main__":
    alphabet = ("a", "b")
    test = DFA(alphabet)
    test.add_state()
    test.add_state()
    test.add_state()
    test.add_state(True)
    test.add_state()
    
    test.add_connection(0, 1, "a")
    test.add_connection(0, 4, "b")
    test.add_connection(1, 4, "a")
    test.add_connection(1, 2, "b")
    test.add_connection(2, 3, "a")
    test.add_connection(2, 4, "b")
    test.add_connection(3, 3, "a")
    test.add_connection(3, 3, "b")
    test.add_connection(4, 4, "a")
    test.add_connection(4, 4, "b")

    print(test.run("ababbb"))
    test.print_info()
    
