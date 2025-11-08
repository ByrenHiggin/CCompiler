# type: ignore
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.parser.ASTLegalizerVisitor import ASTLegalizer
from modules.parser.StackAllocator import StackAllocator
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate


class TestASTLegalizerSimple(unittest.TestCase):
    """Simplified tests for ASTLegalizer that focus on core functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.allocator = StackAllocator()
        self.legalizer = ASTLegalizer(self.allocator)

    def test_legalizer_initializes_correctly(self):
        """Test that ASTLegalizer initializes with the correct allocator."""
        self.assertEqual(self.legalizer.allocator, self.allocator)

    def test_legal_register_to_register_move(self):
        """Test that legal register-to-register moves pass through unchanged."""
        instructions = []
        src = Register(value=RegisterEnum.EAX)
        dest = Register(value=RegisterEnum.R10)
        move = IRMoveValue(src=src, dest=dest)
        
        self.legalizer.visit_ir_move_value(move, instructions)
        
        # Should have exactly one instruction (the original move)
        self.assertEqual(len(instructions), 1)
        self.assertIsInstance(instructions[0], IRMoveValue)

    def test_legal_immediate_to_register_move(self):
        """Test that immediate-to-register moves are legal."""
        instructions = []
        src = Immediate(value="42")
        dest = Register(value=RegisterEnum.EAX)
        move = IRMoveValue(src=src, dest=dest)
        
        self.legalizer.visit_ir_move_value(move, instructions)
        
        # Should pass through as single instruction
        self.assertEqual(len(instructions), 1)

    def test_illegal_stack_to_stack_move_is_split(self):
        """Test that illegal stack-to-stack moves are split into two legal moves."""
        instructions = []
        src = Stack(offset=-4)
        dest = Stack(offset=-8)
        move = IRMoveValue(src=src, dest=dest)
        
        self.legalizer.visit_ir_move_value(move, instructions)
        
        # Should be split into two instructions
        self.assertEqual(len(instructions), 2)
        
        # First instruction: stack to R10
        self.assertIsInstance(instructions[0], IRMoveValue)
        self.assertEqual(instructions[0].src, src)
        self.assertIsInstance(instructions[0].dest, Register)
        self.assertEqual(instructions[0].dest.value, RegisterEnum.R10)
        
        # Second instruction: R10 to destination stack
        self.assertIsInstance(instructions[1], IRMoveValue)
        self.assertIsInstance(instructions[1].src, Register)
        self.assertEqual(instructions[1].src.value, RegisterEnum.R10)
        self.assertEqual(instructions[1].dest, dest)

    def test_pseudo_resolution_in_moves(self):
        """Test that pseudos are properly resolved to stack locations."""
        instructions = []
        
        # Create and allocate pseudos
        pseudo1 = self.allocator.allocate_pseudo("tmp.1")
        pseudo2 = self.allocator.allocate_pseudo("tmp.2")
        
        move = IRMoveValue(src=pseudo1, dest=pseudo2)
        
        self.legalizer.visit_ir_move_value(move, instructions)
        
        # Should be split because both resolve to stack locations
        self.assertEqual(len(instructions), 2)
        
        # Both instructions should use resolved stack addresses
        self.assertIsInstance(instructions[0].src, Stack)
        self.assertIsInstance(instructions[0].dest, Register)
        self.assertIsInstance(instructions[1].src, Register)
        self.assertIsInstance(instructions[1].dest, Stack)

    def test_mixed_pseudo_and_register(self):
        """Test moves between pseudos and registers."""
        instructions = []
        
        # Pseudo to register (should be legal after resolution)
        pseudo = self.allocator.allocate_pseudo("tmp.1")
        reg = Register(value=RegisterEnum.EAX)
        move = IRMoveValue(src=pseudo, dest=reg)
        
        self.legalizer.visit_ir_move_value(move, instructions)
        
        # Should be one instruction (stack to register is legal)
        self.assertEqual(len(instructions), 1)
        self.assertIsInstance(instructions[0].src, Stack)
        self.assertEqual(instructions[0].dest, reg)


if __name__ == '__main__':
    unittest.main()