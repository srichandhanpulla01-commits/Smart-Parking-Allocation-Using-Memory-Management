import serial
import time

arduino = serial.Serial("COM9", 9600, timeout=1)

time.sleep(2)

print("Connected to Arduino")
print("Sending OPEN_GATE...")

arduino.write(b"OPEN_GATE\n")

time.sleep(1)

while arduino.in_waiting:
    message = arduino.readline().decode("utf-8", errors="ignore").strip()
    if message:
        print("Arduino:", message)

arduino.close()

print("Test finished")