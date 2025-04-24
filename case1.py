import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 車體參數
T = 0.01  # 時間間隔
L = 0.15  # 車體軸距

# 全局變數儲存 simulation 狀態
sim_index = 0
is_running = False
x, y, theta, v, omega, v_l, v_r, time = [], [], [], [], [], [], [], []

# encoder 模擬資料產生
def generate_encoder_data(x_data, y_data, v_l, v_r):
    noise_x = np.random.normal(0, 0.01, size=len(x_data))
    noise_y = np.random.normal(0, 0.01, size=len(y_data))
    noise_l = np.random.normal(0, 0.01, size=len(v_l))
    noise_r = np.random.normal(0, 0.01, size=len(v_r))
    v_l_enc = v_l + noise_l
    v_r_enc = v_r + noise_r
    v_enc = (v_l_enc + v_r_enc) / 2
    omega_enc = (v_r_enc - v_l_enc) / L
    return x_data + noise_x, y_data + noise_y, v_l_enc, v_r_enc, v_enc, omega_enc

# 模擬計算
def simulate_case1(t_change1, t_change2, t_change3, target_speed):
    total_time = 5
    time_array = np.arange(0, total_time + T, T)
    v_array = np.zeros_like(time_array)

    for i, t in enumerate(time_array):
        if t <= t_change1:
            v_array[i] = target_speed * (t / t_change1)
        elif t_change1 < t <= t_change2:
            v_array[i] = target_speed
        elif t_change2 < t <= t_change3:
            v_array[i] = target_speed * (1 - (t - t_change2) / (t_change3 - t_change2))
        else:
            v_array[i] = 0

    omega_array = np.zeros_like(time_array)
    x_array, y_array, theta_array = [0], [0], [0]
    for i in range(1, len(time_array)):
        dx = v_array[i-1] * np.cos(theta_array[-1]) * T
        dy = v_array[i-1] * np.sin(theta_array[-1]) * T
        dtheta = omega_array[i-1] * T
        x_array.append(x_array[-1] + dx)
        y_array.append(y_array[-1] + dy)
        theta_array.append(theta_array[-1] + dtheta)

    x_array = np.array(x_array)
    y_array = np.array(y_array)
    theta_array = np.array(theta_array)
    v_r_array = v_array + omega_array * L / 2
    v_l_array = v_array - omega_array * L / 2

    return time_array, x_array, y_array, theta_array, v_array, omega_array, v_l_array, v_r_array

# 動態繪圖

def update_plot_dynamic():
    global sim_index, is_running
    if not is_running:
        return
    if sim_index < len(time):
        ax1.plot(x[:sim_index], y[:sim_index], 'b-', label="Odometry" if sim_index == 1 else "")
        ax1.plot(x_enc[:sim_index], y_enc[:sim_index], 'r--', label="Encoder" if sim_index == 1 else "")

        ax2.plot(time[:sim_index], v_l[:sim_index], label="Left Wheel" if sim_index == 1 else "")
        ax2.plot(time[:sim_index], v_r[:sim_index], label="Right Wheel" if sim_index == 1 else "")

        ax3.plot(time[:sim_index], v_l_enc[:sim_index], 'c--', label="Enc L" if sim_index == 1 else "")
        ax3.plot(time[:sim_index], v_r_enc[:sim_index], 'm--', label="Enc R" if sim_index == 1 else "")

        ax4.plot(time[:sim_index], v[:sim_index], label="v(t)" if sim_index == 1 else "")
        ax4.plot(time[:sim_index], omega[:sim_index], label="ω(t)" if sim_index == 1 else "")

        ax5.plot(time[:sim_index], v_enc[:sim_index], 'g-', label="Enc v" if sim_index == 1 else "")
        ax5.plot(time[:sim_index], omega_enc[:sim_index], 'k--', label="Enc ω" if sim_index == 1 else "")

        ax1.set_title("Trajectory(XY Graph)")
        ax1.set_xlabel("X (cm)")
        ax1.set_ylabel("Y (cm)")
        ax1.axis('equal')
        ax1.grid(True)
        ax1.legend()

        ax2.set_title("phi dot desired")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("ω (rad/s)")
        ax2.grid(True)
        ax2.legend()

        ax3.set_title("Encoder phi dot")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Encoder ω (rad/s)")
        ax3.grid(True)
        ax3.legend()

        ax4.set_title("v/ω desired")
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel("v(cm/s) / ω(rad/s)")
        ax4.grid(True)
        ax4.legend()

        ax5.set_title("Encoder v/ω ")
        ax5.set_xlabel("Time (s)")
        ax5.set_ylabel("v(cm/s) / ω(rad/s)")
        ax5.grid(True)
        ax5.legend()

        canvas.draw()
        sim_index += 1
        root.after(10, update_plot_dynamic)

# 初始化模擬

def run_simulation():
    global sim_index, x, y, theta, v, omega, v_l, v_r, time, is_running
    global x_enc, y_enc, v_l_enc, v_r_enc, v_enc, omega_enc
    try:
        t1 = float(entry_t1.get())
        t2 = float(entry_t2.get())
        t3 = float(entry_t3.get())
        v_target = float(entry_v.get())
    except ValueError:
        return

    time, x, y, theta, v, omega, v_l, v_r = simulate_case1(t1, t2, t3, v_target)
    x_enc, y_enc, v_l_enc, v_r_enc, v_enc, omega_enc = generate_encoder_data(x, y, v_l, v_r)
    sim_index = 0
    is_running = True
    for ax in (ax1, ax2, ax3, ax4, ax5):
        ax.clear()
    update_plot_dynamic()

# UI 控制

def pause_simulation():
    global is_running
    is_running = False

def stop_simulation():
    root.destroy()

# UI
root = tk.Tk()
root.title("Case 1 Odometry 模擬（含 Encoder 速度與輪速）")
root.geometry("1600x900")

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

for i, (text, default) in enumerate(zip([
    "加速結束時間 (s):", "等速結束時間 (s):", "減速結束時間 (s):", "目標速度 v (cm/s):"],
    ["1.0", "2.5", "4.0", "0.3"])):
    tk.Label(control_frame, text=text).grid(row=0, column=2 * i)
    entry = tk.Entry(control_frame, width=10)
    entry.insert(0, default)
    entry.grid(row=0, column=2 * i + 1)
    globals()[f'entry_t{i+1}' if i < 3 else 'entry_v'] = entry

btn_start = tk.Button(control_frame, text="模擬執行", command=run_simulation)
btn_start.grid(row=0, column=8, padx=5)
btn_pause = tk.Button(control_frame, text="暫停模擬", command=pause_simulation)
btn_pause.grid(row=0, column=9, padx=5)
btn_stop = tk.Button(control_frame, text="結束程式", command=stop_simulation)
btn_stop.grid(row=0, column=10, padx=5)

fig = plt.figure(figsize=(16, 8))
ax1 = fig.add_subplot(2, 3, 1)  # 左半邊軌跡圖
ax2 = fig.add_subplot(2, 3, 2)  # 右上1
ax3 = fig.add_subplot(2, 3, 3)  # 右上2
ax4 = fig.add_subplot(2, 3, 5)  # 右下1
ax5 = fig.add_subplot(2, 3, 6)  # 右下2
fig.tight_layout(pad=4.0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

run_simulation()
root.mainloop()