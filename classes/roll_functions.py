import random


class roller():

    def __init__(self):
        pass

    # async def single_roll(self, sides):
    #     return random.randint(1, sides)

    async def roll(self, dice_pool=1, sides=6):
        return [random.randint(1, sides) for _ in range(0, dice_pool)]
