import numpy as np

from roadIntersection import roadIntersection


print("Hello World...Kill me")
print("Starting model training...")


intersection = roadIntersection()



#train Q table
trainingIterations = 10000
intersection.startTrafficFlow(trainingIterations)

testIterations = 10000
#run the model with the trained Q-table to see if the worst score has improved.
intersection.startTrafficFlow(testIterations)



