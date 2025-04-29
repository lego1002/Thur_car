import math
import time

class ABEncoder:
    def __init__(self, pulses_per_phase_per_rev=11, debounce_time=0.001):
        self.counts_per_rev = pulses_per_phase_per_rev * 4  # 4x decoding #
        
        self.last_time = time.perf_counter()
        self.debouce_time = debounce_time
        self.min_interval = 0.00001 # --100kHz -> 0.00001s ---------------#

        self.counter = 0     
        self.vel_counter = 0  
        self.last_state = 0b00  # --(A << 1) | B -------------------------#
        # --4-bit transition key: (old_state << 2) | new_state : delta--- #
        self.lookup = {
            (0b00, 0b00): 0,
            (0b00, 0b01): +1,
            (0b00, 0b10): -1,
            (0b00, 0b11): 0,
            (0b01, 0b00): -1,
            (0b01, 0b01): 0,
            (0b01, 0b11): +1,
            (0b01, 0b10): 0,
            (0b11, 0b01): -1,
            (0b11, 0b11): 0,
            (0b11, 0b10): +1,
            (0b11, 0b00): 0,
            (0b10, 0b11): -1,
            (0b10, 0b10): 0,
            (0b10, 0b00): +1,
            (0b10, 0b01): 0,
        }

    # =================================================================== #
    # The update method of the A/B Encoder
    # =================================================================== #
    def update(self, a: int, b: int):
        current_time = time.perf_counter()
        dt = current_time - self.last_time

        current_state = (a << 1) | b
        key = (self.last_state, current_state)
        delta = self.lookup.get(key, 0)

        if dt >= self.debounce_time:
            self.counter += delta
            self.vel_counter = delta / max(dt, self.min_interval)
            self.last_state = current_state
            self.last_time = current_time
        else:
            self.last_state = current_state

    def reset(self):
        self.counter = 0

    def get_counter(self):
        # ------------Return current ABEncoder counter------------------- #
        return self.counter

    def get_vel_counter(self):
        # ----------Return current ABEncoder vel_counter----------------- #
        return self.vel_counter

    def get_degrees(self):
        # ----------Return current rotation in degrees------------------- #
        return (self.counter / self.counts_per_rev) * 360
    
    def get_omega_degree(self):
        # ----------Return current omega in degrees---------------------- #
        return (self.vel_counter / self.counts_per_rev) * 360
    
    def get_radians(self):
        # ----------Return current rotation in radians------------------- #
        return (self.counter / self.counts_per_rev) * (2 * math.pi)
    
    def get_omega_radians(self):
        # ----------Return current omega in radians---------------------- #
        return (self.vel_counter / self.counts_per_rev) * (2 * math.pi)

    def get_revolutions(self):
        # ----------Return total revolutions (can be negative)----------- #
        return self.counter / self.counts_per_rev
    
