import numpy as np
import math
import ABEncoder

class CartOdometry:
    def __init__(self, left_encoder : ABEncoder, right_encoder : ABEncoder, wheel_radius, wheel_base):
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.R = wheel_radius
        self.L = wheel_base

        # These are the decleration of position & angle, velocity & omega vectors
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)     

        self._last_left_deg = self.left_encoder.get_radians()
        self._last_right_deg = self.right_encoder.get_radians()

    def update(self):
        theta = self.pos[2]

        # Get encoder readings
        left_deg = self.left_encoder.get_radians()
        right_deg = self.right_encoder.get_radians()
        left_omega = self.left_encoder.ge_omega_radians()
        right_omega = self.right_encoder.ge_omega_radians()

        d_left = (left_deg - self._last_left_deg) * self.R
        d_right = (right_deg - self._last_right_deg) * self.R

        left_vel = left_omega * self.R
        right_vel = right_omega * self.R

        # Estimate new position
        delta_pos = np.array([
            ((d_left + d_right) * math.cos(theta)) / 2,
            ((d_left + d_right) * math.sin(theta)) / 2,
            (d_right - d_left) / (self.L * 2)
        ])

        # Estimate new velocity
        new_vel = np.array([
            ((left_vel + right_vel) * math.cos(theta)) / 2
            ((left_vel + right_vel) * math.sin(theta)) / 2
            ((right_vel - left_vel) * self.R) / (self.L * 2)
        ])

        self.pos = self.pos + delta_pos
        self.vel = new_vel

        self._last_left_deg = left_deg
        self._last_right_deg = right_deg


    def get_pose(self):
        return (*self.pos, math.degrees(self.theta))

    def get_velocity(self):
        return (*self.vel, math.degrees(self.omaga))

    def reset(self):
        self.__init__(self.left_encoder, self.right_encoder, self.R, self.L)
