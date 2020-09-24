"""""""""""""""""""""
    Nov 22, 2018
"""""""""""""""""""""

import random
import string
import numpy as np
import timeit

target = "Kusogaki"
dnaLength = len(target)
populationSize = 20
generations = 10000
mutationChance = 100


def randomGene():
    return random.choice(string.printable)


def initialPopulation():
    initPop = []
    for i in range(populationSize):
        initPop.append(''.join(random.choice(string.printable) for i in range(dnaLength)))
        return initPop


def fitnessFunction(competingDNA):
    fitness = 0
    for i in range(dnaLength):
        # Compare the results
        if competingDNA[i] != target[i]:
            fitness += 1
    if fitness != 0:
        fitness += 1
    return fitness


def mutation(competingDNA, mutationRatio):
    mutatedDNA = ""  # Create a empty string mutatedDNA
    dna_mutation = list(competingDNA)  # Transfer the empty string mutatedDNA into Array
    for i in range(len(competingDNA)):
        random_mutated_integer = random.choice(string.printable)  # Setup for random mutation integer
        mutation_chance = random.randint(1, mutationRatio)  # Setup for mutation chance
        if mutation_chance == 1:
            dna_mutation[i] = random_mutated_integer  # The integer at the position [i] will be mutated to a new integer
    mutatedDNA = ''.join(dna_mutation)  # Add the array back to the string
    return mutatedDNA


def recombination(competingDNA1, competingDNA2):
    y = random.randint(0, len(competingDNA1))  # Create a random integer y which split the DNA into 2 parts
    DNA1 = list(competingDNA1)  # Create Array DNA1 for further use
    DNA2 = list(competingDNA2)  # Create Array DNA2 for further use
    DNAout1 = ''.join(
        DNA1[0:y] + DNA2[y:len(competingDNA1)])  # Initialize the combination and add the array DNA1 back to the string
    DNAout2 = ''.join(
        DNA2[0:y] + DNA1[y:len(competingDNA1)])  # Initialize the combination and add the array DNA2 back to the string
    return DNAout1, DNAout2


def weightedDNAchoice(competingDNAfitnessPairs):
    probs = [competingDNAfitnessPairs[i][1] for i in range(len(competingDNAfitnessPairs))]
    probs = np.array(probs)
    probs /= probs.sum()
    return competingDNAfitnessPairs[np.random.choice(len(competingDNAfitnessPairs), 1, p=probs)[0]][0]


start_time = timeit.default_timer()
First = True
Second = True

currentPopulation = initialPopulation()

for i in range(generations):
    lastfitnessarray = []
    for k in currentPopulation:
        lastfitnessarray.append(fitnessFunction(k))

        # Print the generation number and its current fittest DNA string
        print("The fittest DNA for generation", i, "is ---",
              currentPopulation[lastfitnessarray.index(min(lastfitnessarray))], "--- with penalty:",
              min(lastfitnessarray))

        if min(lastfitnessarray) == 1 and First is True:
            stop_time1 = timeit.default_timer()
            First = False

        if min(lastfitnessarray) == 0 and Second is True:
            stop_time2 = timeit.default_timer()
            Second = False

        # Return a new population with their respective fitness is format
        # [ ["dnastr1", penalty1], ["dnastr2", penalty2], [...] ...]
    populationWeighted = []
    for individual in currentPopulation:
        individualPenalty = fitnessFunction(individual)
        if individualPenalty == 0:
            DNAfitnessPair = (individual, 1.0)
        else:
            DNAfitnessPair = (individual, 1.0 / individualPenalty)
        populationWeighted.append(DNAfitnessPair)

    # Reset population and repopulate with newly selected, recombined, and mutated DNA
    currentPopulation = []
    for m in range(int(populationSize / 2)):
        # Random selection, weighted by fitness. (higher fitness == higher probability)
        fittestDNA1 = weightedDNAchoice(populationWeighted)
        fittestDNA2 = weightedDNAchoice(populationWeighted)

        # Recombination or crossover
        fittestDNA1, fittestDNA2 = recombination(fittestDNA1, fittestDNA2)

        # Mutation in 1/mutationChance chances
        fittestDNA1 = mutation(fittestDNA1, mutationChance)
        fittestDNA2 = mutation(fittestDNA2, mutationChance)

        # Combining the population for next iteration
        currentPopulation.append(fittestDNA1)
        currentPopulation.append(fittestDNA2)

# Creates an array of penalty value for each DNA in population
lastfitnessarray = []
for g in currentPopulation:
    lastfitnessarray.append(fitnessFunction(g))

# Prints fittest DNA out of the resulting population
print("Fittest string at", generations, "is:", currentPopulation[lastfitnessarray.index(min(lastfitnessarray))])

if not First:
    print("It took " + str(stop_time1 - start_time)[0:5] + " seconds to reach 1 Penalty.")

if not Second:
    print("It took " + str(stop_time2 - start_time)[0:5] + " seconds to reach 0 Penalty.")
