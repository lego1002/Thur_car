import matplotlib.pyplot as plt
import math

print("Select a case: 1, 2, or 3")
case = input("Enter case number: ").strip()

v = float(input("Enter forward velocity v (m/s): "))
dtheta = float(input("Enter angular velocity dtheta (rad/s): "))

if case == "1":
    t1 = float(input("t1: "))
    t2 = float(input("t2: "))
    t3 = float(input("t3: "))
    time_points = [0, t1, t2, t3]
    v_list = [v, v, 0]
    w_list = [0, 0, 0]

elif case == "2":
    t = [float(input(f"t{i+1}: ")) for i in range(9)]
    time_points = [0] + t
    v_list = [v, v, 0, 0, 0, v, v, 0]
    w_list = [0, 0, 0, dtheta, dtheta, 0, 0, 0]

elif case == "3":
    t = [float(input(f"t{i+1}: ")) for i in range(7)]
    time_points = [0] + t
    v_list = [v] * 6 + [0]
    w_list = [0, 0, dtheta, dtheta, 0, 0, 0]

else:
    print("Invalid case")
    exit()

# Parameters
dt = 0.05
wheel_base = 0.15

x, y, theta = 0, 0, 0
positions = [(x, y)]
v_plot = []
w_plot = []
vl_plot = []
vr_plot = []

current_time = 0
for i in range(len(time_points) - 1):
    duration = time_points[i+1] - time_points[i]
    steps = int(duration / dt)
    v_seg = v_list[i]
    w_seg = w_list[i]

    for _ in range(steps):
        x += v_seg * math.cos(theta) * dt
        y += v_seg * math.sin(theta) * dt
        theta += w_seg * dt

        v_r = (2 * v_seg + w_seg * wheel_base) / 2
        v_l = (2 * v_seg - w_seg * wheel_base) / 2

        positions.append((x, y))
        v_plot.append(v_seg)
        w_plot.append(w_seg)
        vl_plot.append(v_l)
        vr_plot.append(v_r)

time_series = [i * dt for i in range(len(v_plot))]
x_vals, y_vals = zip(*positions)

plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.plot(x_vals, y_vals, marker='o')
plt.title("XY Trajectory")
plt.xlabel("X (m)")
plt.ylabel("Y (m)")
plt.axis('equal')

plt.subplot(2, 2, 2)
plt.plot(time_series, vl_plot, label='Left Motor')
plt.plot(time_series, vr_plot, label='Right Motor')
plt.title("Motor Speeds")
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(time_series, v_plot, label='Linear Velocity v')
plt.plot(time_series, w_plot, label='Angular Velocity w')
plt.title("Robot Speed")
plt.xlabel("Time (s)")
plt.ylabel("Speed")
plt.legend()

plt.tight_layout()
plt.show()
