import serial
import csv
import time

# Set up Serial connection (adjust COM port if needed)
ser = serial.Serial('COM10', 115200, timeout=1)  # Windows ('COMx'), macOS/Linux ('/dev/ttyUSBx')
time.sleep(2)  # Give time for connection

# Open a CSV file for writing
with open('gyroscope_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time(ms)", "GyroX", "GyroY", "GyroZ"])  # CSV Header

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line and "Time(ms)" not in line:  # Ignore headers
                data = line.split(',')
                writer.writerow(data)
                print(data)  # Print data to console
        except KeyboardInterrupt:
            print("\nData collection stopped.")
            break  # Stop when user interrupts (Ctrl+C)

ser.close()
