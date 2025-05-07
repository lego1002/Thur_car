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

    def update(self, encoder_data: np.array):
        if len(encoder_data) > 4: self.input_state = "greater than 4"; return
        if len(encoder_data) < 4: self.input_state = "less than 4"; return
        if len(encoder_data) > 4: self.input_state = "currect"

        theta = self.pos[2]

        # Get encoder readings
        left_rad = encoder_data[0]
        right_rad = encoder_data[1]
        left_omega = encoder_data[2]
        right_omega = encoder_data[3]

        d_left = (left_rad - self.last_left_rad) * self.R
        d_right = (right_rad - self.last_right_rad) * self.R
        d_avg = (d_right + d_left) / 2.0
        dtheta = (d_right - d_left) / self.L

        left_vel = left_omega * self.R
        right_vel = right_omega * self.R
        avg_vel = (right_vel + left_vel) / 2.0
        dvel = (right_vel - left_vel) / self.L

        # Estimate new position
        self.pos[0] = self.pos[0] + (d_avg * math.cos(theta + dtheta / 2.0))
        self.pos[1] = self.pos[1] + (d_avg * math.sin(theta + dtheta / 2.0))
        self.pos[2] = dtheta

        # Estimate new velocity
        self.vel[0] = avg_vel * math.cos(theta)
        self.vel[1] = avg_vel * math.sin(theta)
        self.vel[2] = (dvel * self.R) / 2.0

        self.last_left_rad = left_rad
        self.last_right_rad = right_rad


    def get_pose(self):
        return self.pos

    def get_velocity(self):
        return self.vel

    def reset(self):
        self.__init__(self.R, self.L, self.last_left_rad, self.last_right_rad)