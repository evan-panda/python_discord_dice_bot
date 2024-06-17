from . import adventures

def mausritter_main(gen_choice: str):
    """mausritter generator"""
    generator_data = ''
    if gen_choice == "1":
        print('generating adventure seed:')
        adv = adventures.AdventureGenerator()
        generator_data = adv.get_adventure_seed()
    elif gen_choice == '2':
        print('generating hex details:')

    return generator_data


if __name__ == '__main__':
    adv = adventures.AdventureGenerator()
    adv.get_adventure_seed()
