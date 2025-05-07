from Helper import Helpers
from ArduinoPWM import ArduinoPWMController
from Motor_PID import Motor
from Cases_Data import Case1
import numpy as np
import time

def awake():
    print("Initializing hardware and parameters...")

def main():
    awake()
    
    controller = ArduinoPWMController('/dev/ttyACM0')
    controller.connect()

    case1 = Case1(2,9,11,20,0)

    left_motor = Motor()
    right_motor = Motor()
    time.sleep(1)
    start_time = time.monotonic()

    try:
        while True:
            current_time = time.monotonic()
            pasted_time = current_time - start_time

            v = case1.v(pasted_time)
            w = case1.w(pasted_time)


            output = Helpers.compute_pwm_from_velocity(v, w, 8.0, 15.2, 80)
            left_motor.pwm = output[0]
            right_motor.pwm = output[1]
            controller.send_pwm(left_motor.pwm*1.05, right_motor.pwm )

            print(current_time)
            # Simulate control loop delay
            time.sleep(0.001)  # 1000 Hz

    except KeyboardInterrupt:
        print("Shutting down.")

if __name__ == "__main__":
    main()
