from dataclasses import dataclass
from serial import Serial
from typing import Self
import json

BAUDRATE: int = 57600


@dataclass
class Parameters:
    """RN2483 configuration parameters."""

    modulation: str = "lora"
    frequency: int = 433050000
    txpwr: int = 15
    spread_factor: int = 7
    coding_rate: int = 8  # 5 - 8 (becomes denominator of the coding rate fraction)
    bandwidth: int = 500
    crc: bool = True
    iqi: bool = False
    sync: int = 67  # In decimal
    preamble: int = 6

    @classmethod
    def from_json(cls, path: str) -> Self:
        with open(path, "r") as file:
            config = json.load(file)

        return cls(
            modulation=config["modulation"],
            frequency=config["frequency"],
            txpwr=config["txpwr"],
            spread_factor=config["spread_factor"],
            coding_rate=config["coding_rate"],
            bandwidth=config["bandwidth"],
            crc=config["crc"],
            iqi=config["iqi"],
            sync=config["sync"],
            preamble=config["preamble"],
        )


class Radio:
    """Represents the RN2483 radio module."""

    def __init__(self, port: Serial, params: Parameters):
        self.port = port
        self.params = params

    def _write(self, data: str) -> None:
        """Write data to the radio."""
        cmd = f"{data}\r\n"
        self.port.flush()
        self.port.write(cmd.encode("utf-8"))

    def _wait_for_ok(self) -> bool:
        """Returns true for okay, false otherwise."""
        line = self.port.readline()
        return "ok" in str(line)

    def _mac_pause(self) -> bool:
        """Pause the MAC layer."""
        self._write("mac pause")
        line = self.port.readline()
        return "4294967245" in str(line)

    def receive(self) -> str:
        if not self._mac_pause():
            return ""
        self._write("radio rx 0")
        if not self._wait_for_ok():
            return ""

        message = self.port.readline().decode("ascii")[8:].strip()
        if len(message) == 0:
            return ""

        message = bytes.fromhex(message).decode("ascii")
        return message

    def transmit(self, data: str) -> bool:
        if not self._mac_pause():
            return False

        # Encode data to string of hex TODO
        data_str = ""
        for b in data.encode("ascii"):
            data_str += hex(b)[2:]

        self._write(f"radio tx {data_str}")
        if not self._wait_for_ok():
            return False

        # Wait for response of successful TX
        line = ""
        while "radio_tx_ok" not in line:
            line = str(self.port.readline())
        return True

    def configure(self) -> bool:
        """Configure the radio parameters."""

        self._write(f"radio set mod {self.params.modulation}")
        if not self._wait_for_ok():
            return False

        self._write(f"radio set freq {self.params.frequency}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set pwr {self.params.txpwr}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set sf sf{self.params.spread_factor}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set cr 4/{self.params.coding_rate}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set bw {self.params.bandwidth}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set crc {'on' if self.params.crc else 'off'}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set iqi {'on' if self.params.iqi else 'off'}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set sync {str(hex(self.params.sync))[2:]}")
        if not self._wait_for_ok():
            return False
        self._write(f"radio set prlen {self.params.preamble}")
        if not self._wait_for_ok():
            return False

        return True

    def snr(self) -> str:
        self._write("radio get snr")
        return str(self.port.readline())

    @classmethod
    def from_port(cls, port: str, params: Parameters) -> Self:
        return cls(
            port=Serial(port=port, baudrate=BAUDRATE),
            params=params,
        )
