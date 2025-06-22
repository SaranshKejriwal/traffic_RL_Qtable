import numpy as np

from roadIntersection import roadIntersection


print("Hello World...Kill me")
print("Starting model training...")


intersection = roadIntersection()

#train Q table
trainingIterations = 30000
intersection.startTrafficFlow(trainingIterations, True)

print('Worst traffic during training: ', intersection.getWorstTrafficScore())

print("Starting model test...")

testIterations = 30000
#run the model with the trained Q-table to see if the worst score has improved.
#Ensure that the road conditions are fully reset after training
intersection.startTrafficFlow(testIterations, False)

print('Worst traffic during test: ', intersection.getWorstTrafficScore())



