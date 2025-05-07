import numpy as np
import math

class CartOdometry:
    def __init__(self, wheel_radius, wheel_base, last_left_rad: float, last_right_rad: float):
        self.R = wheel_radius
        self.L = wheel_base
        self.last_left_rad = last_left_rad
        self.last_right_rad = last_right_rad

        # These are the decleration of position & angle, velocity & omega vectors
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)     

        self.input_state = "correct"

    def update(self, encoder_data: np.array, dt):
        if len(encoder_data) > 2: self.input_state = "greater than 2"; return
        if len(encoder_data) < 2: self.input_state = "less than 2"; return
        if len(encoder_data) == 2: self.input_state = "currect"

        theta = self.pos[2]

        # Get encoder readings
        left_rad = encoder_data[0]
        right_rad = encoder_data[1]

        d_left = (left_rad - self.last_left_rad) * self.R
        d_right = (right_rad - self.last_right_rad) * self.R
        d_avg = (d_right + d_left) / 2.0
        dtheta = (d_right - d_left) / self.L

        # Estimate new position
        pos0 = self.pos[0] + (d_avg * math.cos(theta + dtheta / 2.0))
        pos1 = self.pos[1] + (d_avg * math.sin(theta + dtheta / 2.0))
        pos2 = dtheta

        # Estimate new velocity
        self.vel[0] = (pos0 - self.pos[0]) / dt
        self.vel[1] = (pos1 - self.pos[1]) / dt
        self.vel[2] = (pos2 - self.pos[2]) / dt 

        self.last_left_rad = left_rad
        self.last_right_rad = right_rad


    def get_pose(self):
        return self.pos

    def get_velocity(self):
        return self.vel

    def reset(self):
        self.__init__(self.R, self.L, self.last_left_rad, self.last_right_rad)
