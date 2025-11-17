from modules.codeGenerator.Visitors.x86_64_AssemblyVisitor import x86_64_AssemblyVisitor
from modules.models.nodes.IR.IRProgramNode import IRProgramNode
from modules.utils.logger import get_logger



class AssemblyGenerator:
    visitor: x86_64_AssemblyVisitor
    lines: list[str]
    def __init__(self) -> None:
        self.visitor = x86_64_AssemblyVisitor()
        self.lines: list[str] = []

    def generate(self, node: IRProgramNode, instructions: list[str]):
        logger = get_logger()
        
        for func in node.functions:
            func.accept(self.visitor, instructions)