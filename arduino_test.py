import serial
import time

arduino = serial.Serial("COM9", 9600, timeout=1)

time.sleep(2)

print("Connected to Arduino!")
print("Waiting for vehicle detection...\n")

while True:
    if arduino.in_waiting:
        message = arduino.readline().decode("utf-8", errors="ignore").strip()

        if message:
            print("Arduino:", message)