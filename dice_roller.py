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
check_roll = r'([0-9]*[dD][0-9]+)'  # check for xdx, or just dx
check_valid_basic = r'(\d+\s*[+-]\s*)+|(\d*[dD]\d+)'
check_mod = r'(\s*[+-]\s*)'  # find +/- symbols
check_double_plus = r'(\s*[+]\s*){2,}'  # find 2 or more +/- in a row
check_double_minus = r'(\s*[-]\s*){2,}'  # find 2 or more +/- in a row
check_invalid_chars = r'(?:(?![dD0-9+\-])[\x20-\x7e])+'  # check for everything that isn't a number or 'd' or +/-


class RollType(Enum):
    ADVANTAGE = 'Advantage'        # +1d, drop lowest
    DISADVANTAGE = 'Disadvantage'  # +1d, drop highest
    BEST = 'Best'                  # keep single best
    WORST = 'Worst'                # keep single worst
    POOL = 'Pool'                  # roll dice pool(s), keep single highest
    DROPLOWEST = 'Drop Lowest'     # drop lowest value
    DROPHIGHEST = 'Drop Highest'   # drop lowest value
    STANDARD = 'Standard'          # roll normally


help_message = """
Input Examples:
    1d20
    1d100
    1d20+4
    1d20 + 6 + 2d4
    2d6 - 1
Roll types are:
    Standard - rolls all dice as normal
    Advantage - rolls +1d to first die, drops lowest
    Disadvantage rolls +1d to first die, drops highest
    Best - takes highest value from first dice group
    Worst - takes lowest value from first dice group
    Pool - takes highest value from all dice groups
    Drop Lowest - drops lowest value from first dice group
    Drop Highest - drops highest value from first dice group
"""


class DiceRoller():
    def __init__(self) -> None:
        self.special_flag = True
        self.roll_eval_str = ""
        self.roll_dis_str = ""
        self.roll_type = RollType.STANDARD

    def __get_num_and_sides(self, raw_roll) -> tuple:
        """get number of dice, and dice sides"""
        num_dice, sides = re.split(r'[dD]', raw_roll, maxsplit=2)
        num_dice, sides = int(num_dice if num_dice else '1'), int(sides)

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
        user_rolls = re.split(check_mod, strip_double_mods)

        cleaned_rolls = []
        for item in user_rolls:
            if len(re.findall(r'[dD]', item)) > 1:  # check for multiple "d's" in the roll
                raise InvlidRollFormatException(roll_input)
            elif re.findall(check_invalid_chars, item):  # check of other invalid characters
                raise InvlidRollFormatException(roll_input)

            cleaned_rolls.append(item)
        return cleaned_rolls

    def __roll_dis_advantage(self, num_dice, sides) -> tuple:
        """
        Rolling with dis/advantage.
          Add +1d to first die rolled and drop the lowest or highest result.
        """
        self.special_flag = False
        display_str = ""
        eval_str = ""
        num_dice += 1

        # get list of roll values [int]
        roll_values = self.roll_dice(num_dice, sides)

        # get highest roll for disadvantage, or lowest roll for advantage
        highlow_val = 0
        if self.roll_type == RollType.ADVANTAGE:
            highlow_val = min(roll_values)
        elif self.roll_type == RollType.DISADVANTAGE:
            highlow_val = max(roll_values)

        # put roll values into the display string
        adv_indx = -1
        display_str += '('
        for i, n in enumerate(roll_values):
            # find lowest/highest value, print crossed out in message
            if adv_indx < 0 and n == highlow_val:
                adv_indx = i
                # cross out lowest/highest value
                display_str += f'*~~ {str(n)} ~~*'
            else:
                display_str += f'{str(n)}'

            # add "+" if not the last element
            if i < (len(roll_values) - 1):
                display_str += '+'
        display_str += ')'

        roll_values.remove(highlow_val)
        eval_str += '(' + '+'.join([str(n) for n in roll_values]) + ')'

        return display_str, eval_str

    def __roll_best_worst(self, num_dice: int, sides: int) -> tuple:
        """
        Get best/worst value from first set rolled
        """
        self.special_flag = False
        display_str = ""
        eval_str = ""

        # get list of roll values [int]
        roll_values = self.roll_dice(num_dice, sides)

        # get lowest/highest rolled value
        if self.roll_type == RollType.BEST:
            bw_val = max(roll_values)
        elif self.roll_type == RollType.WORST:
            bw_val = min(roll_values)

        # put roll values into the display string
        bw_indx = -1
        display_str += '('
        for i, n in enumerate(roll_values):
            # find value, print in message
            if bw_indx < 0 and n == bw_val:
                bw_indx = i
                display_str += f'{str(n)}'
            else:
                # other values crossed out
                display_str += f'*~~ {str(n)} ~~*'

            # add "," if not the last element
            if i < (len(roll_values) - 1):
                display_str += ','
        display_str += ')'

        # add only best/worst value to eval str
        eval_str += f'({bw_val})'

        return display_str, eval_str

    def __roll_pool(self, num_dice, sides):
        """
        Get best die when rolling
        """
        display_str = ""
        eval_str = ""

        highest_flag = -1

        # get list of roll values [int]
        roll_values = self.roll_dice(num_dice, sides)

        # get highest rolled value
        best_val = max(roll_values)

        # put roll values into the display string
        display_str += '('
        for i, n in enumerate(roll_values):
            # find value, print in message
            if n == best_val and highest_flag < 0:
                highest_flag = i
                # bold value
                display_str += f'{str(n)}'
            else:
                # cross out value
                display_str += f'*~~ {str(n)} ~~*'

            # add "," if not the last element
            if i < (len(roll_values) - 1):
                display_str += ','
        display_str += ')'

        # add only highest value to eval str
        eval_str += f'({best_val})'

        return display_str, eval_str

    def __roll_drop_high_low(self, num_dice, sides) -> tuple:
        """
        Drop the highest or lowest value when rolling the first die(dice)
        """
        self.special_flag = False
        display_str = ""
        eval_str = ""

        # get list of roll values [int]
        roll_values = self.roll_dice(num_dice, sides)

        # get highest roll for disadvantage, or lowest roll for advantage
        highlow_val = 0
        if self.roll_type == RollType.DROPLOWEST:
            highlow_val = min(roll_values)
        elif self.roll_type == RollType.DROPHIGHEST:
            highlow_val = max(roll_values)

        # put roll values into the display string
        adv_indx = -1
        display_str += '('
        if len(roll_values) > 1:
            for i, n in enumerate(roll_values):
                # find lowest/highest value, print crossed out in message
                if adv_indx < 0 and n == highlow_val:
                    adv_indx = i
                    # cross out lowest/highest value
                    display_str += f'*~~ {str(n)} ~~*'
                else:
                    display_str += f'{str(n)}'

                # add "+" if not the last element
                if i < (len(roll_values) - 1):
                    display_str += '+'
        else:
            display_str += str(roll_values[0])
        display_str += ')'

        if len(roll_values) > 1:
            roll_values.remove(highlow_val)
        eval_str += '(' + '+'.join([str(n) for n in roll_values]) + ')'

        return display_str, eval_str

    def __construct_output(self, roll_input) -> list:
        """construct output and get total roll"""
        # standard roll
        for indx, item in enumerate(roll_input):
            # check for dice roll (xdx), else just add to display/eval strings
            if re.match(check_roll, item) is not None:
                # get number of dice, and dice sides
                num_dice, sides = self.__get_num_and_sides(item)
                display_str = ""
                eval_str = ""

                if self.roll_type == RollType.STANDARD or not self.special_flag:
                    # get list of roll values [int]
                    roll_values = self.roll_dice(num_dice, sides)

                    display_str = '(' + '+'.join([str(n) for n in roll_values]) + ')'
                    eval_str = '(' + '+'.join([str(n) for n in roll_values]) + ')'
                elif self.roll_type == RollType.ADVANTAGE or self.roll_type == RollType.DISADVANTAGE:
                    display_str, eval_str = self.__roll_dis_advantage(num_dice, sides)
                elif self.roll_type == RollType.DROPHIGHEST or self.roll_type == RollType.DROPLOWEST:
                    display_str, eval_str = self.__roll_drop_high_low(num_dice, sides)
                elif self.roll_type == RollType.BEST or self.roll_type == RollType.WORST:
                    display_str, eval_str = self.__roll_best_worst(num_dice, sides)
                elif self.roll_type == RollType.POOL:
                    display_str, eval_str = self.__roll_pool(num_dice, sides)

                # add values to output
                self.roll_dis_str += display_str
                self.roll_eval_str += eval_str
            else:
                self.roll_dis_str += item
                self.roll_eval_str += item

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
        elif r_type.startswith('l'):
            self.roll_type = RollType.DROPLOWEST
        elif r_type.startswith('h'):
            self.roll_type = RollType.DROPHIGHEST

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
        self.__construct_output(cleaned_rolls)

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
            print(f'ERROR: Something went wrong with input: {user_in} . . .\nSee exception output below.')
            print(e)
            return error_message

        return results
