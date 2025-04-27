import gpiod
import math

class ABEncoder:
    def __init__(self, pulses_per_phase_per_rev=11):
        self.counts_per_rev = pulses_per_phase_per_rev * 4  # 4x decoding
        self.countor = 0
        self.last_state = 0b00  # (A << 1) | B

        # 4-bit transition key: (old_state << 2) | new_state : delta
        self.lookup = {
            0b0001: 1,  0b0010: -1,
            0b0100: -1, 0b0111: 1,
            0b1000: 1,  0b1011: -1,
            0b1101: -1, 0b1110: 1
        }

    def update(self, a: int, b: int):
        #Call this whenever A/B inputs change
        current_state = (a << 1) | b
        transition = (self.last_state << 2) | current_state
        delta = self.lookup.get(transition, 0)
        self.countor += delta
        self.last_state = current_state

    def reset(self):
        self.countor = 0

    def get_degrees(self):
        #Return current rotation in degrees
        return (self.countor / self.counts_per_rev) * 360
    
    def get_radians(self):
        #Return current rotation in radians
        return (self.countor / self.counts_per_rev) * (2 * math.pi)

    def get_revolutions(self):
        #Return total revolutions (can be negative)
        return self.countor / self.counts_per_rev


#---------------------------------------------------------------------------------

# GPIO 設定
CHIP_NAME = "gpiochip4"  # 請根據實際 Raspberry Pi 5 上的 gpiochip 名稱確認，可能是 gpiochip0、gpiochip4 等
PIN_A = 22  # GPIO17，請根據實際接線修改
PIN_B = 23  # GPIO27，請根據實際接線修改

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
   