import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

T = 0.01
L = 0.15
sim_index = 0
is_running = False

def simulate_case2(v_target, omega_target, times):
    time = np.arange(0, times[-1] + T, T)
    v = np.zeros_like(time)
    omega = np.zeros_like(time)

    for i, t in enumerate(time):
        if t <= times[0]:
            v[i] = v_target * t / times[0]
        elif t <= times[1]:
            v[i] = v_target
        elif t <= times[2]:
            v[i] = v_target * (1 - (t - times[1]) / (times[2] - times[1]))
        elif t <= times[5]:
            v[i] = 0
        elif t <= times[6]:
            v[i] = v_target * (t - times[5]) / (times[6] - times[5])
        elif t <= times[7]:
            v[i] = v_target
        elif t <= times[8]:
            v[i] = v_target * (1 - (t - times[7]) / (times[8] - times[7]))

    for i, t in enumerate(time):
        if t <= times[2]:
            omega[i] = 0
        elif t <= times[3]:
            omega[i] = omega_target * (t - times[2]) / (times[3] - times[2])
        elif t <= times[4]:
            omega[i] = omega_target
        elif t <= times[5]:
            omega[i] = omega_target * (1 - (t - times[4]) / (times[5] - times[4]))
        else:
            omega[i] = 0

    x, y, theta = [0], [0], [0]
    for i in range(1, len(time)):
        dt = T
        th = theta[-1] + omega[i-1] * dt
        dx = v[i-1] * np.cos(theta[-1]) * dt
        dy = v[i-1] * np.sin(theta[-1]) * dt
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
        theta.append(th)

    x = np.array(x)
    y = np.array(y)
    theta = np.array(theta)
    v_r = v + omega * L / 2
    v_l = v - omega * L / 2

    x_enc = x + np.random.normal(0, 0.01, len(x))
    y_enc = y + np.random.normal(0, 0.01, len(y))
    v_l_enc = v_l + np.random.normal(0, 0.01, len(v_l))
    v_r_enc = v_r + np.random.normal(0, 0.01, len(v_r))
    v_enc = (v_l_enc + v_r_enc) / 2
    omega_enc = (v_r_enc - v_l_enc) / L

    return time, x, y, x_enc, y_enc, v, omega, v_l, v_r, v_l_enc, v_r_enc, v_enc, omega_enc

def update_plot_dynamic():
    global sim_index, is_running
    if not is_running:
        return
    if sim_index < len(time):
        ax1.plot(x[:sim_index], y[:sim_index], 'b-', label='Odometry' if sim_index == 1 else "")
        ax1.plot(x_enc[:sim_index], y_enc[:sim_index], 'r--', label='Encoder' if sim_index == 1 else "")

        ax2.plot(time[:sim_index], v_l[:sim_index], label='Left Wheel' if sim_index == 1 else "")
        ax2.plot(time[:sim_index], v_r[:sim_index], label='Right Wheel' if sim_index == 1 else "")
        ax3.plot(time[:sim_index], v_l_enc[:sim_index], 'c--', label='Enc L' if sim_index == 1 else "")
        ax3.plot(time[:sim_index], v_r_enc[:sim_index], 'm--', label='Enc R' if sim_index == 1 else "")
        ax4.plot(time[:sim_index], v[:sim_index], label='v(t)' if sim_index == 1 else "")
        ax4.plot(time[:sim_index], omega[:sim_index], label='ω(t)' if sim_index == 1 else "")
        ax5.plot(time[:sim_index], v_enc[:sim_index], 'g-', label='Enc v' if sim_index == 1 else "")
        ax5.plot(time[:sim_index], omega_enc[:sim_index], 'k--', label='Enc ω' if sim_index == 1 else "")

        for ax in [ax1, ax2, ax3, ax4, ax5]:
            ax.grid(True)
            ax.legend()

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

def run_simulation():
    global sim_index, is_running, time, x, y, x_enc, y_enc, v, omega, v_l, v_r, v_l_enc, v_r_enc, v_enc, omega_enc
    try:
        v_target = float(entry_v.get())
        omega_target = float(entry_omega.get())
        times = [float(e.get()) for e in entries_t]
    except ValueError:
        return

    time, x, y, x_enc, y_enc, v, omega, v_l, v_r, v_l_enc, v_r_enc, v_enc, omega_enc = simulate_case2(v_target, omega_target, times)
    sim_index = 0
    is_running = True
    for ax in (ax1, ax2, ax3, ax4, ax5):
        ax.clear()
    update_plot_dynamic()

def pause_simulation():
    global is_running
    is_running = False

def stop_simulation():
    root.destroy()

root = tk.Tk()
root.title("Case 2 Odometry 模擬 UI（完整排版）")
root.geometry("1600x900")

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

entries_t = []
tk.Label(control_frame, text="時間點 t1~t9 (秒):").grid(row=0, column=0, padx=5, columnspan=10)
for i in range(9):
    tk.Label(control_frame, text=f"t{i+1}").grid(row=1, column=i+1)
    et = tk.Entry(control_frame, width=6)
    et.insert(0, str((i + 1)))
    et.grid(row=2, column=i+1)
    entries_t.append(et)

tk.Label(control_frame, text="直線速度 v(cm/s):").grid(row=3, column=0)
entry_v = tk.Entry(control_frame, width=6)
entry_v.insert(0, "0.3")
entry_v.grid(row=3, column=1)

tk.Label(control_frame, text="角速度 ω(rad/s):").grid(row=3, column=2)
entry_omega = tk.Entry(control_frame, width=6)
entry_omega.insert(0, "0.6")
entry_omega.grid(row=3, column=3)

btn_start = tk.Button(control_frame, text="模擬執行", command=run_simulation)
btn_start.grid(row=3, column=5, padx=10)
btn_pause = tk.Button(control_frame, text="暫停模擬", command=pause_simulation)
btn_pause.grid(row=3, column=6, padx=10)
btn_stop = tk.Button(control_frame, text="結束程式", command=stop_simulation)
btn_stop.grid(row=3, column=7, padx=10)

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