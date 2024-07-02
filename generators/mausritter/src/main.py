from .adventures import AdventureGenerator

def mausritter_main(gen_choice: str):
    """mausritter generator"""
    generator_data = ''
    if gen_choice == '1':
        print('generating adventure seed:')
        adv = AdventureGenerator()
        generator_data = adv.get_adventure_seed()
    elif gen_choice == '2':
        print('generating hex details:')
    else:
        generator_data = f'received unexpected input: {gen_choice}'
        print('unexpected input')

    return generator_data


if __name__ == '__main__':
    adv = AdventureGenerator()
    adv.get_adventure_seed()
