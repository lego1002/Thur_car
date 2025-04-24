import gpiod
import time

CHIP_NAME = "gpiochip4"
chip = gpiod.Chip(CHIP_NAME)

num_lines = chip.num_lines()
requested_lines = []

# 預先請求所有 GPIO 為輸入模式
for i in range(num_lines):
    try:
        line = chip.get_line(i)
        line.request(consumer="gpio_scan", type=gpiod.LINE_REQ_DIR_IN)
        requested_lines.append((i, line))
    except OSError:
        print(f"GPIO {i} 無法請求（可能是保留腳位）")

print(f"正在掃描 {CHIP_NAME} 上的 GPIO 狀態（每 0.5 秒更新一次）")
print("按 Ctrl+C 停止")

try:
    while True:
        print("-" * 40)
        for idx, line in requested_lines:
            val = line.get_value()
            print(f"GPIO {idx:2d}: {'HIGH 高電位' if val else 'LOW 低電位'}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("結束掃描")

finally:
    for _, line in requested_lines:
        line.release()
