
'''
this roadIntersection class represents the actual 4-way intersection on which the stoplight exists.

It would have 4 road objects - left, right, top, down - each with their respective flow rates of traffic coming into the road.

We'll assume that the exit rate from the intersection is constant across all 4 lanes, meaning that all vehicles exit the intersection after the green light

The decision params to the traffic Light will all be sent from this class
'''

from trafficLight import trafficLight

class roadIntersection:

    def __init__(self):

        intersectionShortExitRate = 20 #20 cars can exit the intersection in a 30 second green light.  