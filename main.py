from random import Random
from time import time
import re
import inspyred

def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time())

    with open("16.txt") as file:
        lines = file.readlines()

    MAX_WEIGHT = int(lines[0].split(" ")[0])
    MAX_VALUE = int(lines[0].split(" ")[1])

    items = []

    i = 1
    while i<len(lines):
        items.append(([int(lines[i].split(" ")[0]), float(lines[i].split(" ")[1])], int(lines[i].split(" ")[2])))
        i=i+1

    file.close()

    problem = inspyred.benchmarks.Knapsack((MAX_WEIGHT, MAX_VALUE), items, duplicates=False)
    ac = inspyred.swarm.ACS(prng, problem.components)
    ac.terminator = inspyred.ec.terminators.generation_termination

    items2 = []
    reg = re.compile('[^0-9. ]')

    if display:
        best = max(ac.archive)
        for c in best.candidate:
            items2.append(reg.sub('', str(c)))
        print('Best Solution: {0}: {1}'.format(str(best.candidate),
                                               best.fitness))

    i = 0
    while i < len(items2):
        a = (([int(items2[i].split(" ")[0]), float(items2[i].split(" ")[1])], int(items2[i].split(" ")[2])))
        items2[i] = a
        i=i+1

    sum_weight = 0
    sum_volume = 0
    sum_value = 0
    for c in items2:
        sum_weight += c[0][0]
        sum_volume += c[0][1]
        sum_value += c[1]

    print(sum_value, sum_weight, sum_volume)

    indx = []
    for i in items2:
        indx.append(items.index(i)+1)

    print(sorted(indx))

    return ac

if __name__ == '__main__':
    main(display=True)
