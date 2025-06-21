from enum import Enum

'''this class defines a single road in a 4-way intersection
it contains the details of the expected traffic inflow/outflow rate - meaning how many vehicle enter/exit the intersection per unit time.


'''
 

class roadIdentifier(Enum):
    left = 0
    right = 1
    top = 2
    bottom = 3

    none = 999 #for initialization only

class road:

    roadType = roadIdentifier.none

    trafficInflowRate = 0 #the number of cars enter this road and reach the traffic light in each turn.
    totalVehiclesOnRoad = 0 #how many vehicles are on the road at the moment.

    #traffic categorization thresholds - constants.
    LESS_TRAFFIC_THRESHOLD = 30 #there are less than 30 cars on a single road
    MED_TRAFFIC_THRESHOLD = 60 #there are 30-60 cars on a single road. Anything more than 60 cars is heavy traffic
    #these values are deliberately slightly higher than outflow rates to ensure that the model is trained for a continuous traffic flow, not emptying the roads.

    #note - The Q table agent will NOT be aware of the inflow rate of any road. 
    #It will only be able to see the totalVehicles on road, which better reflects what a smart cam system would be able to detect.

    def __init__(self, expectedTrafficInflowRate, roadID):
        self.trafficInflowRate = expectedTrafficInflowRate
        #this will be used by the roadIntersection class to setup how busy the lanes are.
        self.roadType = roadID #may be useful for debugging.

    #this function returns the category of traffic - less, medium, heavy, based on 
    def getTrafficCategorization(self):
        if self.totalVehiclesOnRoad <= self.LESS_TRAFFIC_THRESHOLD: #less than 30
            return 0
        elif self.totalVehiclesOnRoad <= self.MED_TRAFFIC_THRESHOLD: #less than 60 but not less than 30
            return 1
        elif self.totalVehiclesOnRoad > self.MED_TRAFFIC_THRESHOLD: #anything more than 60
            return 2

        #the model is bucketing into 3 possible values - 0,1,2 - based on light/med/heavy traffic

    def getTotalVehicles(self):
        return self.totalVehiclesOnRoad

    def updateTotalVehicleCount(self, changeInCount):
        self.totalVehiclesOnRoad = self.totalVehiclesOnRoad + changeInCount
        #changeInCount will be positive when inflow rate is added, and negative when the roadIntersection outflow rate is subtracted

        if(self.totalVehiclesOnRoad) < 0:
            self.totalVehiclesOnRoad = 0 
            # in case the outflow exceeds the total vehicles on the road, the road is empty, 
            #it makes no sense to have negative number of vehicles
    

    #Adds more vehicles to the road, based on the inflow rate of that road
    def updateTotalVehiclesByInflow(self):
        self.totalVehiclesOnRoad = self.totalVehiclesOnRoad + self.trafficInflowRate


    def processTrafficLightDecision(self, greenlitRoad, outflow):
        if self.roadType == greenlitRoad: #reduce vehicle count only if oneself is greenlit
            self.updateTotalVehicleCount(outflow) #outflow should be negative
        else:
            return


    #resets the previous total of vehicles and sets them to the values expected at the start of the game, ie just the inflow from the first loop. 
    def resetTotalVehicles(self):
        self.totalVehiclesOnRoad = self.trafficInflowRate

    #this is a placeholder function which we can use to change the inflow rate for different times of the day, if needed.
    def adjustTrafficInflowRate(self, newInflowRate):
        self.trafficInflowRate = newInflowRate
        
