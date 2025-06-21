'''
This class will contain the Q table that will control the traffic lights
'''

import numpy as np
import random

from trafficLight import greenLightIndicator

class modelContainer:

    latestModelDecisionIndex = 0 #this will be needed while updating the Q-table using the Bellman equation.

    def __init__(self):

        self.qTable = np.zeros(3,3,3,3,2,2,2,2,4) 
        #note - worst case traffic will be when all 4 lanes have >70 cars, and all 4 lights are delayed for some reason (x2 penalty) - so (-560) is the lowest achievable score for the model.
        #we can construct positive rewards by subtracting the total traffic score along with delay penalties, from 600.
        '''
        Each of the 3's represents the 3 buckets of traffic (low, med, high) across the 4 different roads (L,R,T,B)

        Each of the 2's represents the delay index - has the timer on any one lane exceeded 3 mins (yes/no)

        The 4 corresponds to the action dimension - which lane will the model turn green - (L,R,T,B)

        '''
        pass


    def getModelDecision():
        pass


    def getRandomExploreDecisionByEpsilon(self, modelDecision): #modelDecision is also of type greenLightIndicator

        #decay the epsilon value of the active instance of the Q table container.
        if(self.epsilon > self.lowestEpsilon):
            self.epsilon = self.epsilon * self.epsilonDecay #reduce the probability of getting a random output

        #get a random float between 0 and 1. If that is less than epsilon, return a random decision, else return the model decision. 
        #Epsilon will decrease over time, so the probability of getting a random value lower than epsilon will also reduce
        if np.random.rand() < self.epsilon:
            return greenLightIndicator(random.randint(1,4))#including 1 and 4
        else:
            return modelDecision
    

