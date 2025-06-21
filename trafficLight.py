from enum import Enum
from operator import le
from tkinter import TOP
from timerCalculator import timerCalculator


'''
this class represents a 4 way traffic light, where only 1 of the 4 lights can be green at a time.
'''

class greenLightIndicator(Enum):
    #this enum will represent which of the 4 lights on the traffic light is green
    leftLaneGreen = 1
    rightLaneGreen = 2
    topLaneGreen = 3
    bottomLaneGreen = 4

    noLaneGreen = 999 #used for initialization only

    #this will reduce the magic numbers involved in toggling the lights on/off.


class trafficLight:

    greenLight = greenLightIndicator.noLaneGreen #init at this value. Only one of the lanes will be green

    worstTrafficScore = 0 #will be used to calculate the highest traffic across all 4 lanes
    #this is in terms of absolute number of cars on the road - NOT based on the delay factor of >180sec delay between successive green lights on a lane.



    def __init__(self):

        #this wait calculator will check the delays between 2 green lights for any lane. 
        #If that wait time is more than 3 minutes for any lane, that'll be frustrating, and should be 
        self.waitCalc = timerCalculator()

    #this is the important function which will ingest the traffic stats, create state vector, comput
    def getModelDecision(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):

        #update the worst traffic score - in terms
        self.calculateWorstTraffic(leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic)

        pass


    def calculateWorstTraffic(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        totalTraffic = leftRoadTraffic + rightRoadTraffic + topRoadTraffic + bottomRoadTraffic

        if totalTraffic > self.worstTrafficScore:
            self.worstTrafficScore = totalTraffic #update the worst traffic.

            print('Worst Traffic:',totalTraffic , '; [',leftRoadTraffic,',',bottomRoadTraffic,',',topRoadTraffic,',',bottomRoadTraffic,']',)

    '''Note - this will NOT directly be the reward function - the actual reward function will further penalize an excess wait time on each light'''
    

    #this function will calculate the reward from taking any action
    def calculateReward(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        totalTraffic = leftRoadTraffic + rightRoadTraffic + topRoadTraffic + bottomRoadTraffic
        pass

    def getWorstTrafficScore(self):
        return self.worstTrafficScore

    def resetWorstTrafficScore(self):
        self.worstTrafficScore = 0 #this will be called when the game resets.