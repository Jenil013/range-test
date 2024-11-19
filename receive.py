import sys
from rn2483 import Parameters, Radio


def main() -> None:

    if len(sys.argv) != 2:
        print("Must provide the COM port/serial port where the radio is connected.")
        exit(1)

    params = Parameters.from_json("./config.json")
    print(f"Using parmeters: {params}")
    radio = Radio.from_port(params=params, port=sys.argv[1])
    print(f"Configuration succeeded: {radio.configure()}")

    while True:
        print(f"Received: {radio.receive()}")
        print(f"SNR: {radio.snr()}")


if __name__ == "__main__":
    main()
