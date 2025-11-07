from modules.models.nodes.BaseNode import BaseNode

class ExpressionNode(BaseNode):
	value: str

class UnaryNode(BaseNode):
	operand: BaseNode