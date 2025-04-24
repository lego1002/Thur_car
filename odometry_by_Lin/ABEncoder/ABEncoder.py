import math

class ABEncoder:
    def __init__(self, pulses_per_phase_per_rev=11):
        self.counts_per_rev = pulses_per_phase_per_rev * 4  # 4x decoding #
        self.countor = 0        
        self.last_state = 0b00  # --(A << 1) | B -------------------------#
        # --4-bit transition key: (old_state << 2) | new_state : delta--- #
        self.lookup = {
            0b0001: 1,  0b0010: -1,
            0b0100: -1, 0b0111: 1,
            0b1000: 1,  0b1011: -1,
            0b1101: -1, 0b1110: 1
        }

    # =================================================================== #
    # The update method of the A/B Encoder
    # =================================================================== #
    def update(self, a: int, b: int):
        # ------------Call this whenever A/B inputs change--------------- #
        current_state = (a << 1) | b
        transition = (self.last_state << 2) | current_state
        delta = self.lookup.get(transition, 0)
        self.countor += delta
        self.last_state = current_state

    def reset(self):
        self.countor = 0

    def get_degrees(self):
        # ----------Return current rotation in degrees------------------- #
        return (self.countor / self.counts_per_rev) * 360
    
    def get_radians(self):
        # ----------Return current rotation in radians------------------- #
        return (self.countor / self.counts_per_rev) * (2 * math.pi)

    def get_revolutions(self):
        # ----------Return total revolutions (can be negative)----------- #
        return self.countor / self.counts_per_rev
    