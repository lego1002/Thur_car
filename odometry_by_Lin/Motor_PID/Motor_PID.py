import time


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

    def __init__(self, kp, ki, kd, setpoint, sample_time=0.1, output_min=0, output_max=255):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.sample_time = sample_time
        self.last_error = 0.0
        self.integral = 0.0
        self.output_min = output_min
        self.output_max = output_max
        self.output = 0.0

    def update(self, feedback_value):
        """
        Computes the control output based on the feedback value.

        Args:
            feedback_value (float): The current measured value (e.g., motor speed).

        Returns:
            float: The calculated control output (constrained to output limits).
        """
        error = self.setpoint - feedback_value

        # Proportional term
        proportional = self.kp * error

        # Integral term
        self.integral += self.ki * error * self.sample_time
        self.integral = PIDController.bound(self.output_min, self.output_max, self.integral)  #-> can be replace by lerp

        # Derivative term
        derivative = self.kd * (error - self.last_error) / self.sample_time

        # Calculate the control output
        output = proportional + self.integral + derivative

        # Clamp the output to the specified range
        self.output = PIDController.lerp(self.output_min, self.output_max, output)

        # Update last error
        self.last_error = error

        return output

    def set_setpoint(self, setpoint_value):
        self.setpoint = setpoint_value

    def show_status(self):
        print(f"Setpoint updated to: {self.setpoint}, Output updated to: {self.output}, Last_Error updated to: {self.last_error}")

    # ============================================================= #
    #  --------------------- helpers ------------------------------ #
    # ============================================================= #
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
    
    @staticmethod
    def bound(a: float, b: float, t: float) -> float:
        return max(a, min(b, t))




