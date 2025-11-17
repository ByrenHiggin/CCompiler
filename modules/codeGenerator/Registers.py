from pydantic import BaseModel

from modules.models.enums.GenericRegisterEnum import GenericRegisterEnum

class Register(BaseModel):
    name: str
    as_4_bit: str
    as_1_bit: str

class x86_64_Registers:
    map: dict[GenericRegisterEnum, Register] = {
        GenericRegisterEnum.AX: Register(name="EAX", as_4_bit="%eax", as_1_bit="%al"),
        GenericRegisterEnum.DX: Register(name="EDX", as_4_bit="%edx", as_1_bit="%dl"),
        GenericRegisterEnum.R10: Register(name="R10", as_4_bit="%r10d", as_1_bit="%r10b"),
        GenericRegisterEnum.R11: Register(name="R11", as_4_bit="%r11d", as_1_bit="%r11b"),
    }
    def generic_register_to_x86_64(self, generic_reg: GenericRegisterEnum) -> Register:
        return self.map[generic_reg]