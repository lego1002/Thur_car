import numpy as np

class Helpers:
    def __init__(self):
        pass
    
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
    
    @staticmethod
    def bound(a: float, b: float, t: float) -> float:
        return max(a, min(b, t))
    
    @staticmethod
    def mean(a: np.array):
        l = a.len()
        sum = 0
        for i in range(l):
            sum += a[i]
        return sum
