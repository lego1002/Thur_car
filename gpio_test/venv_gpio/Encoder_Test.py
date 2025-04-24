import time
import gpiod
from ABEncoder import ABEncoder  # 假設 ABEncoder 放在 abencoder.py

# GPIO 設定
CHIP_NAME = "gpiochip4"  # 請根據實際 Raspberry Pi 5 上的 gpiochip 名稱確認，可能是 gpiochip0、gpiochip4 等
PIN_A = 17  # GPIO17，請根據實際接線修改
PIN_B = 27  # GPIO27，請根據實際接線修改

# 初始化 GPIOD
chip = gpiod.Chip(CHIP_NAME)
lines = chip.get_lines([PIN_A, PIN_B])
lines.request(consumer="ab_encoder_reader", type=gpiod.LINE_REQ_EV_BOTH_EDGES)

# 初始化 ABEncoder
encoder = ABEncoder(pulses_per_phase_per_rev=11)

print("Reading encoder... Press Ctrl+C to stop.")
try:
    while True:
        # 等待 A/B 線任一變化
        event = lines.event_wait(sec=1)
        if event:
            values = lines.get_values()
            a_val, b_val = values[0], values[1]
            encoder.update(a_val, b_val)
            degrees = encoder.get_degrees()
            print(f"Angle: {degrees:.2f}°")
        else:
            print("Timeout waiting for encoder change.")

except KeyboardInterrupt:
    print("Stopping encoder reading.")
finally:
    lines.release()
