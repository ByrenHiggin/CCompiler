# type: ignore
from typing import List
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.models.nodes.BaseNode import IRNode
from modules.parser.ASTLegalizerVisitor import ASTLegalizer
from modules.parser.visitors.StackAllocator import StackAllocator
from modules.models.nodes.IR.Statements.IRCopy import IRCopy
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn


class TestASTLegalizer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.allocator = StackAllocator()
        self.legalizer = ASTLegalizer(self.allocator)
        self.instructions: List[IRNode] = []

    def test_init(self):
        """Test that ASTLegalizer initializes correctly."""
        self.assertEqual(self.legalizer.allocator, self.allocator)

    def test_visit_ir_copy_register_to_register(self):
        """Test move between two registers (legal operation)."""
        src_reg = Register(value=RegisterEnum.EAX)
        dest_reg = Register(value=RegisterEnum.R10)
        move_node = IRCopy(src=src_reg, dest=dest_reg)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertIsInstance(self.instructions[0], IRCopy)
        self.assertEqual(self.instructions[0].src, src_reg)
        self.assertEqual(self.instructions[0].dest, dest_reg)

    def test_visit_ir_copy_immediate_to_register(self):
        """Test move from immediate to register (legal operation)."""
        src_imm = Immediate(value="42")
        dest_reg = Register(value=RegisterEnum.EAX)
        move_node = IRCopy(src=src_imm, dest=dest_reg)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertIsInstance(self.instructions[0], IRCopy)
        self.assertEqual(self.instructions[0].src, src_imm)
        self.assertEqual(self.instructions[0].dest, dest_reg)

    def test_visit_ir_copy_register_to_stack(self):
        """Test move from register to stack (legal operation)."""
        src_reg = Register(value=RegisterEnum.EAX)
        dest_stack = Stack(offset=-4)
        move_node = IRCopy(src=src_reg, dest=dest_stack)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertIsInstance(self.instructions[0], IRCopy)
        self.assertEqual(self.instructions[0].src, src_reg)
        self.assertEqual(self.instructions[0].dest, dest_stack)

    def test_visit_ir_copy_stack_to_register(self):
        """Test move from stack to register (legal operation)."""
        src_stack = Stack(offset=-8)
        dest_reg = Register(value=RegisterEnum.R10)
        move_node = IRCopy(src=src_stack, dest=dest_reg)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertIsInstance(self.instructions[0], IRCopy)
        self.assertEqual(self.instructions[0].src, src_stack)
        self.assertEqual(self.instructions[0].dest, dest_reg)

    def test_visit_ir_copy_stack_to_stack_illegal(self):
        """Test move from stack to stack (illegal - should be split into two moves)."""
        src_stack = Stack(offset=-4)
        dest_stack = Stack(offset=-8)
        move_node = IRCopy(src=src_stack, dest=dest_stack)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        # Should generate two instructions: stack->R10, R10->stack
        self.assertEqual(len(self.instructions), 2)
        
        # First instruction: stack to R10
        self.assertIsInstance(self.instructions[0], IRCopy)
        self.assertEqual(self.instructions[0].src, src_stack)
        self.assertIsInstance(self.instructions[0].dest, Register)
        self.assertEqual(self.instructions[0].dest.value, RegisterEnum.R10)
        
        # Second instruction: R10 to destination stack
        self.assertIsInstance(self.instructions[1], IRCopy)
        self.assertIsInstance(self.instructions[1].src, Register)
        self.assertEqual(self.instructions[1].src.value, RegisterEnum.R10)
        self.assertEqual(self.instructions[1].dest, dest_stack)

    def test_visit_ir_copy_pseudo_to_pseudo(self):
        """Test move between two pseudos (should resolve and handle appropriately)."""
        # Set up pseudos in allocator
        pseudo1 = self.allocator.allocate_pseudo("tmp.1")
        pseudo2 = self.allocator.allocate_pseudo("tmp.2")
        
        move_node = IRCopy(src=pseudo1, dest=pseudo2)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        # Should generate two instructions since both pseudos resolve to stack slots
        self.assertEqual(len(self.instructions), 2)
        
        # Verify the instructions use R10 as intermediate
        self.assertIsInstance(self.instructions[0].dest, Register)
        self.assertEqual(self.instructions[0].dest.value, RegisterEnum.R10)
        self.assertIsInstance(self.instructions[1].src, Register)
        self.assertEqual(self.instructions[1].src.value, RegisterEnum.R10)

    def test_visit_ir_copy_pseudo_to_register(self):
        """Test move from pseudo to register."""
        pseudo = self.allocator.allocate_pseudo("tmp.1")
        dest_reg = Register(value=RegisterEnum.EAX)
        move_node = IRCopy(src=pseudo, dest=dest_reg)
        
        self.legalizer.visit_ir_copy(move_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertIsInstance(self.instructions[0].src, Stack)
        self.assertEqual(self.instructions[0].dest, dest_reg)

    def test_visit_unary_instruction_with_register(self):
        """Test unary instruction with register operand."""
        reg = Register(value=RegisterEnum.EAX)
        unary_node = UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=reg)
        
        self.legalizer.visit_unary_instruction(unary_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], unary_node)
        self.assertEqual(self.instructions[0].operand, reg)

    def test_visit_unary_instruction_with_pseudo(self):
        """Test unary instruction with pseudo operand (should resolve to stack)."""
        pseudo = self.allocator.allocate_pseudo("tmp.1")
        unary_node = UnaryInstruction(operator=UnaryOperationEnum.NOT, operand=pseudo)
        
        self.legalizer.visit_unary_instruction(unary_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], unary_node)
        # Operand should be resolved to Stack
        self.assertIsInstance(self.instructions[0].operand, Stack)

    def test_visit_unary_instruction_with_stack(self):
        """Test unary instruction with stack operand."""
        stack = Stack(offset=-4)
        unary_node = UnaryInstruction(operator=UnaryOperationEnum.NEG, operand=stack)
        
        self.legalizer.visit_unary_instruction(unary_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], unary_node)
        self.assertEqual(self.instructions[0].operand, stack)

    def test_visit_ir_return(self):
        """Test IR return statement processing."""
        return_reg = Register(value=RegisterEnum.EAX)
        return_node = IRreturn(value=return_reg)
        
        result = self.legalizer.visit_ir_return(return_node, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], return_node)
        self.assertEqual(result, return_node)

    def test_multiple_stack_to_stack_moves(self):
        """Test multiple stack-to-stack moves use the same intermediate register."""
        stack1 = Stack(offset=-4)
        stack2 = Stack(offset=-8)
        stack3 = Stack(offset=-12)
        
        move1 = IRCopy(src=stack1, dest=stack2)
        move2 = IRCopy(src=stack2, dest=stack3)
        
        self.legalizer.visit_ir_copy(move1, self.instructions)
        self.legalizer.visit_ir_copy(move2, self.instructions)
        
        # Should have 4 instructions total (2 moves split into 2 each)
        self.assertEqual(len(self.instructions), 4)
        
        # All intermediate moves should use R10
        for i in [0, 2]:  # First instruction of each pair
            self.assertEqual(self.instructions[i].dest.value, RegisterEnum.R10)
        for i in [1, 3]:  # Second instruction of each pair
            self.assertEqual(self.instructions[i].src.value, RegisterEnum.R10)


if __name__ == '__main__':
    unittest.main()