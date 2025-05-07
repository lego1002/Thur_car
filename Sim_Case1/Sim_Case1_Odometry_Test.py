from Encoder_Test import EncoderReader
from Cart_Odometry import CartOdometry
from Motor_PID import PIDController
from Motor_PID import Motor
from Helper import Helpers
from ArduinoPWM import ArduinoPWMController
from Cases_Data import Case1
import numpy as np
import time

def awake():
    print("Initializing hardware and parameters...")

def main():
    awake()

    # Replace these with actual GPIO chip and pins
    CHIP_NAME = "gpiochip4"
    LEFT_PIN_A = 23
    LEFT_PIN_B = 22
    RIGHT_PIN_A = 5
    RIGHT_PIN_B = 6 #determined

    # Initialize encoder readers
    left_encoder = EncoderReader(CHIP_NAME, LEFT_PIN_A, LEFT_PIN_B,260)
    right_encoder = EncoderReader(CHIP_NAME, RIGHT_PIN_A, RIGHT_PIN_B,350)
    
    controller = ArduinoPWMController('/dev/ttyACM0')
    controller.connect()

    case1 = Case1(2,4,6,5,5)

    # Initialize odometry
    odometry = CartOdometry(
        8.1, 15.2,
        left_encoder.get_angle_rad(),
        right_encoder.get_angle_rad()
    )

    # Initialize PID motor controllers
    pid = PIDController(-255, 255)

    left_motor = Motor()
    right_motor = Motor()

    start_time = time.perf_counter()

    try:
        while True:
            # Update encoder readings
            left_encoder.update()
            right_encoder.update()

            ode_input = np.array([left_encoder.get_angle_rad(), right_encoder.get_angle_rad(), left_encoder.get_omega_rad(), right_encoder.get_omega_rad()])

            # Update odometry with current angles
            odometry.update(
                ode_input
            )

            print(f"pose: {Helpers.to_deg_and_round(odometry.get_pose())}")
            print(f"velocity:{Helpers.to_deg_and_round(odometry.get_velocity())}")

            
            # Simulate control loop delay
            time.sleep(0.0008)  # 0.8ms as T

    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        left_encoder.close()
        right_encoder.close()

if __name__ == "__main__":
    main()
