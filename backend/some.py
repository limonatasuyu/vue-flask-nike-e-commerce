import random

def randomSizes():
    sizes = ['35', '36', '37', '38', '39', '40', '41', '42', '43', '44'] 

    tempSizes = sizes
    random_sizes = []
    random_sizes_length = random.choice(range(len(sizes)))
    if random_sizes_length <= 9:
        random_sizes_length += 1
    for i in range(random_sizes_length):
        randomSize = random.choice(tempSizes)
        random_sizes.append(randomSize)
        tempSizes.remove(randomSize)
    
    random_sizes.sort()
    return ', '.join(random_sizes)
