from random import randint
import re
from enum import Enum
from user_exceptions import InvlidRollFormatException

# variables
# replace_chars_regex = r'[\s\`\~\!\@\#\$\%\^\&\*\(\)\_\=\[\]\{\}\\\|\;\:\'\"\,\<\>\/\?\t\na-ce-zA-CE-Z]'
replace_chars_regex = r'[^d\d+-]'
replace_chars_pattern = re.compile(replace_chars_regex)
replace_chars = '`~!@#$%^&*)(_=][}{\\|;:\'",.></? \t\r\n'

# regex checks
checkSave = r'^(add|set|save)'  # starts with set, save, or keep
checkDel = r'^(delete|del|remove|destroy)'  # start with delete, del, remove, or destroy
check_roll = r'([0-9]+[dD][0-9]+)'  # check for xdx
check_valid_basic = r'(\d+\s*[+-]\s*)+|(\d+[dD]\d+)'
checkMod = r'(\s*[+-]\s*)'  # find +/- symbols
check_double_plus = r'(\s*[+]\s*){2,}'  # find 2 or more +/- in a row
check_double_minus = r'(\s*[-]\s*){2,}'  # find 2 or more +/- in a row
checkDigits = r'^\d+$'  # check for only digits
checkQuit = r'^(end|exit|stop|quit|zxcv)'  # starts with quit, exit, or stop
checkHelp = r'^(help|\-h)'  # check for the word 'help'
checkInvalidChars = r'(?:(?![dD0-9+\-])[\x20-\x7e])+'  # check for everything that isn't a number or 'd' or +/-
"""Checking for optional modifiers
rh = help
ra = advantage
rb = best
rd = disadvantage
rw = worst
"""


class RollType(Enum):
    ADVANTAGE = 'ADVANTAGE'        # +1d, drop lowest
    DISADVANTAGE = 'DISADVANTAGE'  # +1d, drop highest
    BEST = 'BEST'                  # keep single best
    WORST = 'WORST'                # keep single worst
    POOL = 'POOL'                  # roll dice pool, keep single highest
    STANDARD = 'STANDARD'          # roll normally


help_message = """
Input Examples:
    1d20
    1d100
    1d20+4
    1d20 + 6 + 2d4
    2d6 - 1
Roll types are:
    standard (default)
    advantage (input: "a")
    disadvantage (input: "d")
    best (input: "b")
    worst (input: "w")
"""


class DiceRoller():
    def __init__(self) -> None:
        self.special_flag = True
        self.roll_eval_str = ""
        self.roll_dis_str = ""
        self.roll_list = []
        self.roll_type = RollType.STANDARD

    def __get_num_and_sides(self, raw_roll) -> tuple:
        """get number of dice, and dice sides"""
        num_dice, sides = re.split(r'[dD]', raw_roll, maxsplit=2)
        num_dice, sides = int(num_dice), int(sides)

        return num_dice, sides

    def roll_dice(self, num_dice, sides) -> list:
        """
        Roll dice with number of dice and dice sides
        Return: list of roll values
        """

        rolls = []
        for i in range(num_dice):
            rolls.append(randint(1, sides))

        return rolls

    def __add_items(self, sign, num) -> int:
        """Deciding to add positive or negative number"""
        if type(num) is list:
            num = sum(num)

        if sign == '-':
            return num * -1

        return num

    def __clean_roll_input(self, roll_input) -> list:
        """get list of rolls and modifiers"""
        # see if it's a valid roll
        if not re.match(check_valid_basic, roll_input):
            raise InvlidRollFormatException(roll_input)

        strip_double_mods = re.sub(check_double_plus, '+', roll_input)
        strip_double_mods = re.sub(check_double_minus, '-', strip_double_mods)
        user_rolls = re.split(checkMod, strip_double_mods)

        cleaned_rolls = []
        for item in user_rolls:
            if len(re.findall(r'[dD]', item)) > 1:  # check for multiple "d's" in the roll
                raise InvlidRollFormatException(roll_input)
            elif re.findall(checkInvalidChars, item):  # check of other invalid characters
                raise InvlidRollFormatException(roll_input)

            cleaned_rolls.append(item)
        return cleaned_rolls

    def __construct_output_std(self, roll_input) -> list:
        """construct output and get total roll"""
        # standard roll
        for indx, item in enumerate(roll_input):
            # check for dice roll (xdx)
            if re.match(check_roll, item) is not None:
                # get number of dice, and dice sides
                num_dice, sides = self.__get_num_and_sides(item)

                # get list of roll values [int]
                roll_values = self.roll_dice(num_dice, sides)
                self.roll_dis_str += '(' + '+'.join([str(n) for n in roll_values]) + ')'
                self.roll_eval_str += '(' + '+'.join([str(n) for n in roll_values]) + ')'
            else:
                self.roll_dis_str += item
                self.roll_eval_str += item

        print(f'roll_dis_str: {self.roll_dis_str}')
        print(f'roll_eval_str: {self.roll_eval_str}')
        print(f'value: {eval(self.roll_eval_str)}')

        """
        # doing way too much since eval() exists
        total = 0  # total number rolled +/- others
        output = []  # output string list
        for indx, item in enumerate(roll_input):
            if indx > 0:
                sign = roll_input[indx - 1]
            else:
                sign = '+'

            # check for dice roll (xdx)
            if re.match(check_roll, item) is not None:
                # get number of dice, and dice sides
                num_dice, sides = self.__get_num_and_sides(item)

                item = self.roll_dice(num_dice, sides)
                total += self.__add_items(sign, item)

                output.append('(')
                for i, val in enumerate(item):
                    if i == (len(item) - 1):
                        output.append(str(val))
                    else:
                        output.append(f'{str(val)} + ')
                output.append(') ')
            elif re.search(checkMod, item) is not None:  # is modifier (+/-)
                output.append(item + ' ')
            elif re.match(checkDigits, item) is not None:  # is digit (0-9)
                output.append(item + ' ')
                item = int(item)
                total += self.__add_items(sign, item)

        return [output, total]
        """

    def __construct_advantage_output(self, roll_input: str) -> tuple:
        """
        Rolling with advantage.
          Add +1d to first die rolled and drop the lowest result.
        """
        adv_flag = -1
        print("rolling with advantage")

        for indx, item in enumerate(roll_input):
            # check for dice roll (xdx)
            if re.match(check_roll, item) is not None:
                # get number of dice, and dice sides
                num_dice, sides = self.__get_num_and_sides(item)

                # add 1 die for advantage if it hasn't been done yet
                if self.special_flag:
                    self.special_flag = False
                    num_dice += 1

                # get list of roll values [int]
                roll_values = self.roll_dice(num_dice, sides)
                # TODO remove logging
                print('rolls:')
                print(roll_values)

                # get lowest rolled value
                lowest = min(roll_values)

                # put roll values into the display string
                self.roll_dis_str += '('
                for i, n in enumerate(roll_values):
                    # find lowest value, print crossed out in message
                    if adv_flag < 0 and n == lowest:
                        adv_flag = indx
                        # cross out lowest value
                        self.roll_dis_str += f'*~~{str(n)}~~*'
                    else:
                        self.roll_dis_str += f'{str(n)}'

                    # add "+" if not the last element
                    if i < len(roll_values) - 1:
                        self.roll_dis_str += '+'
                self.roll_dis_str += ')'

                if adv_flag == indx:
                    roll_values.remove(lowest)
                self.roll_eval_str += '(' + '+'.join([str(n) for n in roll_values]) + ')'
            else:
                self.roll_dis_str += item
                self.roll_eval_str += item

        print(f'roll_dis_str: {self.roll_dis_str}')
        print(f'roll_eval_str: {self.roll_eval_str}')
        print(f'value: {eval(self.roll_eval_str)}')

    def __get_roll_type(self, r_type: str):
        """Chooses proper enum for given roll type"""
        if r_type.startswith('a'):
            self.roll_type = RollType.ADVANTAGE
        elif r_type.startswith('d'):
            self.roll_type = RollType.DISADVANTAGE
        elif r_type.startswith('b'):
            self.roll_type = RollType.BEST
        elif r_type.startswith('w'):
            self.roll_type = RollType.WORST
        elif r_type.startswith('p'):
            self.roll_type = RollType.POOL

    def handle_rolls(self, user_in: str, r_type: str = 's'):
        """Performs some checks and returns final output"""
        cleaned_rolls = []  # set default empty rolls list

        self.__get_roll_type(r_type.lower())

        if user_in.lower().startswith('help'):
            return help_message

        # strip out all unexpected characters from the string
        user_in = re.sub(replace_chars_pattern, '', user_in).lower()
        user_in = re.sub(r'(dd+)', 'd', user_in)

        error_message = f'"{user_in}" is not recognized as a valid roll input.' \
            ' Please try again with something like: 2d6 or 1d20+2+1d4'

        # Try to get the "roll" in a list. Return error message if something goes wrong.
        try:
            cleaned_rolls = self.__clean_roll_input(user_in)
        except InvlidRollFormatException as e:
            print(e.message)
            return error_message
        except Exception as e:
            print(e)
            return error_message

        # If there's no rolls something went wrong. Return error message.
        if len(cleaned_rolls) < 1:
            return error_message

        # create roll output
        if self.roll_type == RollType.ADVANTAGE:
            self.__construct_advantage_output(cleaned_rolls)
        else:
            self.__construct_output_std(cleaned_rolls)

        try:
            results = [
                f'Roll Type: {self.roll_type.value}',
                f'Rolling: {"".join(cleaned_rolls)}',
                f'Rolled: {self.roll_dis_str}',
                f'Total: {eval(self.roll_eval_str)}'
            ]
            # log results
            print(results)
        except Exception as e:
            print(e)
            return error_message

        return results
