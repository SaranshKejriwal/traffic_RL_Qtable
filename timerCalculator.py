'''

THis class is expected to ingest a series of model outputs, and compute the total time to show on the traffic light timer, based on the cumulative amount of loops between successive greens
'''

from trafficLight import greenLightIndicator

class timerCalculator:

    #these wait times represent the times taken between 2 successive green lights on the same lane. 
    #these are reset when the light for any lane is green.
    #if the Wait time for any lane is more than 3 minutes (180 seconds), then it will impact the reward function by double 
    leftGreenWait = 0
    rightGreenWait = 0

    def __init__(self):


        pass