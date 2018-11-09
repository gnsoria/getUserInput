#!/usr/bin/env python

"""
This module contains tools for getting input from a user. At any point, enter "quit", "exit", or "leave" to quit()
"""
_EXIT_WORDS = ["quit", "exit", "leave"]

def GetUserInput(prompt, **kwoptions):
    """
    Print out the prompt and then return the input as long as it matches one of the options (given as key/value pairs)

    Example call:
        >>> prompt = "Who is the strongest Avenger?"
        >>> input_options = {"t":"Thor", "i":"Iron Man", "c":"Captain America", "h":"The Hulk"}
        >>> response = GetUserInput(prompt, **input_options)
        Who is the strongest Avenger?
         - 't' for 'Thor'
         - 'i' for 'Iron Man'
         - 'c' for 'Captain America'
         - 'h' for 'The Hulk'
        h
        >>> response
        'h'
    Of course, you can also define the kwoptions in the call:
        >>> response = GetUserInput("Who is the strongest Avenger?", t="Thor", i="Iron Man", c="Captain America", h="The Hulk")
        Who is the strongest Avenger?
        - 't' for 'Thor'
        - 'i' for 'Iron Man'
        - 'c' for 'Captain America'
        - 'h' for 'The Hulk'
        h
        >>> response
        'h'
    
    Invalid results are rejected:
        >>> response = GetUserInput("Who is the strongest Avenger?", t="Thor", i="Iron Man", c="Captain America", h="The Hulk")
        Who is the strongest Avenger?
        - 't' for 'Thor'
        - 'i' for 'Iron Man'
        - 'c' for 'Captain America'
        - 'h' for 'The Hulk'
        Ant-Man
        That wasn't one of the options.
        Who is the strongest Avenger?
        ...
    """
    space = max(map(len, kwoptions))

    while True:
        try:
            print(_TruncateAtMax(prompt))
            for key in kwoptions:
                print(" - '{0}' for '{1}'".format(key.ljust(space), \
                    _TruncateAtMax(kwoptions[key], max_len=60, spacer=space + 11)))

            user_choice = input("")
            if user_choice in kwoptions:
                return user_choice
            elif user_choice in _EXIT_WORDS:
                quit()
        
            print("That wasn't one of the options.",)
        except TypeError:
            print("\n\n")
            raise
        except SystemExit:
            _SysExitMsg()

def GetYesNo(prompt):
    """
    Calls GetUserInput and only allows yes or no as response. Return y/n.

    Example:
        >>> response = GetYesNo("Is Footloose still the greatest movie ever?")
        Is Footloose still the greatest movie ever?
        - 'y' for 'yes'
        - 'n' for 'no'
        It never was!
        That wasn't one of the options.
        Is Footloose still the greatest movie ever?
        - 'y' for 'yes'
        - 'n' for 'no'
        n
        >>> response
        'n'

    """
    return GetUserInput(prompt, y="yes", n="no")

def GetTrueFalse(prompt):
    """
    Calls GetUserInput and only allows boolean response. Return True or False.

    Example:
        >>> GetTrueFalse("True or False - Star-Lord was responsible for the team losing on Titan:")
        True or False - Star-Lord was responsible for the team losing on Titan:
        - 't' for 'True'
        - 'f' for 'False'
        f
        False
        >>>
    """
    if GetUserInput(prompt, t="True", f="False") == "t":
        return True
    return False

def GetUserIntegerChoice(prompt, min_opt=1, max_opt=999999999):
    """
    Let the user choose a number from the min_opt to the max_opt. Return that number
    
    Default min = 1
    Default max = 999,999,999 (almost a billion)

    Example (no min/max):
        >>> guess = GetUserIntegerChoice("How scenarios did Doctor Strange see in Infinity War?")
        How scenarios did Doctor Strange see in Infinity War?
        (min = 1, max = 999,999,999)
        Fourteen million
        Please pick an integer.
        How scenarios did Doctor Strange see in Infinity War?
        (min = 1, max = 999,999,999)
        14000605
        >>> guess
        14000605
    
    Example (with min/max):
        >>> guess = GetUserIntegerChoice("Pick a number between 1 and 12!", 1, 12)
        Pick a number between 1 and 12!
        (min = 1, max = 12)
        13
        Please pick a number between 1 and 12.
        Pick a number between 1 and 12!
        (min = 1, max = 12)
        2
        >>> guess
        2

    """
    prompt = _TruncateAtMax(prompt)
    
    if min_opt == max_opt:
        return max_opt
    
    while True:
        try:
            num_choice = input("{0} \n(min = {1:,}, max = {2:,})\n".format(prompt, min_opt, max_opt))
            
            if num_choice in _EXIT_WORDS:
                quit()
                
            num_choice = int(float(num_choice))
            if eval("{0}<={1}<={2}".format(min_opt, num_choice, max_opt)):
                return num_choice      
            print("Please pick a number between {0} and {1}.".format(min_opt, max_opt),)
        except ValueError:
            print("Please pick an integer.")
        except SystemExit:
            _SysExitMsg()
        except:
            print("\nSomething went wrong...\n")
            raise
    return None
    
def _TruncateAtMax(str, max_len=80, spacer=1):
    """
    Truncate a string at max length and continue on the next line. For example:
    >>>string = "this is a test of the truncate func"
    >>>max_len = 15
    >>>_TruncateAtMax(string, max_len)
    > this is a test 
    > of the truncate
    > func
    """
    
    if len(str) <= max_len - spacer:
        return str
    
    display_str = []
    next_line = ""
    spacing = "\n" + (" " * spacer)
    terms = str.split()
    
    for term in terms:
        if len(next_line + term) < max_len:
            next_line += term + " "
        else:
            display_str.append(next_line)
            next_line = term + " "
    else:
        #adds any stragglers (if next_line != "" but also !< max at the end of terms)
        display_str.append(next_line) 

    truncated_str = spacing.join(display_str)
    
    return truncated_str[1:] if truncated_str[0] == "\n" else truncated_str[:]

def _SysExitMsg(msg="Thanks!"):
    """
    A consistent process for SystemExit error catching
    """
    print(msg)
    raise #raise the SystemExit exception again to exit the program