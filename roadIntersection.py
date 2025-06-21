
'''
this roadIntersection class represents the actual 4-way intersection on which the stoplight exists.

It would have 4 road objects - left, right, top, down - each with their respective flow rates of traffic coming into the road.

We'll assume that the exit rate from the intersection is constant across all 4 lanes, meaning that all vehicles exit the intersection after the green light

The decision params to the traffic Light will all be sent from this class
'''
from road import road
from road import roadIdentifier
from trafficLight import trafficLight
from enum import Enum
import numpy as np




#this class simulates the actual intersection
class roadIntersection:

    leftRoad = road(3, roadIdentifier.left) #lowest inflow of 3 cars per turn. Think of this as a residential street.
    rightRoad = road(4, roadIdentifier.right) #opposite to left road, with slightly higher infow.
    topRoad = road(10, roadIdentifier.top) #busiest road, like an entry point from a main highway
    bottomRoad = road(7, roadIdentifier.bottom) #opposite to top road, like an entry point to a highway

    #counter to avoid infinite loop
    runningIterations = 0

    worstTrafficScore = 0

    #this array will hold the values of the number of vehicles that can exit the intersection based on duration of the green light
    OUTFLOW_RATE = np.array([-20,-40,-60]) #corresponding to the index predicted by the model
    #this means that 20 vehicles exit in 30 seconds, 40 in 60 seconds, and 60 in 90 seconds

    def __init__(self):
        #create a trafficLight object which
        self.trafficSignal = trafficLight()


    def startTrafficFlow(self, iterationCount, isTraining):
        #this function will contain the actual while loop that updates the traffic status based on the decisions made by the light.
        #iterationCount will ensure that we train for a limited set of iterations and don't get into infinite loops.

        #reset the total traffic counters from any previous iterations
        self.resetVehicleCountOnIntersection()
        print("starting intersecction iterations...")

        for i in range(iterationCount):


            #pass the context of the 4 lanes to the model to get a decision - the traffic light can only see the number of vehicles on the road, NOT the inflows
            greenlitRoadIndex, greenLightDurationIndex =  self.trafficSignal.getModelDecision(self.leftRoad.getTrafficCategorization(),self.rightRoad.getTrafficCategorization(),self.topRoad.getTrafficCategorization(),self.bottomRoad.getTrafficCategorization())

            print('green road:',greenlitRoadIndex,'; chosenDuration:',greenLightDurationIndex)

            #greenLightDuration should be an int between 0 and 2
            self.processDecision(roadIdentifier(greenlitRoadIndex), self.OUTFLOW_RATE[greenLightDurationIndex])

            #compute the net traffic just after the decision was processed -  in terms of absolute sum of cars on the road without considering wait time.
            self.calculateWorstTraffic(self.leftRoad.getTotalVehicles(),self.rightRoad.getTotalVehicles(),self.topRoad.getTotalVehicles(),self.bottomRoad.getTotalVehicles(),)

            #add more vehicles to each lane, based on their inflow rates
            self.addVehiclesByInflow()



        pass

    #this method will return the max sum of number of cars across all 4 lanes that were stuck on that lane.
    def getWorstTrafficScore(self):
        return self.trafficSignal.getWorstTrafficScore()
    
    def calculateWorstTraffic(self, leftRoadTraffic, rightRoadTraffic, topRoadTraffic, bottomRoadTraffic):
        totalTraffic = leftRoadTraffic + rightRoadTraffic + topRoadTraffic + bottomRoadTraffic

        if totalTraffic > self.worstTrafficScore:
            self.worstTrafficScore = totalTraffic #update the worst traffic.

            print('Worst Traffic:',totalTraffic , '; [',leftRoadTraffic,',',bottomRoadTraffic,',',topRoadTraffic,',',bottomRoadTraffic,']',)

    '''Note - this will NOT directly be the reward function - the actual reward function will further penalize an excess wait time on each light'''


    def processDecision(self,greenlitRoad, outflow):
        self.leftRoad.processTrafficLightDecision(greenlitRoad, outflow)
        self.rightRoad.processTrafficLightDecision(greenlitRoad, outflow)
        self.topRoad.processTrafficLightDecision(greenlitRoad, outflow)
        self.bottomRoad.processTrafficLightDecision(greenlitRoad, outflow)
        #3 of the roads will compare greenlitRoad enum to themselves and take no action if there is no match.



    def addVehiclesByInflow(self):
        self.leftRoad.updateTotalVehiclesByInflow()
        self.rightRoad.updateTotalVehiclesByInflow()
        self.topRoad.updateTotalVehiclesByInflow()
        self.bottomRoad.updateTotalVehiclesByInflow()

    #this method will reset the traffic on all lanes, based on their inflow rate, to start tracking changes based on traffic light decisions
    def resetVehicleCountOnIntersection(self):
        #this method will only be called once at the start of startTrafficFlow()
        self.leftRoad.resetTotalVehicles()
        self.rightRoad.resetTotalVehicles()
        self.topRoad.resetTotalVehicles()
        self.bottomRoad.resetTotalVehicles()

        #reset worst traffic score to 0
        self.trafficSignal.resetWorstTrafficScore()
