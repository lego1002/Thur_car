import serial
import time

class ArduinoPWMController:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # 等待 Arduino 重啟
            print(f"[INFO] Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            print(f"[ERROR] Failed to connect to Arduino: {e}")

    def send_pwm(self, pwm1: int, pwm2: int):
        if self.ser and self.ser.is_open:
            pwm1 = max(0, min(255, pwm1))
            pwm2 = max(0, min(255, pwm2))
            data = f"{pwm1},{pwm2}\n"
            self.ser.write(data.encode('utf-8'))
            print(f"[DEBUG] Sent: {data.strip()}")
        else:
            print("[ERROR] Serial connection not available.")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("[INFO] Serial connection closed.")

