# !/usr/bin/env python

"""
This module contains tools for getting input from a user.
At any point while getting input, the user may enter "quit",
  "exit", or "leave" to quit()
"""

from textwrap import fill
from enum import Enum, auto

_EXIT_WORDS = {"quit", "exit", "leave"}


class OutputMode(Enum):
    """
    Used to determine the output of the GetNumber function
    """
    INT = auto()
    FLOAT = auto()
    NUM = auto()


def GetStringChoice(prompt, **kwoptions):
    """
    Print out the prompt and then return the input as long as it matches one
    of the options (given as key/value pairs)

    Example call:
        >>> prompt = "Who is the strongest Avenger?"
        >>> input_options = {
                "t":"Thor",
                "i":"Iron Man",
                "c":"Captain America",
                "h":"The Hulk"}
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
        >>> response = GetStringChoice("Who is the strongest Avenger?",
                t="Thor",
                i="Iron Man",
                c="Captain America",
                h="The Hulk")
        Who is the strongest Avenger?
        - 't' for 'Thor'
        - 'i' for 'Iron Man'
        - 'c' for 'Captain America'
        - 'h' for 'The Hulk'
        h
        >>> response
        'h'

    Invalid results are rejected:
        >>> response = GetStringChoice("Who is the strongest Avenger?",
                t="Thor",
                i="Iron Man",
                c="Captain America",
                h="The Hulk")
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
    OPTION_TEMPLATE = " - '{0:{1}}' for '{2}'"
    # The 1 as the second arg below is filler because format won't allow 0
    # -2 ensures that the subsequent indent lines up with the first char
    STR_PADDING = len(OPTION_TEMPLATE.format("", 1, "")) - 2
    MAX_LINE_LEN = 60

    # This adjusts the section before the "-" to be as wide as the longest key
    space = max(map(len, kwoptions))

    while True:
        try:
            print(fill(prompt))
            for key in kwoptions:
                # This wraps the text at the max line length and pads the new
                # lines so it looks nice.
                pad_length = space + STR_PADDING
                full_option = fill(
                    kwoptions[key],
                    width=MAX_LINE_LEN,
                    subsequent_indent=" " * pad_length)

                print(OPTION_TEMPLATE.format(key, space, full_option))

            user_choice = input()
            if user_choice in kwoptions:
                return user_choice
            elif user_choice in _EXIT_WORDS:
                raise SystemExit

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
    Calls GetStringChoice and only allows boolean response.
    Return boolean True or False.

    Example:
        >>> GetTrueFalse("True or False - Star-Lord was responsible for"
                         "the team losing on Titan:")
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


def GetNumber(prompt, min_opt=-1, max_opt=-1, data_type=OutputMode.NUM):
    """
    Return the user's choice of number.

    If min_opt and max_opt == -1.0, don't restrict the range.
    Otherwise, restrict to the range given.

    Use data_type to determine what type of number to return, passing in an
      OutputMode enum. Examples:
    - ui.OutputMode.NUM: whatever type the user entered (this is the default)
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
    - ui.OutputMode.INT: integers
        >>> my_num = GetNumber("Pick an integer:", 1, 10, ui.OutputMode.INT)
        Pick an integer:
        (min = 1, max = 10)
        5.0
        >>> my_num
        5
    - ui.OutputMode.FLOAT: floats
        >>> my_num = GetNumber("Pick an integer:", 1, 10, ui.OutputMode.FLOAT)
        Pick an integer:
        (min = 1, max = 10)
        5
        >>> my_num
        5.0
    """
    print(fill(prompt))

    if min_opt == -1.0 and max_opt == -1.0:
        # No range given
        num_choice = _AcceptAndValidateNumber()
    else:
        num_choice = GetNumberInRange(min_opt, max_opt)

    if data_type == OutputMode.NUM:
        return num_choice
    elif data_type == OutputMode.FLOAT:
        return float(num_choice)
    elif data_type == OutputMode.INT:
        return int(num_choice)


def GetNumberInRange(min_opt, max_opt):
    """
    Let the user pick a number
    Return it as whatever data type the user used
    """
    while True:
        try:
            if max_opt < min_opt:
                # Switch the order if the maximum is less than the minimum.
                # This is done for aesthetics
                min_opt, max_opt = max_opt, min_opt
            if max_opt == min_opt:
                # It makes no sense for these to be equal, so raise an error
                raise ValueError

            print("(min = {0:,}, max = {1:,})".format(min_opt, max_opt))
            num_choice = _AcceptAndValidateNumber()

            # Check to see if the num_choice is valid in our range
            if eval("{0}<={1}<={2}".format(min_opt, num_choice, max_opt)):
                return num_choice
            print("Please pick a number between {0} and {1}.".format(
                min_opt,
                max_opt),)
                # The comma here places the user's response on the same line
        except SystemExit:
            _SysExitMsg()
        except ValueError as v:
            print("\nThe min and max numbers should not be the same.\n")
            raise v
        except Exception as e:
            print("\nSomething went wrong...\n")
            raise e


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

            # Return the corresponding number type
            if num_choice.find(".") == -1:
                return int(float(num_choice))
            return float(num_choice)
        except ValueError:
            print("Please pick a number.")
        except SystemExit:
            raise
        except Exception:
            print("\nSomething went wrong...\n")
            raise


def _SysExitMsg(msg="Thanks!"):
    """
    A consistent process for SystemExit when a user enters one of the
    _EXIT_WORDS
    """
    print(msg)
    raise SystemExit  # Raise the SystemExit exception again to exit


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

    print("Returns {0}\n".format(GetNumber(
        "Step right up and pick a number, any number!")))

    print("Returns {0}\n".format(GetNumber(
        "Only integers this time (decimals will be rounded). "
        "Pick any integer!",
        data_type=OutputMode.INT)))
    print("Returns {0}\n".format(GetNumber(
        "Now only an integer between 1 and 10!", 1, 10, data_type=OutputMode.INT)))
    print("Returns {0}\n".format(GetNumber(
        "Now pick a float! (root beer not allowed)", data_type=OutputMode.FLOAT)))
    print("Returns {0}\n".format(GetNumber(
        "And finally, a float between 1 and 10.", 1, 10, data_type=OutputMode.FLOAT)))
    return None


def _demonstrateGetStringChoice():
    print("""
    Demonstration of GetStringChoice()
    """)

    print("Returns {0}\n".format(GetStringChoice(
        "What does your mother smell of?", e="elderberries", h="hamster")))

    print("Returns {0}\n".format(GetYesNo(
        "That was just a little Python humor. Did you enjoy it?")))

    print("Returns {0}\n".format(GetTrueFalse(
        "Is it true that an African swallow could carry a coconut?")))

    return None


if __name__ == "__main__":
    main()
