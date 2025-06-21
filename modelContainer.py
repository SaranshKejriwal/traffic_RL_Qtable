'''
This class will contain the Q table that will control the traffic lights
'''

import numpy as np
import random
from road import roadIdentifier


class modelContainer:

    epsilon = 1 #start with randomly exploring all possibilities and decay the randomness
    epsilonDecay = 0.99995 #epsilon will reduce by a geometric progression of 0.995, not an arithmetic progression like before.
    #Note that a decay factor of 0.9995 drops to <1% in just 10k iterations, 
    #This means that the snake will end up spinning in circles because that's the only path discovered.
    
    lowestEpsilon = 0.01 #lower threshold for randomness

    alpha = 0.9 #used to update the new Q values.     
    gamma = 0.75 #discount factor

    latestModelDecisionIndex = 0 #this will be needed while updating the Q-table using the Bellman equation.

    def __init__(self):

        self.qTable = np.zeros([3,3,3,3,2,2,2,2,4,3]) 
        #note - worst case traffic will be when all 4 lanes have >70 cars, and all 4 lights are delayed for some reason (x2 penalty) - so (-560) is the lowest achievable score for the model.
        #we can construct positive rewards by subtracting the total traffic score along with delay penalties, from 600.
        '''
        Each of the 3's represents the 3 buckets of traffic (low, med, high) across the 4 different roads (L,R,T,B)

        Each of the 2's represents the delay index - has the timer on any one lane exceeded 3 mins (yes/no)

        The 4 corresponds to the action dimension 1 - which lane will the model turn green - (L,R,T,B)
        The 3 corresponds to the action dimension 2 - what will be the duration of that green light - 0(30s), 1(60s) or 2(90s)

        '''
        pass


    def getModelDecision(self, stateVector):

        #Directly pass the vector as an index to the table and get a 2D array of possible actions
        qTableRewardSection = np.array(self.qTable[tuple(stateVector)]) #this will be a 4x3 array


        chosenRoadIndex, chosenDurationIndex = np.unravel_index(qTableRewardSection.argmax(), qTableRewardSection.shape) #get 2 indices across the 2D array,wherever the max reward is located.

        #print('chosenRoad:',chosenRoadIndex,'; chosenDuration:',chosenDurationIndex)

        #latestModelDecisionIndex will be referred later when the Q table is being updated.
        #Note that because of epsilon, the model will be more likely to explore and update multiple Q-values for the future.

        return self.getRandomExploreDecisionByEpsilon(chosenRoadIndex, chosenDurationIndex)



    def getRandomExploreDecisionByEpsilon(self, chosenRoadIndex, chosenDurationIndex): #modelDecision is also of type greenLightIndicator

        #decay the epsilon value of the active instance of the Q table container.
        if(self.epsilon > self.lowestEpsilon):
            self.epsilon = self.epsilon * self.epsilonDecay #reduce the probability of getting a random output

        #get a random float between 0 and 1. If that is less than epsilon, return a random decision, else return the model decision. 
        #Epsilon will decrease over time, so the probability of getting a random value lower than epsilon will also reduce
        if np.random.rand() < self.epsilon:
            return (random.randint(0,3)) , random.randint(0,2) #select a random road out of 4 and a random duration out of 3 options.
            #randint includes 0 and 3
        else:
            return chosenRoadIndex, chosenDurationIndex
    

