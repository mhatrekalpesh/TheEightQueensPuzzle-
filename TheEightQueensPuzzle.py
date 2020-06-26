#!/usr/bin/env python

import random
import pandas as pd


# Intiate global parameters

totalPopulation = 50                  #this is count of generations in all the population

mutationRate = 0.9                    #this is the percentage of times mutation happens

crossOver = 0.5                       #this is the crossover point percentage

target = [0,3,4,5,6,1,2,4]            #this is the target sequence

numberList = [0,1,2,3,4,5,6,7]        #this is the list of valid positions

topParentsRate = 0.5                  #this is the rate of top parents used for generation of next population

populationData = []                   #this is list for all the population
fitnessData = []                      #this is list for all the population's fitness data
    

# function to populate intial pool of randomly generated sequences
def PopulateIntialPool(totalPopulation):
    for outloop in range(totalPopulation):
        randomData = []
        for inloop in range(len(target)):
            selectedData = random.choice(numberList)
            randomData.append(selectedData)
        fitnessScore = getFitnessScore(randomData)
        populationData.append(randomData)
        fitnessData.append(fitnessScore)
    probDataFrame = pd.DataFrame({'Sequence':populationData,'FitnessScore':fitnessData})
    probDataFrame = probDataFrame.sort_values(['FitnessScore'],ascending=False)
    probDataFrame = probDataFrame.reset_index(drop=True)
    return probDataFrame


# function to get the fitness score of a sequence
def getFitnessScore(data):
    fitnessScore = 0
    for inloop in range(len(target)):
        if (data[inloop] == target[inloop]):
            fitnessScore = fitnessScore + 1
    return fitnessScore


# function to get crossover sequence of the given 2 sequences
def getCrossOver(parent1,parent2):
    crossOverPoint = int(crossOver*len(target))
    child = parent1[0:crossOverPoint]+parent2[crossOverPoint:]
    return child


# function to make a mutation to the sequnce based on mutationRate
def getMutation(sequence):
    if random.randint(0,100)/100 < mutationRate:
        sequence[random.randint(0,len(target)-1)] = random.choice(numberList)
    return sequence


# function to generate new pool with crossover and mutated child sequences
# for top fitness parents
def generateNewPool(probDataFrame):
    populationData = []
    fitnessData = []
    for outloop in range(totalPopulation):
        numberOfTopParents = int(topParentsRate*totalPopulation)
        randomParent1 = random.randint(0,numberOfTopParents-1)
        parent1 = probDataFrame[randomParent1:]["Sequence"].values[0]
        randomParent2 = random.randint(0,numberOfTopParents-1)
        parent2 = probDataFrame[randomParent2:]["Sequence"].values[0]
        child = getCrossOver(parent1,parent2)
        child = getMutation(child)
        populationData.append(child)
        fitnessData.append(getFitnessScore(child))
    probDataFrame = pd.DataFrame({'Sequence':populationData,'FitnessScore':fitnessData})
    probDataFrame = probDataFrame.sort_values(['FitnessScore'],ascending=False)
    probDataFrame = probDataFrame.reset_index(drop=True)
    return probDataFrame


# Main Code

#get intial set of sequences
probDataFrame = PopulateIntialPool(totalPopulation)

#limit the loop to generationCount
generationCount = 1000

for generation in range(generationCount):
    #get the best sequence in current generation
    bestSequence = probDataFrame[0:1]["Sequence"].values[0]
    #get the fitness score for the best sequence in current generation
    bestFitnessScore = probDataFrame[0:1]["FitnessScore"].values[0]
    #print the best sequence by fitness in current generation
    print('Generation : ',generation,
          ', Best Fitness Score : ',bestFitnessScore,
          ', Best Sequence : ', bestSequence)
    if (bestFitnessScore == len(target)):
        break
    #get next generation of sequences
    probDataFrame = generateNewPool(probDataFrame)
    