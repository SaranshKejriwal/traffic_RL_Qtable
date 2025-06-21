'''

THis class is expected to ingest a series of model outputs, and compute the total time to show on the traffic light timer, based on the cumulative amount of loops between successive greens
'''
import numpy as np
from road import roadIdentifier

class timerCalculator:

    #these wait times represent the times taken between 2 successive green lights on the same lane. 
    #these are reset when the light for any lane is green.
    #if the Wait time for any lane is more than 3 minutes (180 seconds), then it will impact the reward function by double 
    waitingSecondsByRoad = np.zeros(4)

    GREEN_LIGHT_DURATIONS = np.array([30,60,90])


    def __init__(self):


        pass

    #update the timers based on which lane was made green, and for how long.
    def updateWaitTimeAfterModelDecision(self, decidedRoadIndex, decidedDuration):

        #add the green light duration to ALL 4 lanes (just for efficiency)
        self.waitingSecondsByRoad += self.GREEN_LIGHT_DURATIONS[decidedDuration]

        #reset the green timer to 0, ONLY for the greenlit road.
        self.waitingSecondsByRoad[decidedRoadIndex] = 0

        return

    #get max wait time on each light for tracking.
    def getMaxWaitTime(self):
        return max(self.leftGreenWaitSeconds, self.rightGreenWaitSeconds, self.topGreenWaitSeconds, self.bottomGreenWaitSeconds)

    #boolean value - true if the any road signal has been red for over 180 seconds
    def isLeftWaitTooLong(self):
        return int(self.waitingSecondsByRoad[0] > 180) #left = 0
    def isRightWaitTooLong(self):
        return int(self.waitingSecondsByRoad[1] > 180) #right = 1
    def isTopWaitTooLong(self):
        return int(self.waitingSecondsByRoad[2] > 180) #top = 2
    def isBottomWaitTooLong(self):
        return int(self.waitingSecondsByRoad[3] > 180) #bottom = 3