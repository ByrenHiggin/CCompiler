from typing import List
from modules.models.nodes.BaseNode import BaseNode, IRNode 
from modules.models.nodes.AST.ProgramNode import ProgramNode
from modules.parser.visitors.ASTLegalizerVisitor import ASTLegalizer
from modules.parser.visitors.ASTLowererVisitor import ASTLowerer
from modules.models.nodes.IR.IRProgramNode import IRFunctionDefinition, IRProgramNode
from modules.parser.visitors.StackAllocator import StackAllocator

class TackyGenerator:
    def __init__(self):
        self.first_pass_instructions: list[BaseNode] = []
        self.second_pass_instructions: list[BaseNode] = []
        self.third_pass_instructions: list[BaseNode] = []
    
    def parse_ast(self, node: ProgramNode) -> IRProgramNode:
        functions: list[IRFunctionDefinition] = []
        for func in node.functions:
            allocator = StackAllocator()
            lowerer = ASTLowerer(allocator=allocator)
            legalizer = ASTLegalizer(allocator=allocator)
            
            #phase 1 - lowerer
            lowered_instructions: List[BaseNode] = []
            func.accept(lowerer, lowered_instructions)
            
            #phase 2 - legalizer
            legalized_instructions: List[IRNode] = []
            for instr in lowered_instructions:
                instr.accept(legalizer, legalized_instructions)
            
            functions.append(
                IRFunctionDefinition(
                    name=func.name,
                    offset=abs(allocator.stack_offset),
                    instructions=legalized_instructions
                )
            )
        return IRProgramNode(functions=functions)