from .gen_spell import RandomMagic
from .gen_pc import RandomPC


PROMPT = """
What would you like to generate?
[1] Spell Name - by the book
[2] Spell Name - random
[3] Character Details
[4] Character Items
[x] To Quit

"""


def main(choice: str, local_run: bool = False) -> None:
    while choice.isnumeric():
        if local_run:
            choice = input(PROMPT)

        description = ''

        magic = RandomMagic()
        pc = RandomPC()

        if choice == '1':
            description = magic.get_random_spell(by_the_book=True)
            if local_run:
                print('\n' + description, end='\n\n')
        elif choice == '2':
            description = magic.get_random_spell(by_the_book=False)
            if local_run:
                print('\n' + description, end='\n\n')
        elif choice == '3':
            description = pc.describe_pc()
            if local_run:
                print('\n' + description, end='\n\n')
        elif choice == '4':
            description = pc.describe_pc_items()
            if local_run:
                print('\n' + description, end='\n\n')
        else:
            description = f'Your choice of "{choice}" was not recognized as a valid option.'
            if choice.isnumeric() and local_run:
                print(
                    f'Your choice of "{choice}" was not recognized as an option.'
                    '\nPlease try again, or enter "x" to quit.'
                )
            elif local_run:
                print('Exiting...')

        if not local_run:
            return description

    if local_run:
        print('The choice was not numeric')
    return 'The choice was not numeric'


if __name__ == '__main__':
    main('1', local_run=True)
