# doskvolMasterGenerator.py
# A menu interface capable of calling the individual Doskvol generators

from . import buildings
from . import demons
from . import ghosts
from . import leviathans
from . import people
from . import streets
from . import cults
from . import scores


def main(generator: str):
    '''
        generator = input(
            """
Select generator:
[1]  Create common NPC
[2]  Create rare NPC
[3]  Create street description
[4]  Create common building description
[5]  Create rare building description
[6]  Create a demon
[7]  Create a ghost
[8]  Create a cult
[9]  Create a score
[10] Create a leviathan doing banal activity
[11] Create a leviathan doing surreal activity
[12] Create a leviathan spawn
[0] Quit

"""
'''
    if generator == "1":
        common_person = people.Person("common")
        description = common_person.describe()
        

    elif generator == "2":
        rare_person = people.Person("rare")
        description = rare_person.describe()
        

    elif generator == "3":
        random_street = streets.Street()
        description = random_street.describe()
        

    elif generator == "4":
        common_building = buildings.Building("common")
        description = common_building.describe()
        

    elif generator == "5":
        rare_building = buildings.Building("rare")
        description = rare_building.describe()
        

    elif generator == "6":
        random_demon = demons.Demon()
        description = random_demon.describe()
        

    elif generator == "7":
        random_ghost = ghosts.Ghost()
        description = random_ghost.describe()
        

    elif generator == "8":
        random_cult = cults.Cult()
        description = random_cult.describe()
        

    elif generator == "9":
        random_score = scores.Score()
        description = random_score.describe()
        

    elif generator == "10":
        random_leviathan = leviathans.Leviathan("banal")
        description = random_leviathan.describe()
        

    elif generator == "11":
        random_leviathan = leviathans.Leviathan("surreal")
        description = random_leviathan.describe()
        

    elif generator == "12":
        random_spawn = leviathans.LeviathanSpawn()
        description = random_spawn.describe()


    return description

if __name__ == "__main__":
    main("1")
