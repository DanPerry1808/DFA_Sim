# DFA_Sim
A text based program for running Determinative Finite Automata. DFAs can be described in a simple text based format and then read into the program where you can pass strings to them.

## Download and Installation
You will need Python 3 installed as a prerequisite
1) Download the zip file from the releases section
2) Extract the zip file to its own folder
3) Open a terminal in this new folder
4) Run python passing in DFA_console.py as an argument

## Using the console
All console commands are lowercase and have spaces separating the values.

### Command List
- `quit` - Closes the program
- `show` - Lists all currently loaded DFAs
- `info [dfa_name]` - Prints info about that DFA object
- `load [filename]` - loads a DFA object from a .dfa file 
	- Can be called with same file name more than once to update that DFA
	- Filepath is relative from the folder you ran the program from and must not contain spaces
- `run [dfa_name] [input_string]` - Runs the named DFA using the string input_string 
	- Optional parameter `-v` outputs full log of all transitions)

## Writing a .dfa file
A .dfa file describes a single automaton and has a rigid structure. The only optional part of the file is the indentation in the transitions section. It must follow this format:

```ALPHABET [list of comma separated characters with no spaces eg. x,y,z]
STATES [integer]
START [integer]
ACCEPT [list of comma separated integers with no spaces eg. 3,5]
TRANSITIONS
	[current_state],[new_state],[character]
	[current_state],[new_state],[character]
END_TRANSITIONS```

There is an example file `test.dfa` included.