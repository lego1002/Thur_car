import numpy as np 
from Helper import Helpers

class PIDController:
    """
    A PID controller class for controlling a system, such as a motor's speed or position.
    This class focuses solely on the PID control algorithm and does not handle
    any communication with external devices like an Arduino.

    Attributes:
        kp (float): Proportional gain.
        ki (float): Integral gain.
        kd (float): Derivative gain.
        setpoint (float): The desired target value (e.g., speed, position).
        sample_time (float): The time between updates (in seconds).
        last_error (float): The previous error value.
        integral (float): The accumulated error (for the integral term).
        output_min (float): Minimum allowed output value.
        output_max (float): Maximum allowed output value.

    Methods:
        update(feedback_value): Computes the control output based on the feedback.
        set_setpoint(setpoint_value): Updates the setpoint.
    """

    def __init__(self, output_min=0, output_max=255):
        self.last_error = 0.0
        self.integral = 0.0
        self.output_min = output_min
        self.output_max = output_max
        self.output = 0.0

    def update(self, feedback_value, kp, ki, kd, setpoint, delta_time):
        """
        Computes the control output based on the feedback value.

        Args:
            feedback_value (float): The current measured value (e.g., motor speed).

        Returns:
            float: The calculated control output (constrained to output limits).
        """
        error = setpoint - feedback_value

        # Proportional term
        proportional = kp * error

        # Integral term
        self.integral += ki * error * delta_time
        self.integral = Helpers.bound(self.output_min, self.output_max, self.integral)  #-> can be replace by lerp

        # Derivative term
        derivative = kd * (error - self.last_error) / delta_time

        # Calculate the control output
        output = proportional + self.integral + derivative

        # Clamp the output to the specified range
        self.output = Helpers.lerp(self.output_min, self.output_max, output)

        # Update last error
        self.last_error = error

        return output
    
    
    def update_array(self, feedback: np.array, kp: np.array, ki: np.array, kd: np.array, setpoint: np.array, dt):
        array_len = [len(feedback), len(kp), len(ki), len(kd), len(setpoint)]
        max, min = Helpers.find_array_MaxMin(array_len)
        if min < 1: return np.zeros(max)
        if Helpers.find_array_iseqlen(array_len) is False: return np.zeros(max)

        output = np.zeros(max)

        for i in range(max):
            self.update(feedback[i], kp[i], ki[i], kd[i], setpoint[i], delta_time=dt)

        return output


    def show_status(self):
        print(f"Setpoint updated to: {self.setpoint}, Output updated to: {self.output}, Last_Error updated to: {self.last_error}")


class Motor:
    def __init__(self):
        self.pwm = 0                   # Current PWM value
        self.pid_output = np.zeros(2)          # Output from PID controller
        self.pos = np.zeros(3)         # np.array([x, y, z])
        self.vel = np.zeros(3)         # np.array([vx, vy, vz])

    def set_pwm(self, pwm_value):
        """設定 PWM 值（自動裁剪在 0~255）"""
        self.pwm = int(max(0, min(255, pwm_value)))

    def set_pid_output(self, output):
        """儲存 PID 控制器的輸出值"""
        self.pid_output = output

    def update_position(self, new_pos):
        """更新位置 (new_pos: np.array of shape (3,))"""
        if isinstance(new_pos, np.ndarray) and new_pos.shape == (3,):
            self.pos = new_pos
        else:
            raise ValueError("Position must be a numpy array of shape (3,)")

    def update_velocity(self, new_vel):
        """更新速度 (new_vel: np.array of shape (3,))"""
        if isinstance(new_vel, np.ndarray) and new_vel.shape == (3,):
            self.vel = new_vel
        else:
            raise ValueError("Velocity must be a numpy array of shape (3,)")

    def __repr__(self):
        return f"Motor(pwm={self.pwm}, pid_output={self.pid_output}, pos={self.pos}, vel={self.vel})"


