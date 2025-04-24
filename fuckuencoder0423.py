import gpiod
import time

CHIP_NAME = "gpiochip4"
chip = gpiod.Chip(CHIP_NAME)

# GPIO 腳位對應設定
LEFT_A = 22
LEFT_B = 23
RIGHT_A = 5
RIGHT_B = 6

# 建立 GPIO 物件
lines = {
    "LEFT_A": chip.get_line(LEFT_A),
    "LEFT_B": chip.get_line(LEFT_B),
    "RIGHT_A": chip.get_line(RIGHT_A),
    "RIGHT_B": chip.get_line(RIGHT_B)
}

# 請求作為輸入使用
for name, line in lines.items():
    line.request(consumer="encoder_test", type=gpiod.LINE_REQ_DIR_IN)

print("開始監聽 Encoder 腳位，轉動馬達會顯示變化（按 Ctrl+C 離開）")

# 初始化狀態
prev = {name: lines[name].get_value() for name in lines}

try:
    while True:
        for name, line in lines.items():
            val = line.get_value()
            if val != prev[name]:
                print(f"{name} changed to {'HIGH' if val else 'LOW'}")
                prev[name] = val
        time.sleep(0.001)  # 短暫延遲避免吃太多 CPU

except KeyboardInterrupt:
    print("結束監聽")

finally:
    for line in lines.values():
        line.release()
