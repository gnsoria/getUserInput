#!/usr/bin/env python

"""
This module contains tools for getting input from a user.
"""
_EXIT_WORDS = ["quit", "exit", "leave"]

def GetUserInput(prompt, **kwoptions):
    """
    Print out the prompt and then return the input as long as it matches one of the options (given as key/value pairs)
    """
    space = max(map(len, kwoptions))

    while True:
        try:
            print(TruncateAtMax(prompt))
            for key in kwoptions:
                print(" - '{0}' for '{1}'".format(key.ljust(space), \
                    TruncateAtMax(kwoptions[key], max_len=60, spacer=space + 11)))

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
            print("Thanks!")
            raise #raise the SystemExit exception again to exit the program

def GetYesNo(prompt):
    """
    Get user input to the prompt. Only allow yes or no as response. Return y/n.
    """
    return GetUserInput(prompt, y="yes", n="no")

def GetTrueFalse(prompt):
    """
    Get user input to the prompt. Only allow boolean response. Return True or False.
    """
    if GetUserInput(prompt, t="True", f="False") == "t":
        return True
    return False

def GetUserIntegerChoice(prompt, min_opt=1, max_opt=999999999):
    """
    Let the user choose a number from the min_opt to the max_opt. Return that number
    
    Default min = 1
    Default max = 999,999,999 (almost a billion)
    """
    prompt = TruncateAtMax(prompt)
    
    if min_opt == max_opt:
        return max_opt
    
    while True:
        try:
            num_choice = input("{0} \n(min = {1:,}, max = {2:,})\n".format(prompt, min_opt, max_opt))
            
            if num_choice in _EXIT_WORDS:
                quit()
                
            num_choice = int(num_choice)
            if eval("{0}<={1}<={2}".format(min_opt, num_choice, max_opt)):
                return num_choice      
            print("Please pick a number between {0} and {1}.".format(min_opt, max_opt),)
        except ValueError:
            print("Please pick an integer.")
        except SystemExit:
            print("Thanks anyway!")
            raise #raise the SystemExit exception again to exit the program
        except:
            print("\nSomething went wrong...\n")
            raise
    return None
    
def TruncateAtMax(str, max_len=80, spacer=1):
    """
    Truncate a string at max length and continue on the next line. For example:
    string = "this is a test of the truncate func"
    max_len = 15

    output:
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