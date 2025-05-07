# test_right.py
import gpiod, time

# 這裡先用 chip0，offset 5=BCM5，6=BCM6
chip = gpiod.Chip('gpiochip4')
lineA = chip.get_line(5)            # BCM5 (A 相)
lineB = chip.get_line(6)            # BCM6 (B 相)
lineA.request(consumer='tR', type=gpiod.LINE_REQ_EV_RISING_EDGE)
lineB.request(consumer='tR', type=gpiod.LINE_REQ_DIR_IN)
print("右輪測試：慢速正/反轉輪子，Ctrl+C 停止")
try:
    while True:
        if lineA.event_wait(sec=1):
            ev = lineA.event_read()
            lvl = lineB.get_value()
            print(f"Event! B={lvl}")
except KeyboardInterrupt:
    pass
finally:
    lineA.release()
    lineB.release()

