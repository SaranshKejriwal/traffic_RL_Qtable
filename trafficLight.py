
from timerCalculator import timerCalculator
import numpy as np
from modelContainer import modelContainer
from road import road

'''
this class represents a 4 way traffic light, where only 1 of the 4 lights can be green at a time.
'''



class trafficLight:
 

    #traffic categorization thresholds - constants.
    LESS_TRAFFIC_THRESHOLD = 30 #there are less than 30 cars on a single road
    MED_TRAFFIC_THRESHOLD = 60 #there are 30-60 cars on a single road. Anything more than 60 cars is heavy traffic
    #these values are deliberately slightly higher than outflow rates to ensure that the model is trained for a continuous traffic flow, not emptying the roads.

    isTraining = True

    #These will be used to retain the state vectors for updating the Q table using the bellman equation
    currentStateVector = np.zeros(8)
    previousStateVector = np.zeros(8)

    def __init__(self):

        #this wait calculator will check the delays between 2 green lights for any lane. 
        #If that wait time is more than 3 minutes for any lane, that'll be frustrating, and should be 
        self.waitCalc = timerCalculator()
        self.model = modelContainer()

    #this is the important function which will ingest the traffic stats, create state vector, comput
    def getModelDecision(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):


        self.currentStateVector = self.getStateVectorForModel(leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic)

        #get the highest reward from reading the Q-table
        decidedRoadIndex, decidedDurationIndex = self.model.getModelDecision(self.currentStateVector)

        self.waitCalc.updateWaitTimeAfterModelDecision(decidedRoadIndex, decidedDurationIndex)


        if(self.isTraining):

            #rewardFromDecision  = self.model.calculateRewardBetweenStates(self.previousStateVector, self.currentStateVector)
            rewardFromDecision = self.getRewardByTrafficCount(leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic)

            self.model.updateQTable(self.currentStateVector, self.previousStateVector, decidedRoadIndex, decidedDurationIndex, rewardFromDecision)


        #update the previous state to the current state, AFTER the old value has been used to update the Q table
        self.previousStateVector = self.currentStateVector

        return decidedRoadIndex, decidedDurationIndex


    def getStateVectorForModel(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        stateVector = np.array([
            self.getTrafficCategorizationOfValue(leftRoadTraffic), self.getTrafficCategorizationOfValue(rightRoadTraffic), self.getTrafficCategorizationOfValue(topRoadTraffic), self.getTrafficCategorizationOfValue(bottomRoadTraffic) 
                                                                                                                                                                                                                    #traffic categorizations for all 4 lanes
            ,self.waitCalc.isLeftWaitTooLong(),self.waitCalc.isRightWaitTooLong(),self.waitCalc.isTopWaitTooLong(),self.waitCalc.isBottomWaitTooLong() #timer checkers on all 4 lanes
            ])

        return stateVector

    def getRewardByTrafficCount(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        #model will have to bring the negative reward closer to 0
        totalNegativeReward = 0

        totalNegativeReward -= leftRoadTraffic * (2 if self.waitCalc.isLeftWaitTooLong() else 1)
        totalNegativeReward -= rightRoadTraffic * (2 if self.waitCalc.isRightWaitTooLong() else 1)
        totalNegativeReward -= topRoadTraffic * (2 if self.waitCalc.isTopWaitTooLong() else 1)
        totalNegativeReward -= bottomRoadTraffic * (2 if self.waitCalc.isBottomWaitTooLong() else 1)

        return totalNegativeReward

        pass

    #used to toggle whether to update the Q-table or not
    def setIsTraining(self, isTraining):
        self.isTraining = isTraining
    



        #this function returns the category of traffic - less, medium, heavy, based on the threshold
    def getTrafficCategorizationOfValue(self, trafficValue):
        if trafficValue <= self.LESS_TRAFFIC_THRESHOLD: #less than 30
            return int(0)
        elif trafficValue <= self.MED_TRAFFIC_THRESHOLD: #less than 60 but not less than 30
            return int(1)
        elif trafficValue > self.MED_TRAFFIC_THRESHOLD: #anything more than 60
            return int(2) #typecasting here is important because these will be array indices

        #the model is bucketing into 3 possible values - 0,1,2 - based on light/med/heavy traffic