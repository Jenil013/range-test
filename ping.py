# To ping the Board  (Change the PORT to whichever port it is connected to)

import serial
import time

# Change COM3 if your port is different
PORT = "COM3"
BAUD = 57600
cmd = "sys reset"  +  "\r\n" # Write the cmd to ping it to RN2483

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)

    # Give the RN2483 a moment to initialize
    time.sleep(5)

    # Send a command
    ser.write(cmd.encode("utf-8"))

    # Read response
    response = ser.read(100)  # read up to 100 bytes
    print("Response:", response.decode(errors="ignore"))

    ser.close()

except Exception as e:
    print("Error:", e)
