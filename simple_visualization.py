import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

ser = None
data = []

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(0.5)  # Wait for connection to stabilize
except serial.SerialException as e:
    print(f"Error: Could not open serial port /dev/ttyUSB0")
    print(f"Details: {e}")
    print("\nTroubleshooting:")
    print("1. Check if another process is using the port: lsof /dev/ttyUSB0")
    print("2. Close any serial monitors or IDEs")
    print("3. Try reconnecting the USB device")
    exit(1)

def update(i):
    global ser
    try:
        if ser and ser.is_open:
            line = ser.readline().decode().strip()

            if line.isdigit():
                value = int(line)
                data.append(value)

                if len(data) > 100:
                    data.pop(0)

                plt.cla()
                plt.plot(data)
                plt.ylim(0, 200)
                plt.title("Ultrasonic Distance Graph")
                plt.xlabel("Samples")
                plt.ylabel("Distance (cm)")
    except Exception as e:
        print(f"Error reading from serial: {e}")

try:
    ani = animation.FuncAnimation(plt.gcf(), update, interval=100)
    plt.show()
finally:
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")