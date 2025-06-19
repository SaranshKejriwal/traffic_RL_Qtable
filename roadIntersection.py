
'''
this roadIntersection class represents the actual 4-way intersection on which the stoplight exists.

It would have 4 road objects - left, right, top, down - each with their respective flow rates of traffic coming into the road.

We'll assume that the exit rate from the intersection is constant across all 4 lanes, meaning that all vehicles exit the intersection after the green light

The decision params to the traffic Light will all be sent from this class
'''
from road import road
from road import roadIdentifier
from trafficLight import trafficLight
from trafficLight import greenLightIndicator
from enum import Enum

#this enum will hold the values of the number of vehicles that can exit the intersection based on duration of the green light
class outflowRate(Enum):
    shortGreenLight = -20 #green light of 30 seconds
    mediumGreenLight = -40 #green light of 60 seconds
    longGreenLight = -60 #green light of 90 seconds



#this class simulates the actual intersection
class roadIntersection:

    leftRoad = road(3, roadIdentifier.left) #lowest inflow of 3 cars per turn. Think of this as a residential street.
    rightRoad = road(4, roadIdentifier.right) #opposite to left road, with slightly higher infow.
    topRoad = road(10, roadIdentifier.top) #busiest road, like an entry point from a main highway
    bottomRoad = road(7, roadIdentifier.bottom) #opposite to top road, like an entry point to a highway

    #
    runningIterations = 0
    worstTrafficScore = 0

    def __init__(self):
        #create a trafficLight object which
        self.trafficSignal = trafficLight()


    def startTrafficFlow(self, iterationCount):
        #this function will contain the actual while loop that updates the traffic status based on the decisions made by the light.
        #iterationCount will ensure that we train for a limited set of iterations and don't get into infinite loops.

        #reset the total traffic counters from any previous iterations
        self.resetVehicleCountOnIntersection()

        for i in range(iterationCount):




            #add more vehicles to each lane, based on their inflow rates


            pass

        pass

    #this method will return the max sum of number of cars across all 4 lanes that were stuck on that lane.
    def getWorstTrafficScore(self):
        pass

    def addVehiclesByInflow(self):
        self.leftRoad.addVehiclesByInflow()
        self.rightRoad.addVehiclesByInflow()
        self.topRoad.addVehiclesByInflow()
        self.bottomRoad.addVehiclesByInflow()

    #this method will reset the traffic on all lanes, based on their inflow rate, to start tracking changes based on traffic light decisions
    def resetVehicleCountOnIntersection(self):
        #this method will only be called once at the start of startTrafficFlow()
        self.leftRoad.resetTotalVehicles()
        self.rightRoad.resetTotalVehicles()
        self.topRoad.resetTotalVehicles()
        self.bottomRoad.resetTotalVehicles()
