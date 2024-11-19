import serial
import time
import datetime

DATA: str = "564133494E490A"


def wait_for_ok(radio: serial.Serial) -> bool:
    line = radio.readline()
    print(f"Radio responded: {line}")
    return "ok" in str(line)


def receive(radio: serial.Serial) -> None:
    print("RECEIVE")
    write_radio(radio, "mac pause")
    wait_for_ok(radio)
    write_radio(radio, "radio rx 0")
    wait_for_ok(radio)

    message = radio.readline()
    if message == b"":
        print("Nothing yet.")
    else:
        print(f"{message}")


def transmit(radio: serial.Serial, data: str) -> None:

    print(f"Transmit: {data}")
    write_radio(radio, "mac pause")
    wait_for_ok(radio)
    write_radio(radio, f"radio tx {data}")
    wait_for_ok(radio)
    wait_for_ok(radio)


def write_radio(radio: serial.Serial, cmd: str) -> None:
    cmd += "\r\n"  # Must include carriage return for valid commands (see DS40001784B pg XX)
    radio.flush()  # Flush the serial port

    _ = radio.write(cmd.encode("utf-8"))


def main():
    radio = serial.Serial(
        port="COM8",
        baudrate=57600,
    )

    write_radio(radio, "radio set mod lora")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set freq 433050000")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set pwr 15")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set sf sf7")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set cr 4/8")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set bw 500")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set crc on")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set iqi off")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set sync 43")
    if not wait_for_ok(radio):
        exit(1)
    write_radio(radio, "radio set prlen 6")
    if not wait_for_ok(radio):
        exit(1)
    print("Set parameters.")
    write_radio(radio, "radio set wdt 0")
    wait_for_ok(radio)

    while True:
        transmit(radio, DATA)
        time.sleep(1)

    # with open("range_test.txt", "w") as file:
    #     while True:
    #         receive(radio)
    #         write_radio(radio, "radio get snr")
    #         snr = str(radio.readline()).strip()
    #         print(f"Time: {datetime.datetime.now()} - SNR: {snr}\n")
    #         file.write(f"Time: {datetime.datetime.now()} - SNR: {snr}\n")


if __name__ == "__main__":
    main()
