import numpy as np
import time
import math
import ABEncoder

class CartOdometry:
    def __init__(self, left_encoder, right_encoder, wheel_radius, wheel_base):
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.R = wheel_radius
        self.L = wheel_base

        # These are the decleration of position, velocity, and acceleration vectors
        self.pos = np.zeros(2)
        self.vel = np.zeros(2)
        self.acc = np.zeros(2)
        
        # These are the decleration of historic position, and velocity vectors
        self._prev_vel = np.zeros(2)
        self._prev_pos = np.zeros(2)
        

        # These are the decleration of angle, angular velocity, and angular acceleration value of the cart itself (in radians)
        self.theta = 0.0
        self.omaga = 0.0
        self._prev_omaga = 0.0
        self.alpha = 0.0

        self._last_left_deg = self.left_encoder.get_radians()
        self._last_right_deg = self.right_encoder.get_radians()
        self._last_time = time.time()

    def update(self):
        now = time.time()
        dt = now - self._last_time
        if dt <= 0: return

        # Get encoder readings
        left_deg = self.left_encoder.get_radians()
        right_deg = self.right_encoder.get_radians()
        d_left = (left_deg - self._last_left_deg) * self.R
        d_right = (right_deg - self._last_right_deg) * self.R

        ds = (d_left + d_right) / 2
        dtheta = (d_right - d_left) / self.L
        heading = self.theta + dtheta / 2

        # Estimate new position
        delta_pos = np.array([
            ds * math.cos(heading),
            ds * math.sin(heading)
        ])
        new_pos = self.pos + delta_pos

        # Midpoint estimation for velocity
        new_vel = (new_pos - self._prev_pos) / (2 * dt)
        self.acc = (new_vel - self._prev_vel) / (2 * dt)

        # Angular velocity and acceleration (also via midpoint)
        new_omaga = dtheta / dt
        self.alpha = (new_omaga - self._prev_omaga) / (2 * dt)

        # Update states
        self._prev_pos = self.pos.copy()
        self._prev_vel = self.vel.copy()
        self._prev_omaga = self.omaga
        self.pos = new_pos
        self.vel = new_vel
        self.omaga = new_omaga
        self.theta += dtheta

        self._last_left_deg = left_deg
        self._last_right_deg = right_deg
        self._last_time = now

    def get_pose(self):
        return (*self.pos, math.degrees(self.theta))

    def get_velocity(self):
        return (*self.vel, math.degrees(self.omaga))

    def get_acceleration(self):
        return (*self.acc, math.degrees(self.alpha))

    def reset(self):
        self.__init__(self.left_encoder, self.right_encoder, self.R, self.L)