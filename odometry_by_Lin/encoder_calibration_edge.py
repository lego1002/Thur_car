# encoder_calibration_edge.py
import gpiod
import time

CHIP = 'gpiochip4'
PIN_A, PIN_B = 22, 23
DEBOUNCE = 0.002   # 2ms 去彈跳

chip = gpiod.Chip(CHIP)
lineA = chip.get_line(PIN_A)
lineB = chip.get_line(PIN_B)
lineA.request(consumer='calA', type=gpiod.LINE_REQ_EV_RISING_EDGE)
lineB.request(consumer='calB', type=gpiod.LINE_REQ_DIR_IN)

count = 0
last_ts = None

print("校正開始：慢速轉動輪子一圈，完成後 Ctrl+C 結束…")
try:
    while True:
        if not lineA.event_wait(sec=2):
            continue
        ev = lineA.event_read()
        ts = time.monotonic()
        if last_ts is not None and (ts - last_ts) < DEBOUNCE:
            continue
        last_ts = ts

        b = lineB.get_value()
        count += 1 if b==1 else -1
        print(f"\rCount: {count:>4d}", end="")

except KeyboardInterrupt:
    print(f"\n→ 單邊緣模式整圈總脈衝：{count}")
    print(f"   ※ 之後請把 counts_per_rev 設為 {abs(count)}")
finally:
    lineA.release()
    lineB.release()

