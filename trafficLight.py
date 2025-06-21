from enum import Enum
from timerCalculator import timerCalculator
import numpy as np
from modelContainer import modelContainer


'''
this class represents a 4 way traffic light, where only 1 of the 4 lights can be green at a time.
'''



class trafficLight:

    
    worstTrafficScore = 0 #will be used to calculate the highest traffic across all 4 lanes
    #this is in terms of absolute number of cars on the road - NOT based on the delay factor of >180sec delay between successive green lights on a lane.


    def __init__(self):

        #this wait calculator will check the delays between 2 green lights for any lane. 
        #If that wait time is more than 3 minutes for any lane, that'll be frustrating, and should be 
        self.waitCalc = timerCalculator()
        self.model = modelContainer()

    #this is the important function which will ingest the traffic stats, create state vector, comput
    def getModelDecision(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):


        stateVector = self.getStateVectorForModel(leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic)

        #get the highest reward from reading the Q-table
        decidedRoadIndex, decidedDurationIndex = self.model.getModelDecision(stateVector)

        self.waitCalc.updateWaitTimeAfterModelDecision(decidedRoadIndex, decidedDurationIndex)

        return decidedRoadIndex, decidedDurationIndex


    def getStateVectorForModel(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        stateVector = np.array([
            leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic #traffic categorizations for all 4 lanes
            ,self.waitCalc.isLeftWaitTooLong(),self.waitCalc.isRightWaitTooLong(),self.waitCalc.isTopWaitTooLong(),self.waitCalc.isBottomWaitTooLong() #timer checkers on all 4 lanes
            ])

        return stateVector



    

    #this function will calculate the reward from taking any action
    def calculateReward(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        totalTraffic = leftRoadTraffic + rightRoadTraffic + topRoadTraffic + bottomRoadTraffic
        pass

    def getWorstTrafficScore(self):
        return self.worstTrafficScore

    def resetWorstTrafficScore(self):
        self.worstTrafficScore = 0 #this will be called when the game resets.