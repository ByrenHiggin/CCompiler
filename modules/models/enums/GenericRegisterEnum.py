from enum import Enum

class GenericRegisterEnum(Enum):
    AX = "AX"
    DX = "DX"
    R10 = "R10"
    R11 = "R11"
    def from_reg_label(label: str) -> "GenericRegisterEnum":
        val = label.split(".").pop()
        return GenericRegisterEnum[val]