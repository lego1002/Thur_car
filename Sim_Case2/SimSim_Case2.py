from Helper import Helpers
from ArduinoPWM import ArduinoPWMController
from Motor_PID import Motor
from Cases_Data import Case2
import numpy as np
import time

def awake():
    print("Initializing hardware and parameters...")

def main():
    awake()
    
    controller = ArduinoPWMController('/dev/ttyACM0')
    controller.connect()

    case2 = Case2(2,4,6,8,10,12,14,16,18,5,5)

    left_motor = Motor()
    right_motor = Motor()

    start_time = time.monotonic()

    try:
        while True:
            current_time = time.monotonic()
            pasted_time = current_time - start_time

            v = case2.v(current_time)
            w = case2.w(current_time)

            left_motor.pwm, right_motor.pwm = Helpers.compute_pwm_from_velocity(v, w, 8.1, 15.2, 1)

            controller.send_pwm(left_motor.pwm, right_motor.pwm)

            # Simulate control loop delay
            time.sleep(0.001)  # 1000 Hz

    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
