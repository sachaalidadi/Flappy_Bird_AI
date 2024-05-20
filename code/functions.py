import math

def sigmoid(x):
    return 1/(1+math.exp(-x))

def normalize(x, min, max):
    return sigmoid(((x-min)/(max-min))*8-4)