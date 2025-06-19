

'''this class defines a single road in a 4-way intersection
it contains the details of the expected traffic inflow/outflow rate - meaning how many vehicle enter/exit the intersection per unit time.


'''

class road:

    trafficInflowRate = 5 #meaning that 5 cars enter this road and reach the traffic light in each turn.
    totalVehiclesOnRoad = 0 #how many vehicles are on the road at the moment.

    #note - The Q table agent will NOT be aware of the inflow rate of any road. 
    #It will only be able to see the totalVehicles on road, which better reflects what a smart cam system would be able to detect.

    def __init__(self, expectedTrafficInflowRate):
        self.trafficInflowRate = expectedTrafficInflowRate
        #this will be used by the roadIntersection class to setup how busy the lanes are.


    #this is a placeholder function which we can use to change the inflow rate for different times of the day.
    def adjustTrafficInflowRate(self, newInflowRate):
        self.trafficInflowRate = newInflowRate
        pass
