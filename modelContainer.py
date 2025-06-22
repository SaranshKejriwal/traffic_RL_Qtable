'''
This class will contain the Q table that will control the traffic lights
'''

import numpy as np
import random
from road import road


class modelContainer:

    epsilon = 1 #start with randomly exploring all possibilities and decay the randomness
    epsilonDecay = 0.995 #epsilon will reduce by a geometric progression of 0.995, not an arithmetic progression like before.
    #Note that a decay factor of 0.9995 drops to <1% in just 10k iterations, 
    #This means that the snake will end up spinning in circles because that's the only path discovered.
    
    lowestEpsilon = 0.001 #lower threshold for randomness

    alpha = 0.9 #used to update the new Q values.     
    gamma = 0.6 #discount factor

    latestChosenRoadIndex = 0 #these will be needed while updating the Q-table using the Bellman equation.
    latestChosenDurationIndex = 0 

    def __init__(self):

        self.qTable = np.ones([3,3,3,3,2,2,2,2,4,3]) * (-2000)
        #all rewards are negative, so the Q table cannot be initialized with zeros

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

        #save these values to reuse them while updating the Q table.
        self.latestChosenRoadIndex, self.latestChosenDurationIndex = np.unravel_index(qTableRewardSection.argmax(), qTableRewardSection.shape) #get 2 indices across the 2D array,wherever the max reward is located.

        #latestModelDecisionIndex will be referred later when the Q table is being updated.
        #Note that because of epsilon, the model will be more likely to explore and update multiple Q-values for the future.

        return self.getRandomExploreDecisionByEpsilon(self.latestChosenRoadIndex, self.latestChosenDurationIndex)

    #this is supposed to be the IMPORTANT function which will update the reward values in the table, 
    #the reward value update will be as per the random explorations that the snake is able to do, AND for different locations of the food
    def updateQTable(self, currentStateVector, nextStateVector, chosenRoadIndex, chosenDurationIndex, rewardFromDecision):
        #modelContainer instance will be calling this function, once the decision is taken.

        #took an action given a state. We use this to update the QValue, if initialized at 0, using Bellman equation.
        oldQValue = self.qTable[tuple(currentStateVector)][self.latestChosenRoadIndex][self.latestChosenDurationIndex]

        #print(self.qTable[tuple(nextStateVector.astype(int))])
        nextStateMaxReward = np.max(self.qTable[tuple(nextStateVector.astype(int)), :]) 

        #update the Q table of the current state using the Bellman equation:
        self.qTable[tuple(currentStateVector)][self.latestChosenRoadIndex][self.latestChosenDurationIndex] = (1 - self.alpha) * oldQValue + self.alpha *(rewardFromDecision + self.gamma * nextStateMaxReward)


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
    

    def calculateRewardBetweenStates(self, prevState, currentState):

        #penalty is defined by the total number of vehicles based on the traffic category, and also considering a wait time multiplier.
        prevStatePenalty = 0
        currentStatePenalty = 0
        for i in range(4): #there will always be 4 roads, so this isn't a magic number
            prevStatePenalty += self.calculatePenaltyOfRoadByStateAndDelays(prevState[i], prevState[i+4]) #the next 4 values in state contain the delay values
            currentStatePenalty += self.calculatePenaltyOfRoadByStateAndDelays(currentState[i], currentState[i+4])
        
        return prevStatePenalty - currentStatePenalty #improvement in traffic is the reward that the model needs to maximize

        pass

    #this function computes the traffic score of each road based on the traffic category thresholds (from road class), and the wait timers
    def calculatePenaltyOfRoadByStateAndDelays(self, trafficCategory, isWaitingTooLong):

        penaltyMultiplier = 2 if isWaitingTooLong==1 else 1 #isWaitingTooLong is an int(boolean) that signifies a wait time of over 3 mins. If it's too big a delay, then traffic score is doubled.

        roadScore = penaltyMultiplier * road.LESS_TRAFFIC_THRESHOLD * (trafficCategory) #minimum achievable penalty would be 0; max would be 120

        return roadScore
        