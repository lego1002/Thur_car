import matplotlib.pyplot as plt
import math
import os

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

def get_next_filename(prefix="odometry_graph_", ext=".png"):
    i = 1
    while True:
        filename = f"{prefix}{i}{ext}"
        if not os.path.exists(filename):
            return filename
        i += 1

def run_odometry_and_plot(time_points, v_list, w_list, dt=0.05, wheel_base=0.15):
    x, y, theta = 0.0, 0.0, 0.0
    positions = [(x, y)]
    v_plot, w_plot, vl_plot, vr_plot, time_series = [], [], [], [], []

    current_time = 0.0
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

            positions.append((x, y))
            v_plot.append(v)
            w_plot.append(w)
            vl_plot.append(v_l)
            vr_plot.append(v_r)
            time_series.append(current_time)

            current_time += dt

    # === Plotting ===
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    x_vals, y_vals = zip(*positions)

    axs[0, 0].plot(x_vals, y_vals, marker='o')
    axs[0, 0].set_title("XY Trajectory")
    axs[0, 0].set_xlabel("X (m)")
    axs[0, 0].set_ylabel("Y (m)")
    axs[0, 0].axis('equal')

    axs[0, 1].plot(time_series, vl_plot, label='Left Motor')
    axs[0, 1].plot(time_series, vr_plot, label='Right Motor')
    axs[0, 1].set_title("Motor Speeds")
    axs[0, 1].set_xlabel("Time (s)")
    axs[0, 1].set_ylabel("Speed (m/s)")
    axs[0, 1].legend()

    axs[1, 0].plot(time_series, v_plot, label='Linear Velocity v')
    axs[1, 0].plot(time_series, w_plot, label='Angular Velocity w')
    axs[1, 0].set_title("Robot Speeds")
    axs[1, 0].set_xlabel("Time (s)")
    axs[1, 0].set_ylabel("Speed")
    axs[1, 0].legend()

    axs[1, 1].axis('off')
    axs[1, 1].text(0.1, 0.5,
                   f"Final Position:\nX = {x:.3f} m\nY = {y:.3f} m\nTheta = {theta:.3f} rad",
                   fontsize=14, verticalalignment='center')

    plt.tight_layout()
    filename = get_next_filename()
    plt.savefig(filename)
    plt.close()
    print(f"\nSaved graph to {filename}")

# === Run ===
data = get_case_data()
if data:
    run_odometry_and_plot(*data)
