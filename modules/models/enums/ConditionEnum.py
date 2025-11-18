from enum import Enum


class ConditionEnum(Enum):
    EQ = "e"
    NEQ = "ne"
    LT = "l"
    LTE = "le"
    GT = "g"
    GTE = "ge"
    UNCONDITIONAL = "unconditional"