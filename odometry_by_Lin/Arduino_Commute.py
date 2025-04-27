import serial  # Required for serial communication with Arduino

class ArduinoCommunicator:
    """
    A class to handle communication with an Arduino board over serial.
    This class is responsible for establishing and managing the serial connection,
    and sending commands (like PWM values) to the Arduino.  It is decoupled from
    the PID control logic.

    Attributes:
        arduino_port (str): The serial port where the Arduino is connected (e.g., '/dev/ttyACM0').
        serial_baudrate (int): The baud rate for serial communication with the Arduino.
        serial_connection (serial.Serial): The serial connection object.

    Methods:
        connect(): Establishes a serial connection with the Arduino.
        disconnect(): Closes the serial connection with the Arduino.
        send_pwm(pwm_value): Sends the PWM value to the Arduino.
    """

    def __init__(self, arduino_port='/dev/ttyACM0', serial_baudrate=115200):
        """
        Initializes the ArduinoCommunicator.

        Args:
            arduino_port (str, optional): The serial port of the Arduino. Defaults to '/dev/ttyACM0'.
            serial_baudrate (int, optional): Baud rate for serial communication. Defaults to 115200.
        """
        self.arduino_port = arduino_port
        self.serial_baudrate = serial_baudrate
        self.serial_connection = None

    def connect(self):
        """
        Establishes a serial connection with the Arduino.
        Handles potential errors and raises an exception if the connection fails.
        """
        try:
            self.serial_connection = serial.Serial(self.arduino_port, self.serial_baudrate, timeout=1)
            print(f"Connected to Arduino on {self.arduino_port} at {self.serial_baudrate} baud.")
            time.sleep(2)  # Allow time for the connection to initialize
        except serial.SerialException as e:
            print(f"Error: Could not connect to Arduino: {e}")
            self.serial_connection = None  # Ensure it's None if connection fails
            raise  # Re-raise the exception to stop execution if connection is critical

    def disconnect(self):
        """
        Closes the serial connection with the Arduino.
        """
        if self.serial_connection:
            self.serial_connection.close()
            print("Disconnected from Arduino.")
            self.serial_connection = None

    def send_pwm(self, pwm_value):
        """
        Sends the PWM value to the Arduino.  Includes error handling.

        Args:
            pwm_value (int): The PWM value to send.
        """
        if self.serial_connection is None:
            print("Error: Serial connection to Arduino not established.  Call connect() first.")
            return

        try:
            # Ensure pwm_value is an integer
            pwm_value = int(pwm_value)
            self.serial_connection.write(f"{pwm_value}\n".encode('utf-8'))
            #print(f"Sent PWM: {pwm_value}") #for debugging
        except serial.SerialException as e:
            print(f"Error sending PWM to Arduino: {e}")
            self.disconnect()  # Clean up the connection.
            self.serial_connection = None
            raise  # re-raise the exception