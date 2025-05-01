import gpiod
import time

class EncoderReader:
    def __init__(self, chip_name, pin_a, pin_b, counts_per_rev=396, debounce=0.002):
        self.count = 0
        self.last_ts = None
        self.last_count = 0
        self.last_time = time.monotonic()
        self.counts_per_rev = counts_per_rev
        self.debounce = debounce

        self.omega_deg = 0.0
        self.omega_rad = 0.0

        # GPIO 初始化
        self.chip = gpiod.Chip(chip_name)
        self.lineA = self.chip.get_line(pin_a)
        self.lineB = self.chip.get_line(pin_b)
        self.lineA.request(consumer='encA', type=gpiod.LINE_REQ_EV_RISING_EDGE)
        self.lineB.request(consumer='encB', type=gpiod.LINE_REQ_DIR_IN)

    def update(self):
        """若 A 相有事件，則更新計數與角速度"""
        if not self.lineA.event_wait(sec=0):  # 非阻塞
            return

        ev = self.lineA.event_read()
        ts = time.monotonic()
        if self.last_ts is not None and (ts - self.last_ts) < self.debounce:
            return
        self.last_ts = ts

        # 根據 B 相判斷方向
        b = self.lineB.get_value()
        self.count += 1 if b == 1 else -1

        # 更新角速度
        dt = ts - self.last_time
        if dt > 0:
            dcount = self.count - self.last_count
            dangle_deg = (dcount / self.counts_per_rev) * 360.0
            dangle_rad = (dcount / self.counts_per_rev) * 2 * 3.1415926

            self.omega_deg = dangle_deg / dt
            self.omega_rad = dangle_rad / dt

            self.last_time = ts
            self.last_count = self.count

    def get_count(self):
        return self.count

    def get_angle_deg(self):
        return (self.count / self.counts_per_rev) * 360.0

    def get_angle_rad(self):
        return (self.count / self.counts_per_rev) * 2 * 3.1415926

    def get_omega_deg(self):
        return self.omega_deg

    def get_omega_rad(self):
        return self.omega_rad

    def reset(self):
        self.count = 0
        self.last_count = 0
        self.omega_deg = 0.0
        self.omega_rad = 0.0
        self.last_time = time.monotonic()

    def close(self):
        self.lineA.release()
        self.lineB.release()
