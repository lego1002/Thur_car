import numpy as np
from Helper import Helpers

class CartOdometry:
    def __init__(self, wheel_radius, wheel_base, last_left_deg: float, last_right_deg: float):
        self.R = wheel_radius
        self.L = wheel_base
        self.last_left_deg = last_left_deg
        self.last_right_deg = last_right_deg

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
        left_deg = encoder_data[0]
        right_deg = encoder_data[1]
        left_omega = encoder_data[2]
        right_omega = encoder_data[3]

        d_left = (left_deg - self.last_left_deg) * self.R
        d_right = (right_deg - self.last_right_deg) * self.R

        left_vel = left_omega * self.R
        right_vel = right_omega * self.R

        # Estimate new position
        '''
        delta_pos = np.array([
            ((d_left + d_right) * math.cos(theta)) / 2,
            ((d_left + d_right) * math.sin(theta)) / 2,
            (d_right - d_left) / (self.L * 2)
        ])
        '''

        # Estimate new velocity
        '''
        new_vel = np.array([
            ((left_vel + right_vel) * math.cos(theta)) / 2
            ((left_vel + right_vel) * math.sin(theta)) / 2
            ((right_vel - left_vel) * self.R) / (self.L * 2)
        ])
        '''

        self.pos = self.pos + Helpers.ABphasetoPos(d_left, d_right, theta, self.L)
        self.vel = Helpers.ABphasetoVel(left_vel, right_vel, theta, self.R, self.L)

        self.last_left_deg = left_deg
        self.last_right_deg = right_deg


    def get_pose(self):
        return self.pos

    def get_velocity(self):
        return self.vel

    def reset(self):
        self.__init__(self.left_encoder, self.right_encoder, self.R, self.L)