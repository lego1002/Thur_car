from Encoder_Test import EncoderReader
from Cart_Odometry import CartOdometry
from Motor_PID import PIDController
from Motor_PID import Motor
from Helper import Helpers
from ArduinoPWM import ArduinoPWMController
from Cases_Data import Case2
import numpy as np
import time

def awake():
    print("Initializing hardware and parameters...")

def main():
    awake()

    # Replace these with actual GPIO chip and pins
    CHIP_NAME = "gpiochip0"
    LEFT_PIN_A = 6
    LEFT_PIN_B = 5
    RIGHT_PIN_A = 23
    RIGHT_PIN_B = 24 #determined

    # Initialize encoder readers
    left_encoder = EncoderReader(CHIP_NAME, LEFT_PIN_A, LEFT_PIN_B)
    right_encoder = EncoderReader(CHIP_NAME, RIGHT_PIN_A, RIGHT_PIN_B)
    
    controller = ArduinoPWMController('/dev/ttyACM0')
    controller.connect()

    case2 = Case2(2,4,6,8,10,12,14,16,18,5,5)

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

    start_time = time.monotonic()

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

            vel_mag = Helpers._3vecto2vec(odometry.get_velocity())

            current_time = time.monotonic()
            pasted_time = current_time - start_time

            v = case2.v(current_time)
            w = case2.w(current_time)

            pid1 = pid.update(vel_mag[0], 1, 0, 0, v, 0.001)
            pid2 = pid.update(vel_mag[1], 1, 0, 0, w, 0.001)

            left_motor.pwm, right_motor.pwm += Helpers.compute_pwm_from_velocity(pid1, pid2, 8.1, 15.2, 1)
            
            controller.send_pwm(left_motor.pwm, right_motor.pwm)

            # Simulate control loop delay
            time.sleep(0.0008)  # 1000 Hz

    except KeyboardInterrupt:
        print("Shutting down.")
    finally:
        left_encoder.close()
        right_encoder.close()

if __name__ == "__main__":
    main()
