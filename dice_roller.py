from random import randint
import re
from enum import Enum

## variables 
replaceCharsRegex = r'[\s\`\~\!\@\#\$\%\^\&\*\(\)\_\=\[\]\{\}\\\|\;\:\'\"\,\<\>\/\?]'
replaceChars = '`~!@#$%^&*)(_=][}{\\|;:\'",.></? \t\r\n'
confirmList = [
    'y', 'yes', 'yy', 'yees', 'yeees', 'yess', 'yis', 'yep',
    'yeah', 'yea', 'yay', 'ye', 'yee', 'yey', 'yup', 'yuup', 
    'uh-huh', 'uh huh', 'affirmative', 'confirm', 'check', ':)']

## regex checks 
checkSave = r'^(add|set|save)' # starts with set, save, or keep 
checkDel = r'^(delete|del|remove|destroy)' # start with delete, del, remove, or destroy 
checkRoll = r'([0-9]+[dD][0-9]+)' # check for xdx
checkValidBasic = r'(\d+\s*[+-]\s*)+|(\d+[dD]\d+)'
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
  ADVANTAGE=1
  DISADVANTAGE=2
  BEST=3
  WORST=4
  STANDARD=5

roll_type = RollType.STANDARD
## preset file name
# presetsFileName = 'presets.json'

## User Messages
# print("Welcome to my simple dice roller. To exit, type: 'end', 'exit', 'stop', or 'quit'.")
# print('This dice roller will roll values for any dice entered as the formula: <num>d<num>')
# print('It can also handle basic formulas such as; adding multiple dice rolls together, and adding or subtracting modifiers.')
# print("Type 'help' for examples and additional features.")
help_message = """
Input Examples:
  roll 1d20+4
  roll 1d20 + 6 + 2d4
  roll 2d6 + 3
"""

helpMessage = """
    Input Examples:
        roll 1d20+4
        roll 1d20 + 6 + 2d4
        roll 2d8 + 3
    Saving preset commands:
        Type 'add', 'set', or 'save'; then the name of the preset; then the roll associated with it.
        After it is saved, you can use the preset by just typing the name of it.
        Example save:
            set atk 1d20+5
            save bless atk 1d20 + 4 + 1d4
            keep dmg 1d8 + 3
        Example use:
            atk<press enter> - it will roll the preset value.
            rolld20 - is a default preset you can try
    Deleting a preset:
        Type 'delete', 'del', 'destroy', or 'remove'; then the name of the preset
        Enter confirmation, 'y', when asked. It will be removed from your presets file.
    """

"""
## gets data from file or creates default data if file doesn't exist
def readPresetsFile(fileName):
    if path.exists(fileName):
        with open(fileName, mode='r') as pFile:
            presetsData = json.load(pFile)
    else:
        with open(fileName, mode='w') as pFile:
            default = {
                "presets": [
                    {
                        "name": "rolld20",
                        "roll": "1d20"
                    }
                ]
            }
            json.dump(default, pFile, indent=4)

        with open(fileName, mode='r') as pFile:
            presetsData = json.load(pFile)
            
    return presetsData
"""

## Dice rolling
def rollDice(dice_roll):
  # get number of dice and dice sides
  dr = re.split('[dD]', dice_roll, maxsplit=2)
  num_dice = int(dr[0])
  sides = int(dr[1])

  if roll_type != RollType.STANDARD:
    num_dice += 1
  
  rolls = []
  for i in range(num_dice):
      rolls.append(randint(1, sides))

  return rolls

## deciding to add positive or negative number
def addItems(sign, num):
    if type(num) is list:
        num = sum(num)

    if sign == '-':
        return num * -1

    return num


def cleanRollInput(rollInput):
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


def constructOutput(rollInput):
  """construct output and get total roll"""
  total = 0 # total number rolled +/- others
  output = [] # output string list
  for indx, item in enumerate(rollInput):
      if indx > 0:
          sign = rollInput[indx - 1]
      else:
          sign = '+'
      
      if re.match(checkRoll, item) is not None:  # is dice roll (xdx) 
          item = rollDice(item)
          total += addItems(sign, item)

          output.append('(')
          for i, val in enumerate(item):
              if i == (len(item) - 1):
                  output.append(str(val))
              else:
                  output.append(str(val) + ' + ')
          output.append(') ')
      elif re.search(checkMod, item) is not None:  # is modifier (+/-)
          output.append(item + ' ')
      elif re.match(checkDigits, item) is not None:  # is digit (0-9)
          output.append(item + ' ')
          item = int(item)
          total += addItems(sign, item)
  
  return [output, total]

"""
## check for existing preset and/or save the new preset
def savePreset(userIn):
    # get preset name and value 
    startName = re.match(checkSave, userIn).end()
    endName = re.search(checkValidBasic, userIn).start()
    presetName = userIn[startName:endName].strip(replaceChars)
    print(f'preset name: {presetName} ')
    cleanedRolls = cleanRollInput(userIn[endName:])
    newPreset = {
        "name": presetName,
        "roll": ''.join(cleanedRolls)
    }

    if len(cleanedRolls) > 0 and len(presetName) > 0:
        # check if the preset exists and ask if it should be updated
        existsFlag = False
        for pre in presetsData["presets"]:
            if newPreset["name"] == pre["name"]:
                existsFlag = True
                print(f'Preset already exists: {pre["name"]}')
                print(f'Would you like to update the value from <{pre["roll"]}> to <{newPreset["roll"]}> ?')
                confirmUpdate = input('(y/n) ')
                confirmUpdate = confirmUpdate.strip(replaceChars).lower()
                if confirmUpdate in confirmList:
                    print(f'Updated the preset: {pre["name"]}\n From: {pre["roll"]} | To: {newPreset["roll"]}')
                    pre["roll"] = newPreset["roll"]
                    with open(presetsFileName, mode='w') as pFile:
                        json.dump(presetsData, pFile, indent=4)
                else:
                    print(f'Did not update existing preset: {pre["name"]}, value: {pre["roll"]}')
        # save new preset, use flag to see if it found an existing one.
        if not existsFlag:
            presetsData["presets"].append(newPreset)
            with open(presetsFileName, mode='w') as pFile:
                json.dump(presetsData, pFile, indent=4)
            print(f'Preset added: {newPreset["name"]}, value: {newPreset["roll"]}')
        
        readPresetsFile(presetsFileName) # update presets list in memory
    else:
        print('Invalid preset; not saved. Preset must have name and valid roll.')


## delete existing preset
def deletePreset(userIn, presetsData):
    print('--- deleting preset ---')
    start = re.match(checkDel, userIn).end()
    presetName = userIn[start:]
    presetName = presetName.strip(replaceChars).lower()
    presetFound = False
    for i, pre in enumerate(presetsData["presets"]):
        if presetName == pre["name"]:
            presetFound = True
            print(f'Are you sure you want to delete the preset: {pre["name"]} ?')
            userCon = input(f'Name: {pre["name"]}, Value: {pre["roll"]} Delete? (y/n) ')
            if userCon in confirmList:
                del presetsData["presets"][i]
                print(f'Preset {pre["name"]} deleted.')

                with open(presetsFileName, mode='w') as pFile:
                    json.dump(presetsData, pFile, indent=4)
                    
                presetsData = readPresetsFile(presetsFileName)
            else:
                print('Did not delete the preset.')
    
    if not presetFound:
        print(f'No preset found matching name: "{presetName}"\nPlease try again.') 
"""
## get presets 
# presetsData = readPresetsFile(presetsFileName)

## app loop
def handle_rolls(userIn: str):
  """Performs some checks and returns final output"""
  cleanedRolls = [] # set default empty rolls list
  ## user input 
  # userIn = input('\nEnter dice roll (#d# +/- <modifiers>): ')
  userIn = userIn.strip(replaceChars).lower()

  if userIn.startswith('help'):
    return help_message
  elif userIn.startswith('-'):
    userIn = userIn[1:]

  if re.match(checkValidBasic, userIn): # see if it's a basic roll 
    cleanedRolls = cleanRollInput(userIn)
  else:
    ## check for presets
    presetFound = False
    #for pre in presetsData["presets"]:
    #    if userIn == pre["name"]:
    #        presetFound = True 
    #        cleanedRolls = cleanRollInput(pre["roll"])

    ## if no presets were found this will occur, or will skip if there are numbers in the input

  if len(cleanedRolls) < 1:
    print(f'"{userIn}" is not valid. Please try again.')
    return f'"{userIn}" is not recognized as valid. Please try again.'

  output = constructOutput(cleanedRolls) 

  ## print results
  print(f'Rolling: {"".join(cleanedRolls)}') 
  print(f'Rolled: {"".join(output[0])}') 
  print(f'Total: {str(output[1])}') 

  return [
    f'Rolling: {"".join(cleanedRolls)}',
    f'Rolled: {"".join(output[0])}',
    f'Total: {str(output[1])}'
  ]
