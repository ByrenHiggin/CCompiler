from typing import List
from modules.models.nodes.BaseNode import BaseNode, IRNode 
from modules.models.nodes.AST.ProgramNode import ProgramNode
from modules.IntermediateGenerator.visitors.ASTLegalizerVisitor import ASTLegalizer
from modules.IntermediateGenerator.visitors.ASTLowererVisitor import ASTLowerer
from modules.models.nodes.IR.IRProgramNode import IRFunctionDefinition, IRProgramNode
from modules.IntermediateGenerator.visitors.StackAllocator import StackAllocator
from modules.utils.logger import get_logger

class IRGenerator:
    def __init__(self):
        self.logger = get_logger()
        self.first_pass_instructions: list[BaseNode] = []
        self.second_pass_instructions: list[BaseNode] = []
        self.third_pass_instructions: list[BaseNode] = []
    
    def parse_ast(self, node: ProgramNode) -> IRProgramNode:
        functions: list[IRFunctionDefinition] = []
        for func in node.functions:
            allocator = StackAllocator()
            lowerer = ASTLowerer(allocator=allocator)
            legalizer = ASTLegalizer(allocator=allocator)
            self.logger.debug(f"Processing function: {func.name}")
            #phase 1 - lowerer
            lowered_instructions: List[BaseNode] = []
            func.accept(lowerer, lowered_instructions)
            self.logger.debug(f"Lowered instructions for function: {func.name}")
            #phase 2 - legalizer
            legalized_instructions: List[IRNode] = []
            for instr in lowered_instructions:
                instr.accept(legalizer, legalized_instructions)
            self.logger.debug(f"Legalized instructions for function: {func.name}")
            functions.append(
                IRFunctionDefinition(
                    name=func.name,
                    offset=abs(allocator.stack_offset),
                    instructions=legalized_instructions
                )
            )
        return IRProgramNode(functions=functions)