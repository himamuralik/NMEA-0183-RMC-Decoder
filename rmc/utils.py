
from typing import Final

KNOTS_TO_MPS: Final = 0.514444


def validate_checksum(sentence: str) -> bool:
    if "*" not in sentence:
        return False

    data, checksum = sentence.strip().split("*")
    data = data.lstrip("$")

    calc = 0
    for char in data:
        calc ^= ord(char)

    return f"{calc:02X}" == checksum.upper()


def knots_to_mps(knots: float) -> float:
    return round(knots * KNOTS_TO_MPS, 3)


def dmm_to_decimal(value: str, direction: str) -> float:
    if not value or not direction:
        raise ValueError("Invalid coordinate value")

    if direction in {"N", "S"}:
        degrees = int(value[:2])
        minutes = float(value[2:])
    else:
        degrees = int(value[:3])
        minutes = float(value[3:])

    decimal = degrees + minutes / 60

    if direction in {"S", "W"}:
        decimal *= -1

    return round(decimal, 6)
