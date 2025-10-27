from modules.models.AstNodes.BaseNode import IRNode, Operand

class stack_allocation(IRNode):
    size: int
    dest: Operand

    def toAsm(self) -> str:
        return f"subq ${self.size}({self.dest})"

class IRMoveValue(IRNode):
    src: Operand
    dest: Operand

    def accept(self, visitor, instructions):
        return visitor.visit_ir_move_value(self, instructions)

    def toAsm(self) -> str:
        return f"movl {self.src.toAsm()}, {self.dest.toAsm()}"
    
class IRreturn(IRNode):
    value: Operand

    def accept(self, visitor, instructions):
        return visitor.visit_ir_return(self, instructions)

    def toAsm(self) -> str:
        lines: list[str] = []
        lines.append("")
        lines.append(f"movq %rbp, %rsp")
        lines.append(f"popq %rbp")
        lines.append("ret")
        return "\n".join(lines)
    
class IRFunctionDefinition(IRNode):
    name: str
    instructions: list[IRNode]
    offset: int = 0
    def accept(self, visitor, instructions):
        return visitor.visit_function_definition(self, instructions)
    def toAsm(self) -> str:
        lines: list[str] = []
        lines.append(f".globl _{self.name}")
        lines.append(f"_{self.name}:")
        lines.append("\tpushq %rbp")
        lines.append("\tmovq %rsp, %rbp")
        lines.append(f"\tsubq ${self.offset}, %rsp")
        for instr in self.instructions:
            asm_line = instr.toAsm()
            for line in asm_line.splitlines():
                lines.append(f"\t{line}")
        return "\n".join(lines)

class IRProgramNode(IRNode):
    functions: list[IRFunctionDefinition]
    def toAsm(self) -> str:
        asm: list[str] = []
        for func in self.functions:
            asm.append(func.toAsm())
        return "\n".join(asm)
    def accept(self, visitor, instructions):
        return visitor.visit_ir_program_node(self, instructions)

class InstructionBuilder:
    def toAsm(self, programNode: IRProgramNode) -> str:
        asm: list[str] = []
        for func in programNode.functions:
            asm.append(func.toAsm())
        return "\n".join(asm)


    
