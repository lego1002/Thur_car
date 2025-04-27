from Motor_PID import PIDController
from Arduino_Commute import ArduinoCommunicator

def run_pid_controller():
    """
    Example function to run the PID controller and communicate with the Arduino.
    """
    # PID gains (tune these for your specific motor and application)
    kp = 1.0
    ki = 0.05
    kd = 0.2
    setpoint = 100.0
    arduino_port = '/dev/ttyACM0'  # Change to your Arduino's serial port

    # Create instances of the PIDController and ArduinoCommunicator
    pid_controller = PIDController(kp, ki, kd, setpoint, sample_time=0.1, output_min=0, output_max=255)
    arduino_comm = ArduinoCommunicator(arduino_port=arduino_port, serial_baudrate=115200)

    try:
        # Connect to the Arduino
        arduino_comm.connect()

        # Simulate the motor and feedback
        current_value = 0.0
        start_time = time.time()
        while time.time() - start_time < 10:
            # Simulate getting feedback from the motor
            current_value = current_value + (setpoint - current_value) * 0.1 + (random.random() - 0.5) * 10
            if current_value < 0:
                current_value = 0
            print(f"Current Value: {current_value:.2f}")

            # Update the PID controller and get the PWM output
            pwm_value = pid_controller.update(current_value)
            if pwm_value is not None:
                arduino_comm.send_pwm(pwm_value)

            time.sleep(pid_controller.sample_time)

        pid_controller.set_setpoint(50)
        while time.time() - start_time < 20:
            current_value = current_value + (setpoint - current_value) * 0.1 + (random.random() - 0.5) * 10
            if current_value < 0:
                current_value = 0
            print(f"Current Value: {current_value:.2f}")
            pwm_value = pid_controller.update(current_value)
            if pwm_value is not None:
                arduino_comm.send_pwm(pwm_value)
            time.sleep(pid_controller.sample_time)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the serial connection is closed when the program finishes or an error occurs
        arduino_comm.disconnect()

if __name__ == "__main__":
    import random
    run_pid_controller()