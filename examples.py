from entity import *

### XOR EXAMPLE ###

class XOR(Entity):

    def calc_fitness(self):
        error = 0
        error += (self.think([0,0])[0])
        error += (1 - self.think([0,1])[0])
        error += (1 - self.think([1,0])[0])
        error += (self.think([1,1])[0])
        score = 4 - error
        self.fitness = score**2

def xor_assessment(e):
    correct = 0
    if e.think([0,0])[0] < 0.5: correct += 1
    if e.think([0,1])[0] > 0.5: correct += 1
    if e.think([1,0])[0] > 0.5: correct += 1
    if e.think([1,1])[0] < 0.5: correct += 1
    if correct == 4:
        return True
    return False

class DIGITS(Entity):

    ''' Digit Display
    |-6-|
    1   5
    |-7-|
    2   4
    |-3-|
    '''
    
    NUMS = [
        [1,1,1,1,1,1,0],
        [0,0,1,0,0,1,1],
        [0,1,1,0,1,1,1],
        [0,0,1,1,1,1,1],
        [1,0,0,1,1,0,1],
        [1,0,1,1,0,1,1],
        [1,1,1,1,0,1,1],
        [0,0,0,1,1,1,0],
        [1,1,1,1,1,1,1],
        [1,0,1,1,1,1,1],
    ]

    def calc_fitness(self):
        error = 0

        for i in range(len(DIGITS.NUMS)):
            error += (1 - self.think(DIGITS.NUMS[i])[i])**2
            for j in range(len(DIGITS.NUMS)):
                if j != i:
                    error += (self.think(DIGITS.NUMS[i])[j])**2

        score = len(DIGITS.NUMS)**2 - error
        self.fitness = score**2

def digits_assessment(e):
    correct = 0

    for i in range(len(DIGITS.NUMS)):
        if e.think(DIGITS.NUMS[i])[i] > 0.5: correct += 1
        for j in range(len(DIGITS.NUMS)):
            if j != i and e.think(DIGITS.NUMS[i])[j] < 0.5: correct += 1
        
    if correct == len(DIGITS.NUMS)**2:
        return True
    if correct > 95:
        print("good")
    print(correct)
    return False
