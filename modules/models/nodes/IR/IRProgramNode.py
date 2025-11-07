from modules.models.AstNodes.BaseNode import IRNode 
from modules.models.AstNodes.IR.Functions.IRFunctionDefinition import IRFunctionDefinition
 
class IRProgramNode(IRNode):
    functions: list[IRFunctionDefinition]
    def accept(self, visitor, instructions):
        return visitor.visit_ir_program_node(self, instructions)



    
