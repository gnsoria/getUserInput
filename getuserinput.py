# !/usr/bin/env python

"""
This module contains tools for getting input from a user.
At any point while getting input, the user may enter "quit", "exit", or
  "leave" to raise a SystemExit exception and quit
"""

import textwrap as tw
from enum import Enum, auto

_EXIT_WORDS = {"quit", "exit", "leave"}

# Constants
Y = 'y'
N = 'n'
YES = 'yes'
NO = 'no'


class OutputMode(Enum):
    """
    Used to determine the output of the get_number function
    """
    INT = auto()
    FLOAT = auto()
    NUM = auto()


def get_string_choice(prompt, return_full_option=False, **kwoptions):
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
        >>> response = get_string_choice(prompt, **input_options)
        Who is the strongest Avenger?
         - 't' for 'Thor'
         - 'i' for 'Iron Man'
         - 'c' for 'Captain America'
         - 'h' for 'The Hulk'
        h
        >>> response
        'h'
    Of course, you can also define the kwoptions in the call:
        >>> response = get_string_choice("Who is the strongest Avenger?",
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
        >>> response = get_string_choice("Who is the strongest Avenger?",
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
    formatted_options = _get_formatted_options(**kwoptions)

    print(tw.fill(prompt))
    while True:
        print(formatted_options)

        user_choice = input()
        if user_choice in kwoptions:
            return user_choice if return_full_option is not True else kwoptions[user_choice]
        elif user_choice in _EXIT_WORDS:
            _sys_exit_msg()

        print("That wasn't one of the options.",)


def _get_formatted_options(**kwoptions):
    """Formats a dictionary of options and returns them as a string"""

    OPTION_TEMPLATE = " - '{0:{1}}' for '{2}'"
    # The 1 as the second arg below is filler because format won't allow 0
    # -2 ensures that the subsequent indent lines up with the first char
    STR_PADDING = len(OPTION_TEMPLATE.format("", 1, "")) - 2

    # This is used to adjust the section before the "-" to be as wide as the
    # longest key
    space = max(map(len, kwoptions))
    pad_length = space + STR_PADDING

    prompt_lines = []

    for key in kwoptions:
        # This wraps the text at the max line length and pads the new
        # lines so it looks nice.
        full_option = tw.fill(
            kwoptions[key],
            subsequent_indent=" " * pad_length)

        prompt_lines.append(OPTION_TEMPLATE.format(key, space, full_option))

    return "\n".join(prompt_lines)


def get_yes_no(prompt, return_full_option=False):
    """
    Calls get_string_choice and only allows yes or no as response. Return y/n.
    Returns the approrpriate the module constant Y, N, YES, or NO

    Example:
        >>> response = get_yes_no("Is Footloose still the greatest movie ever?")
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
    yes_no = {Y:YES, N:NO}
    return get_string_choice(prompt, return_full_option, **yes_no)


def get_true_false(prompt):
    """
    Calls get_string_choice and only allows boolean response.
    Return boolean True or False.

    Example:
        >>> get_true_false("True or False: Star-Lord was responsible for"
                         "the team losing on Titan:")
        True or False: Star-Lord was responsible for the team losing on Titan:
        - 't' for 'True'
        - 'f' for 'False'
        f
        False
        >>>
    """
    if get_string_choice(prompt, t="True", f="False") == "t":
        return True
    return False


def get_number(prompt, min_opt=1, max_opt=10, data_type=OutputMode.NUM,
              restrict_range=False):
    """
    Return the user's choice of number.

    If restrict_range=False, don't restrict the range (deafult).
    Otherwise, restrict answer to between min/max_opt.

    Use data_type to determine what type of number to return, passing in an
      OutputMode enum. Examples:
    - ui.OutputMode.NUM: whatever type the user entered (this is the default)
        >>> my_num = get_number("Pick a number:")
        Pick a number:
        5.0
        >>> my_num
        5.0
        >>> my_num = get_number("Pick a number:")
        Pick a number:
        5
        >>> my_num
        5
    - ui.OutputMode.INT: integers
        >>> my_num = get_number("Pick an integer:", 1, 10, ui.OutputMode.INT,
                               restrict_range=False)
        Pick an integer:
        (min = 1, max = 10)
        5.0
        >>> my_num
        5
    - ui.OutputMode.FLOAT: floats
        >>> my_num = get_number("Pick an integer:", 1, 10, ui.OutputMode.FLOAT
                               restrict_range=False)
        Pick an integer:
        (min = 1, max = 10)
        5
        >>> my_num
        5.0
    """
    print(tw.fill(prompt))

    if not restrict_range:
        # User is not restricted to the min/max range
        num_choice = _accept_and_validate_number()
    else:
        num_choice = get_number_in_range(min_opt, max_opt)

    if data_type == OutputMode.NUM:
        return num_choice
    elif data_type == OutputMode.FLOAT:
        return float(num_choice)
    elif data_type == OutputMode.INT:
        return int(num_choice)


def get_number_in_range(min_opt, max_opt):
    """
    Let the user pick a number
    Return it as whatever data type the user used
    """

    # This could live in a separate func but then it'd have to assign
    # min/max_opt even when nothing changes
    if max_opt < min_opt:
        # Switch the order if the maximum is less than the minimum.
        # This is done for aesthetics
        min_opt, max_opt = max_opt, min_opt

    if max_opt == min_opt:
        # It makes no sense for these to be equal, so raise an error
        raise ValueError("The min and max numbers should not be the same.\n")

    print("(min = {0:,}, max = {1:,})".format(min_opt, max_opt))

    while True:
        num_choice = _accept_and_validate_number()

        # Check to see if the num_choice is valid in our range
        if eval("{0}<={1}<={2}".format(min_opt, num_choice, max_opt)):
            return num_choice
        print("Please pick a number between {0} and {1}.".format(
            min_opt,
            max_opt))


def _accept_and_validate_number():
    """
    Accept a user's choice of number, and then return it as a float or int.

    Type is determined by whether the user includes a decimal point.
    """
    while True:
        try:
            num_choice = input()
            if num_choice in _EXIT_WORDS:
                _sys_exit_msg()

            # Return the corresponding number type
            if num_choice.find(".") == -1:
                return int(float(num_choice))
            return float(num_choice)
        except ValueError:
            # Don't raise; just force the user back into the loop
            print("Please pick a number.")


def _sys_exit_msg(msg="Thanks!"):
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
    _demonstrate_get_number()
    _demonstrate_get_string_choice()


def _demonstrate_get_number():
    print("""
    Demonstration of get_number()
    """)

    print("Returns {0}\n".format(get_number(
        "Step right up and pick a number, any number!")))

    print("Returns {0}\n".format(get_number(
        "Only integers this time (decimals will be rounded). "
        "Pick any integer!",
        data_type=OutputMode.INT)))
    print("Returns {0}\n".format(get_number(
        prompt="Now only an integer in the range below!",
        data_type=OutputMode.INT,
        restrict_range=True)))
    print("Returns {0}\n".format(get_number(
        "Now pick a float! (root beer not allowed)",
        data_type=OutputMode.FLOAT)))
    print("Returns {0}\n".format(get_number(
        prompt="And finally, a float in the given range:",
        min_opt=1,
        max_opt=50,
        data_type=OutputMode.FLOAT,
        restrict_range=True)))
    return None


def _demonstrate_get_string_choice():
    print("""
    Demonstration of get_string_choice()
    """)
    DEMO_TEMPLATE = "Returns {}"

    test_return = get_string_choice("What does your mother smell of?",
                                    e="elderberries",
                                    h="hamster")
    print(DEMO_TEMPLATE.format(test_return))

    test_return = get_yes_no(
        "That was just a little Python humor. Did you enjoy it?")
    print(DEMO_TEMPLATE.format(test_return))

    test_return = get_true_false(
        "Is it true that an African swallow could carry a coconut?")
    print(DEMO_TEMPLATE.format(test_return))


if __name__ == "__main__":
    main()
