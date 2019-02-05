#!/usr/bin/env python

"""
This module contains tools for getting input from a user. At any point, enter "quit", "exit", or "leave" to quit()
"""
_EXIT_WORDS = ["quit", "exit", "leave"]
INT_ = "INT"
FLOAT_ = "FLOAT"
NUM = "NUM"
STR_ = "STRING"


def GetStringChoice(prompt, **kwoptions):
    """
    Print out the prompt and then return the input as long as it matches one of the options (given as key/value pairs)

    Example call:
        >>> prompt = "Who is the strongest Avenger?"
        >>> input_options = {"t":"Thor", "i":"Iron Man", "c":"Captain America", "h":"The Hulk"}
        >>> response = GetStringChoice(prompt, **input_options)
        Who is the strongest Avenger?
         - 't' for 'Thor'
         - 'i' for 'Iron Man'
         - 'c' for 'Captain America'
         - 'h' for 'The Hulk'
        h
        >>> response
        'h'
    Of course, you can also define the kwoptions in the call:
        >>> response = GetStringChoice("Who is the strongest Avenger?", t="Thor", i="Iron Man", c="Captain America", h="The Hulk")
        Who is the strongest Avenger?
        - 't' for 'Thor'
        - 'i' for 'Iron Man'
        - 'c' for 'Captain America'
        - 'h' for 'The Hulk'
        h
        >>> response
        'h'
    
    Invalid results are rejected:
        >>> response = GetStringChoice("Who is the strongest Avenger?", t="Thor", i="Iron Man", c="Captain America", h="The Hulk")
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
    Calls GetStringChoice and only allows yes or no as response. Return y/n.

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
    return GetStringChoice(prompt, y="yes", n="no")

def GetTrueFalse(prompt):
    """
    Calls GetStringChoice and only allows boolean response. Return True or False.

    Example:
        >>> GetTrueFalse("True or False - Star-Lord was responsible for the team losing on Titan:")
        True or False - Star-Lord was responsible for the team losing on Titan:
        - 't' for 'True'
        - 'f' for 'False'
        f
        False
        >>>
    """
    if GetStringChoice(prompt, t="True", f="False") == "t":
        return True
    return False

def GetNumber(prompt, min_opt=-1, max_opt=-1, data_type=NUM):
    """
    Return the user's choice of number.

    If min_opt and max_opt == -1.0, don't restrict the range.
    Otherwise, restrict to the range given.

    Use data_type to determine what type of number to return.
    Use the global INT_, FLOAT_, or NUM constants.
    - ui.NUM: whatever type the user entered (this is the default)
        >>> my_num = GetNumber("Pick a number:")
        Pick a number:
        5.0
        >>> my_num
        5.0
        >>> my_num = GetNumber("Pick a number:")
        Pick a number:
        5
        >>> my_num
        5
    - ui.INT_: integers
        >>> my_num = GetNumber("Pick an integer:", 1, 10, ui.INT_)
        Pick an integer: 
        (min = 1, max = 10)
        5.0
        >>> my_num
        5
    - ui.FLOAT_: floats
        >>> my_num = GetNumber("Pick an integer:", 1, 10, ui.FLOAT_)
        Pick an integer: 
        (min = 1, max = 10)
        5
        >>> my_num
        5.0
    """
    prompt = _TruncateAtMax(prompt)
    
    if min_opt==-1.0 and max_opt==-1.0:
        #no range
        try:
            print(f"{prompt}")
            num_choice = _AcceptAndValidateNumber()
        except:
            print("\nSomething went wrong...\n")
            raise
    else:
        try:
            print(f"{prompt}")
            num_choice = GetNumberInRange(min_opt, max_opt)
        except:
            print("\nSomething went wrong...\n")
            raise
    
    if data_type == NUM:
        return num_choice
    elif data_type == FLOAT_:
        return float(num_choice)
    elif data_type == INT_:
        return int(num_choice)

def GetNumberInRange(min_opt, max_opt):
    """
    Let the user pick a number and return it as whatever data type the user used.
    """
    while True:
        try:
            if max_opt < min_opt:
                min_opt, max_opt = max_opt, min_opt
            if max_opt == min_opt:
                return max_opt #ideally, this would raise an error. figure out what to raise here
            
            print(f"(min = {min_opt:,}, max = {max_opt:,})")
            num_choice = _AcceptAndValidateNumber()

            if eval(f"{min_opt}<={num_choice}<={max_opt}"):
                return num_choice      
            print(f"Please pick a number between {min_opt} and {max_opt}.",)
        except SystemExit:
            _SysExitMsg()
        except:
            print("\nSomething went wrong...\n")
            raise

def _AcceptAndValidateNumber():
    """
    Accept a user's choice of number, and then return it as a float or int.

    Type is determined by whether the user includes a decimal point.
    """
    while True:
        try:
            num_choice = input()
            if num_choice in _EXIT_WORDS:
                _SysExitMsg()
            
            #return the corresponding number type
            if num_choice.find(".") == -1:
                return int(float(num_choice))
            return float(num_choice)
        except ValueError:
            print("Please pick a number.")
        except SystemExit:
            raise
        except:
            print("\nSomething went wrong...\n")
            raise

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
    raise SystemExit #raise the SystemExit exception again to exit the program




def main():
    """
    A demonstration function.
    """
    _demonstrateGetNumber()
    _demonstrateGetStringChoice()

def _demonstrateGetNumber():
    print("""
    Demonstration of GetNumber()
    """)

    GetNumber("Step right up and pick a number, any number!")

    GetNumber("Only integers this time. Pick any integer!", data_type=INT_)
    GetNumber("Now only an integer between 1 and 10!", 1, 10, data_type=INT_)
    GetNumber("Now pick a float! (root beer not allowed)", data_type=FLOAT_)
    GetNumber("And finally, a float between 1 and 10.", 1, 10, data_type=FLOAT_)
    return None

def _demonstrateGetStringChoice():
    print("""
    Demonstration of GetStringChoice()
    """)

    GetStringChoice("What does your mother smell of?", "e"="elderberries", "h"="hamster")

    GetYesNo("That was just a little Python humor. Did you enjoy it?")

    GetTrueFalse("Is it true that an African swallow could carry a coconut?")

    return None

if __name__ == "__main__":
    main()