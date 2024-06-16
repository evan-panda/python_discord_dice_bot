from . import adventures

def mausritter_main(generator: str):
    """mausritter generator"""
    generator_data = ''
    if generator == "1":
        print('generating adventure seed')
        adv = adventures.AdventureGenerator()
        generator_data = adv.get_adventure_seed()

    return generator_data


if __name__ == '__main__':
    adv = adventures.AdventureGenerator()
    adv.get_adventure_seed()
