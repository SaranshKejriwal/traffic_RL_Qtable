from enum import Enum

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

    greenLight = greenLightIndicator.noLaneGreen #init at this value


