import serial
import time
import sys

# Adjust COM port and baudrate if needed
PORT = "COM3"        # <-- change to your actual COM port
BAUDRATE = 57600     # RN2483 default is 57600 baud

def send_cmd(radio, cmd, delay=0.2):
    """Send a command and return response line."""
    radio.write((cmd + "\r\n").encode("utf-8"))
    time.sleep(delay)
    resp = radio.read_all().decode("utf-8").strip()
    return resp

def main():
    try:
        radio = serial.Serial(PORT, BAUDRATE, timeout=1)
    except Exception as e:
        print(f"Failed to open {PORT}: {e}")
        sys.exit(1)

    # Flush any junk
    radio.reset_input_buffer()
    radio.reset_output_buffer()

    # Step 1: check connection
    resp = send_cmd(radio, "sys get ver")
    if resp and "RN2483" in resp:
        print("Successfully connected to RN2483")
    else:
        print("No response from RN2483, check wiring/port.")
        sys.exit(1)

    # Step 2: pause MAC (LoRaWAN stack)
    print("Pausing LoRaWAN stack...")
    print(">>", send_cmd(radio, "mac pause"))

    # Step 3: configure FSK modulation
    print("Switching to FSK...")
    print(">>", send_cmd(radio, "radio set mod fsk"), " --> setting the Modulation to FSK")
    print(">>", send_cmd(radio, "radio set freq 868000000"), " --> setting the freq to 868000000")  # adjust region # Using EU (868 MHz band)
    print(">>", send_cmd(radio, "radio set bitrate 50000"), " --> setting the bits per sec to 50000")
    print(">>", send_cmd(radio, "radio set fdev 25000"), " --> setting the freq dev to 25000")
    print(">>", send_cmd(radio, "radio set rxbw 125"), " --> setting the receiver bw to 125")
    print(">>", send_cmd(radio, "radio set afcbw 41.7"), " --> setting the AFC bw to 41.7")
    print(">>", send_cmd(radio, "radio set prlen 8"), " --> setting the praamble length to 8")
    print(">>", send_cmd(radio, "radio set crc on"), " --> enablling CRC for packets")
    print(">>", send_cmd(radio, "radio set sync 12AABBCCDD"), " --> setting up to 8 bytes sync word")
    print(">>", send_cmd(radio, "radio set bt 0.5"), " --> setting Gaussian bt to 0.5")
    print(">>", send_cmd(radio, "radio set pwr 14"), " --> TX power (dbm) to 14")

    # Optional: test transmit (payload "Hello")
    print("Sending test TX...")
    print(">>", send_cmd(radio, "radio tx 48656C6C6F"))

    radio.close()

if __name__ == "__main__":
    main()
