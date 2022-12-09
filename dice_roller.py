from random import randint
import re
from enum import Enum

# variables 
replaceCharsRegex = r'[\s\`\~\!\@\#\$\%\^\&\*\(\)\_\=\[\]\{\}\\\|\;\:\'\"\,\<\>\/\?]'
replaceChars = '`~!@#$%^&*)(_=][}{\\|;:\'",.></? \t\r\n'

# regex checks 
checkSave = r'^(add|set|save)' # starts with set, save, or keep 
checkDel = r'^(delete|del|remove|destroy)' # start with delete, del, remove, or destroy 
checkRoll = r'([0-9]+[dD][0-9]+)' # check for xdx
check_valid_basic = r'(\d+\s*[+-]\s*)+|(\d+[dD]\d+)'
checkMod = r'(\s*[+-]\s*)' # find +/- symbols
checkDoublePlus = r'(\s*[+]\s*){2,}' # find 2 or more +/- in a row
checkDoubleMinus = r'(\s*[-]\s*){2,}' # find 2 or more +/- in a row
checkDigits = r'^\d+$' # check for only digits
checkQuit = r'^(end|exit|stop|quit|zxcv)' # starts with quit, exit, or stop
checkHelp = r'^(help|\-h)' # check for the word 'help'
checkInvalidChars = r'(?:(?![dD0-9+\-])[\x20-\x7e])+' # check for everything that isn't a number or 'd' or +/-
"""Checking for optional modifiers
rh = help
ra = advantage
rb = best
rd = disadvantage
rw = worst
"""


class RollType(Enum):
  ADVANTAGE=1     # +1d, drop lowest
  DISADVANTAGE=2  # +1d, drop highest
  BEST=3          # keep single best
  WORST=4         # keep single worst
  STANDARD=5      # roll normally


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
        self.roll_list = []
        self.roll_type = RollType.STANDARD


    def roll_dice(self, dice_roll) -> list[int]:
        """Roll dice. With number of dice and dice sides"""
        num_dice, sides = re.split('[dD]', dice_roll, maxsplit=2)
        num_dice, sides = int(num_dice), int(sides)

        # if self.roll_type == RollType.ADVANTAGE or self.roll_type == RollType.DISADVANTAGE:
        #     num_dice += 1

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


    def __clean_roll_input(self, rollInput) -> list:
        """get list of various rolls and modifiers"""
        stripDoubleMods = re.sub(checkDoublePlus, '+', rollInput)
        stripDoubleMods = re.sub(checkDoubleMinus, '-', stripDoubleMods)
        userRolls = re.split(checkMod, stripDoubleMods)
        
        cleanedRolls = []
        for item in userRolls:
            item = item.strip(replaceChars)
            if len(re.findall(r'[dD]', item)) > 1:  # check for multiple "d's" in the roll
                cleanedRolls = []
                return cleanedRolls
            elif re.findall(checkInvalidChars, item):  # check of other invalid characters
                cleanedRolls = []
                return cleanedRolls

            cleanedRolls.append(item)
        return cleanedRolls


    def __construct_output_std(self, rollInput) -> list:
        """construct output and get total roll"""
        total = 0 # total number rolled +/- others
        output = [] # output string list
        for indx, item in enumerate(rollInput):
            if indx > 0:
                sign = rollInput[indx - 1]
            else:
                sign = '+'
            
            if re.match(checkRoll, item) is not None:  # is dice roll (xdx) 
                item = self.roll_dice(item)
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


    def __get_roll_type(self, r_type:str):
        """Chooses proper enum for given roll type"""
        if r_type.startswith('a'):
            self.roll_type = RollType.ADVANTAGE
        elif r_type.startswith('d'):
            self.roll_type = RollType.DISADVANTAGE
        elif r_type.startswith('b'):
            self.roll_type = RollType.BEST
        elif r_type.startswith('w'):
            self.roll_type = RollType.WORST


    def __construct_advantage_output(self, user_in: str):
        """
        Rolling with advantage.
          Add +1d to first die rolled and drop the lowest result.
        """
        # TODO implement advantage rolls starting here
        pass

    def handle_rolls(self, user_in: str, r_type: str = 's') -> (str | list[str]):
        """Performs some checks and returns final output"""
        cleaned_rolls = [] # set default empty rolls list
        
        self.__get_roll_type(r_type.lower())

        user_in = user_in.strip(replaceChars).lower()

        if user_in.startswith('help'):
            return help_message
        elif user_in.startswith('-'):
            user_in = user_in[1:]

        if re.match(check_valid_basic, user_in): # see if it's a valid roll 
            cleaned_rolls = self.__clean_roll_input(user_in)

        if len(cleaned_rolls) < 1:
            print(f'"{user_in}" is not valid. Please try again.')
            return f'"{user_in}" is not recognized as a valid roll input. Please try again with something like, "2d6" or "1d20+2+1d4"'

        output = self.__construct_output_std(cleaned_rolls)

        if self.roll_type == RollType.ADVANTAGE:
            adv_output = self.__construct_advantage_output(cleaned_rolls)

        ## print results
        print(
            f'Rolling: {"".join(cleaned_rolls)}'
            f'Rolled: {"".join(output[0])}'
            f'Total: {eval("".join(output[0]))}'
        )

        return [
            f'Rolling: {"".join(cleaned_rolls)}',
            f'Rolled: {"".join(output[0])}',
            f'Total: {str(output[1])}'
        ]
