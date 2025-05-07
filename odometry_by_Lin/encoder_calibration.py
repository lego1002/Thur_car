# encoder_calibration.py
# 校正 ABEncoder 原始 PPR
# 步驟：
#   1. 確認 ABEncoder.py 已包含 debounce_time 參數
#   2. 執行此程式，慢速手動完整旋轉一圈
#   3. 旋轉完成後按 Ctrl+C 結束，程式會顯示 raw counts 與推算 PPR

import gpiod
import time

# 請確保 ABEncoder.py 與此檔案位於同一資料夾
from ABEncoder import ABEncoder

# --- GPIO 參數，請依實際接線修改 ---
CHIP_NAME = 'gpiochip4'
PIN_A = 22  # A 相 (BCM 編號)
PIN_B = 23  # B 相 (BCM 編號)

# --- 實例化 ABEncoder ---
# 建議把 debounce_time 調大一點，避免手動慢速旋轉時的 bounce
encoder = ABEncoder(pulses_per_phase_per_rev=11, debounce_time=0.005)
# 重置計數器與狀態
encoder.reset()

# --- 初始化 GPIO Event ---
chip = gpiod.Chip(CHIP_NAME)
lines = chip.get_lines([PIN_A, PIN_B])
lines.request(consumer='calibration', type=gpiod.LINE_REQ_EV_BOTH_EDGES)

print("開始校正：慢速手動旋轉一圈，完成後按 Ctrl+C 結束")

last_ts = None
try:
    while True:
        # 阻塞等候 A/B 任意邊緣事件，timeout 2 秒
        if not lines.event_wait(sec=2):
            continue  # 若超時可繼續等待
        ts = time.monotonic()
        # 忽略過快的重複事件
        if last_ts and (ts - last_ts) < encoder.debounce_time:
            continue
        last_ts = ts

        # 讀取 A/B 當前值並更新
        a, b = lines.get_values()
        encoder.update(a, b)

        # 顯示即時 count
        count = encoder.get_counter()
        print(f"\rCurrent count: {count:>6d}", end="")

except KeyboardInterrupt:
    # Ctrl+C 結束時，計算並顯示結果
    total_counts = encoder.get_counter()
    print("\n校正完成！")
    print(f"Raw counts (4x) for one revolution: {total_counts}")
    base_ppr = total_counts / 4
    print(f"=> 推算 base PPR = {base_ppr:.2f} (counts/4)")
    # 若有機械減速，請用 base_ppr / gear_ratio

finally:
    lines.release()
