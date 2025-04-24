import math
import os
import csv

def get_case_data():
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
        print("Invalid case.")
        return None

    return time_points, v_list, w_list

def get_next_filename(prefix="date_", ext=".csv"):
    i = 1
    while True:
        filename = f"{prefix}{i}{ext}"
        if not os.path.exists(filename):
            return filename
        i += 1

def run_odometry(time_points, v_list, w_list, dt=0.05, wheel_base=0.15):
    x, y, theta = 0.0, 0.0, 0.0
    current_time = 0.0
    log_rows = []

    print("\n--- Simulation Start ---")
    print(f"{'Time':>6} {'X':>7} {'Y':>7} {'Theta':>7} {'vL':>7} {'vR':>7} {'v':>7} {'w':>7}")
    for i in range(len(time_points) - 1):
        duration = time_points[i + 1] - time_points[i]
        steps = int(duration / dt)
        v = v_list[i]
        w = w_list[i]

        for _ in range(steps):
            x += v * math.cos(theta) * dt
            y += v * math.sin(theta) * dt
            theta += w * dt

            v_r = (2 * v + w * wheel_base) / 2
            v_l = (2 * v - w * wheel_base) / 2

            print(f"{current_time:6.2f} {x:7.3f} {y:7.3f} {theta:7.3f} {v_l:7.3f} {v_r:7.3f} {v:7.3f} {w:7.3f}")
            log_rows.append([round(current_time, 3), round(x, 3), round(y, 3), round(theta, 3),
                             round(v_l, 3), round(v_r, 3), round(v, 3), round(w, 3)])
            current_time += dt

    print("\n--- Simulation End ---")
    print(f"Final Position: x = {x:.3f} m, y = {y:.3f} m, theta = {theta:.3f} rad")

    filename = get_next_filename()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'x', 'y', 'theta', 'vL', 'vR', 'v', 'w'])
        writer.writerows(log_rows)

    print(f"Saved CSV to {filename}")

# 主程式
data = get_case_data()
if data:
    run_odometry(*data)
