import sys
from rn2483 import Parameters, Radio
import time

TRANSMIT_DATA: str = (
    "VA3INI - This is a test message to test the functionality of the RN2483 transceiver with a long packet containing plenty of data - VA3INI - Packet number follows"
)


def main() -> None:

    if len(sys.argv) != 2:
        print("Must provide the COM port/serial port where the radio is connected.")
        exit(1)

    print(f"Using packet length: {len(TRANSMIT_DATA.encode('ascii'))}")

    params = Parameters.from_json("./config.json")
    print(f"Using parameters: {params}")
    radio = Radio.from_port(params=params, port=sys.argv[1])
    print(f"Configuration succeeded: {radio.configure()}")

    counter = 0
    while True:
        data = f"{TRANSMIT_DATA} - #{counter}"
        print(f"Transmitting: {data}")

        start = time.time()
        if not radio.transmit(data):
            print(f"TRANSMIT FAILED {counter}")
        else:
            end = time.time()
            print(f"Period: {end - start}")
            counter += 1


if __name__ == "__main__":
    main()
