import numpy as np
import math
import time

class Helpers:
    def __init__(self):
        pass
    
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
    
    @staticmethod
    def _2Dlerp(t0, t1, y0, y1, t):
        if t1 == t0:  # Avoid division by zero
            return y0
        return y0 + (y1 - y0) * ((t - t0) / (t1 - t0))
    
    @staticmethod
    def bound(a: float, b: float, t: float) -> float:
        return max(a, min(b, t))
    
    @staticmethod
    def mean(a: list):
        l = len(a)
        sum = 0
        for i in range(l):
            sum += a[i]
        return sum
    
    @staticmethod 
    def ABphasetoPos(a: float, b: float, c: float, L:float):
        P = np.array([
            ((a + b) * math.cos(c)) / 2,
            ((a + b) * math.sin(c)) / 2,
            (b - a) / (L * 2)
        ])

        return P
    
    @staticmethod
    def ABphasetoVel(a: float, b: float, c: float, R: float, L:float):
        V = np.array([
            ((a + b) * math.cos(c)) / 2
            ((a + b) * math.sin(c)) / 2
            ((b - a) * R) / (L * 2)
        ])

        return V

    @staticmethod
    def PostoABphase(P: np.array, L:float):
        if len(P) > 3: return

        c = math.atan2(P[0], P[1])

        sum_term = 2 * (P[0] * math.cos(c) + P[1] * math.sin(c))
        diff_term = 2 * L * P[2]

        a = (sum_term - diff_term) / 2
        b = (sum_term + diff_term) / 2

        return a, b
    
    @staticmethod
    def VeltoABphase(V: np.array, c: float, R: float, L:float):
        if len(V) > 3: return

        sum_term = 2 * (V[0] * math.cos(c) + V[1] * math.sin(c))
        diff_term = (2 * L * V[2]) / R

        a = (sum_term - diff_term) / 2
        b = (sum_term + diff_term) / 2

        return a, b
    
    @staticmethod
    def getCurrentTime():
        return time.perf_counter()

    @staticmethod
    def _3vecto2vec(a: np.array):
        if len(a) != 3: return

        b1 = math.sqrt(a[0] * a[0] + a[1] * a[1])
        b2 = a[2]

        return np.array([b1, b2])
    
    @staticmethod
    def find_array_MaxMin(array: list):
        if len(array) < 1: return

        max_val = array[0]
        min_val = array[0]

        for num in array:
            if num > max_val:
                max_val = num
            if num < min_val:
                min_val = num

        return max_val, min_val 
    
    @staticmethod
    def find_array_iseqlen(array: list):
        if len(array) < 1: return

        for i in range(len(array)):
            if array[i] != array[0]:
                return False
        
        return True
    
    @staticmethod
    def compute_pwm_from_velocity(delta_v, delta_w, wheel_base, wheel_radius, k_pwm):

        # 線速度 → 輪速
        v_left = delta_v - (wheel_base / 2.0) * delta_w
        v_right = delta_v + (wheel_base / 2.0) * delta_w

        # 輪速 → 角速度
        omega_left = v_left / wheel_radius
        omega_right = v_right / wheel_radius

        # 角速度 → PWM（正負代表方向）
        pwm_left = omega_left * k_pwm
        pwm_right = omega_right * k_pwm

        # 如果只允許單向（如你說的），則限制最小為 0，最大為 255
        pwm_left = max(0, min(255, int(pwm_left)))
        pwm_right = max(0, min(255, int(pwm_right)))

        return pwm_left, pwm_right