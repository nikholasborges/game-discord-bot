from numpy.random import randint


async def dice_calculator(message):
    values = message.upper().split('D')
    result = ''

    if int(values[1].strip()) > 20:
        return "dice faces invalid, max is 20"

    dice_numbers = int(values[0])
    dice_faces = int(values[1])

    calculated_values = randint(1, dice_faces, dice_numbers)

    for value in calculated_values:

        if value == 10 or value == 1:
            value = f'**{value}**'

        result += str(value) + '  '

    return result
