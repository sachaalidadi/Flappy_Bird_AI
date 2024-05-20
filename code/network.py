import random
from functions import sigmoid
import numpy as np

class Network:
    def __init__(self,mutate=False,weights=None,bias=None):

        if mutate:
            if weights == None or bias == None:
                raise ValueError("Weights and Bias must be provided for mutation")
            else:
                self.weights = []
                for weight in weights:
                    # print(weight)
                    self.weights.append(np.random.normal(weight,0.2))
                    if weights[-1] > 1:
                        weights[-1] = 1
                    elif weights[-1] < -1:
                        weights[-1] = -1
                self.bias = np.random.normal(bias,0.2)
                if self.bias > 1:
                    self.bias = 1
                elif self.bias < -1:
                    self.bias = -1
        else:
            if weights == None or bias == None:
                self.weight1 = random.uniform(-1,1)
                self.weight2 = random.uniform(-1,1)
                self.weight3 = random.uniform(-1,1)
                self.weight4 = random.uniform(-1,1)
                self.weights = [self.weight1,self.weight2,self.weight3,self.weight4]
        
                self.bias = random.uniform(-1,1)
            else:
                self.weights = weights
                self.bias = bias

        self.activation = sigmoid
    
    def forward(self,inputs):
        output = 0
        for i in range(4):
            output += inputs[i] * self.weights[i]
        output += self.bias
        return self.activation(output)