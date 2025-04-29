import numpy as np
import math
import ABEncoder
import numpy as np
import matplotlib.pyplot as plt

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

    def update_test(self):
        theta = self.pos[2]

        # Get encoder readings
        left_deg = self.left_encoder.get_radians()
        right_deg = self.right_encoder.get_radians()
        left_omega = self.left_encoder.get_omega_radians()
        right_omega = self.right_encoder.get_omega_radians()

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


    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def reset(self):
        self.__init__(self.left_encoder, self.right_encoder, self.R, self.L)

def integrate_cart_trajectory(t, v_t, omega_t, R, L):
    assert len(t) == len(v_t) == len(omega_t)

    # Initialize pose
    x = [0.0]
    y = [0.0]
    theta = [0.0]

    # Initialize wheel rotation (radians)
    phi_L = [0.0]
    phi_R = [0.0]

    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        v = v_t[i]
        omega = omega_t[i]

        # Integrate theta
        theta_new = theta[-1] + omega * dt

        # Integrate position using previous theta
        x_new = x[-1] + v * np.cos(theta[-1]) * dt
        y_new = y[-1] + v * np.sin(theta[-1]) * dt

        # Compute individual wheel speeds
        v_L = v - omega * L / 2
        v_R = v + omega * L / 2

        # Integrate wheel rotation (angle = angular velocity * dt = linear_velocity / R * dt)
        phi_L_new = phi_L[-1] + v_L * dt / R
        phi_R_new = phi_R[-1] + v_R * dt / R

        # Append
        x.append(x_new)
        y.append(y_new)
        theta.append(theta_new)
        phi_L.append(phi_L_new)
        phi_R.append(phi_R_new)

    return (
        np.array(x),
        np.array(y),
        np.array(theta),
        np.array(phi_L),
        np.array(phi_R)
    )

# Example usage:
if __name__ == "__main__":
    # Simulated time and velocities
    t = np.linspace(0, 10, 1000)
    v_t = 0.5 * np.ones_like(t)         # constant forward speed
    omega_t = 0.1 * np.sin(0.5 * t)     # oscillating rotation

    R = 0.05  # wheel radius in meters
    L = 0.2   # wheel separation in meters

    x, y, theta, phi_L, phi_R = integrate_cart_trajectory(t, v_t, omega_t, R, L)

    leftencoder = ABEncoder(pulses_per_phase_per_rev=11, debounce_time=0.001)
    rightencoder = ABEncoder(pulses_per_phase_per_rev=11, debounce_time=0.001)
    odometry = CartOdometry(leftencoder, rightencoder, R, L)

    

    # Plotting
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 2, 1)
    plt.plot(t, x)
    plt.title("x(t)")
    
    plt.subplot(3, 2, 2)
    plt.plot(t, y)
    plt.title("y(t)")
    
    plt.subplot(3, 2, 3)
    plt.plot(t, theta)
    plt.title("theta(t)")
    
    plt.subplot(3, 2, 4)
    plt.plot(t, np.rad2deg(phi_L), label="Left Wheel")
    plt.plot(t, np.rad2deg(phi_R), label="Right Wheel")
    plt.title("Wheel Rotation (degrees)")
    plt.legend()
    
    plt.subplot(3, 2, 5)
    plt.plot(x, y)
    plt.title("Trajectory (x vs y)")
    plt.axis('equal')

    plt.tight_layout()
    plt.show()

    while(True):
        odometry.update_test()


