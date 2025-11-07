import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.parser.ASTLowererVisitor import ASTLowerer
from modules.parser.StackAllocator import StackAllocator
from modules.models.nodes.AST.Operands.UnaryOperators import BitwiseNot, Negate
from modules.models.nodes.AST.Functions.FunctionDefinition import FunctionDefinitionNode
from modules.models.nodes.BaseNode import BaseNode
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Operands.Pseudo import Pseudo
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn


class TestASTLowerer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.allocator = StackAllocator()
        self.lowerer = ASTLowerer(self.allocator)
        self.instructions = []

    def test_init(self):
        """Test that ASTLowerer initializes correctly."""
        self.assertEqual(self.lowerer.allocator, self.allocator)

    def test_visit_constant_integer(self):
        """Test visiting a constant integer node."""
        # Mock constant integer node
        const_node = Mock()
        const_node.value = "42"
        
        result = self.lowerer.visit_constant_integer(const_node, self.instructions)
        
        self.assertIsInstance(result, Immediate)
        self.assertEqual(result.value, "42")
        # Should not add any instructions
        self.assertEqual(len(self.instructions), 0)

    def test_visit_negate_with_constant(self):
        """Test negating a constant operand."""
        # Create a real constant integer node instead of mock
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        const_operand = ConstantInteger(value="5")
        
        # Create negate node
        negate_node = Negate(operand=const_operand)
        
        result = self.lowerer.visit_negate(negate_node, self.instructions)
        
        # Should return a pseudo
        self.assertIsInstance(result, Pseudo)
        self.assertEqual(result.value, "tmp.0")
        
        # Should generate two instructions: move and negate
        self.assertEqual(len(self.instructions), 2)
        
        # First instruction: move immediate to pseudo
        self.assertIsInstance(self.instructions[0], IRMoveValue)
        self.assertIsInstance(self.instructions[0].src, Immediate)
        self.assertEqual(self.instructions[0].src.value, "5")
        self.assertIsInstance(self.instructions[0].dest, Pseudo)
        
        # Second instruction: negate the pseudo
        self.assertIsInstance(self.instructions[1], UnaryInstruction)
        self.assertEqual(self.instructions[1].operator, UnaryOperationEnum.NEG)
        self.assertIsInstance(self.instructions[1].operand, Pseudo)
        
        # Verify temp counter was incremented
        self.assertEqual(self.allocator.temp_counter, 1)

    def test_visit_bitwise_not_with_constant(self):
        """Test bitwise NOT operation on a constant."""
        # Create a real constant integer node instead of mock
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        const_operand = ConstantInteger(value="7")
        
        # Create bitwise NOT node
        not_node = BitwiseNot(operand=const_operand)
        
        result = self.lowerer.visit_bitwise_not(not_node, self.instructions)
        
        # Should return a pseudo
        self.assertIsInstance(result, Pseudo)
        self.assertEqual(result.value, "tmp.0")
        
        # Should generate two instructions: move and bitwise not
        self.assertEqual(len(self.instructions), 2)
        
        # First instruction: move immediate to pseudo
        self.assertIsInstance(self.instructions[0], IRMoveValue)
        self.assertIsInstance(self.instructions[0].src, Immediate)
        self.assertEqual(self.instructions[0].src.value, "7")
        self.assertIsInstance(self.instructions[0].dest, Pseudo)
        
        # Second instruction: bitwise not the pseudo
        self.assertIsInstance(self.instructions[1], UnaryInstruction)
        self.assertEqual(self.instructions[1].operator, UnaryOperationEnum.NOT)
        self.assertIsInstance(self.instructions[1].operand, Pseudo)

    def test_visit_negate_nested_operations(self):
        """Test negating a result of another operation."""
        # Setup: Create nested operations (bitwise not then negate)
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        inner_operand = ConstantInteger(value="10")
        
        # First operation: bitwise not
        not_node = BitwiseNot(operand=inner_operand)
        not_result = self.lowerer.visit_bitwise_not(not_node, self.instructions)
        
        # Reset instructions for the negate test
        self.instructions.clear()
        
        # Second operation: negate the result of bitwise not
        # Create another constant node for chaining
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        another_const = ConstantInteger(value="10")
        negate_node = Negate(operand=another_const)
        
        final_result = self.lowerer.visit_negate(negate_node, self.instructions)
        
        # Should return a new pseudo
        self.assertIsInstance(final_result, Pseudo)
        self.assertEqual(final_result.value, "tmp.1")  # Should be second temp
        
        # Should have generated move and negate instructions
        self.assertEqual(len(self.instructions), 2)
        self.assertEqual(self.allocator.temp_counter, 2)

    def test_visit_return_statement(self):
        """Test visiting a return statement."""
        # Mock return value
        return_value_node = Mock()
        return_value_node.accept.return_value = Immediate(value="42")
        
        # Mock return statement node
        return_node = Mock()
        return_node.returnValue = return_value_node
        
        result = self.lowerer.visit_return_statement(return_node, self.instructions)
        
        # Should return the return value
        self.assertIsInstance(result, Immediate)
        self.assertEqual(result.value, "42")
        
        # Should generate two instructions: move to EAX and return
        self.assertEqual(len(self.instructions), 2)
        
        # First instruction: move return value to EAX
        self.assertIsInstance(self.instructions[0], IRMoveValue)
        self.assertIsInstance(self.instructions[0].src, Immediate)
        self.assertEqual(self.instructions[0].src.value, "42")
        self.assertIsInstance(self.instructions[0].dest, Register)
        self.assertEqual(self.instructions[0].dest.value, RegisterEnum.EAX)
        
        # Second instruction: return
        self.assertIsInstance(self.instructions[1], IRreturn)
        self.assertIsInstance(self.instructions[1].value, Register)
        self.assertEqual(self.instructions[1].value.value, RegisterEnum.EAX)

    def test_visit_function_definition(self):
        """Test visiting a function definition."""
        # Mock function body
        function_body = Mock()
        expected_result = Mock()
        function_body.accept.return_value = expected_result
        
        # Mock function definition node
        func_node = Mock(spec=FunctionDefinitionNode)
        func_node.body = function_body
        
        result = self.lowerer.visit_function_definition(func_node, self.instructions)
        
        # Should return the result of processing the function body
        self.assertEqual(result, expected_result)
        
        # Verify that the function body was processed
        function_body.accept.assert_called_once_with(self.lowerer, self.instructions)

    def test_visit_ir_return(self):
        """Test visiting an IR return node."""
        # Create IR return node
        return_value = Register(value=RegisterEnum.EAX)
        ir_return_node = IRreturn(value=return_value)
        
        result = self.lowerer.visit_ir_return(ir_return_node, self.instructions)
        
        # Should return the node itself
        self.assertEqual(result, ir_return_node)
        
        # Should add the node to instructions
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], ir_return_node)

    def test_temp_counter_increments(self):
        """Test that temp counter increments properly across operations."""
        # Create multiple operations to verify counter increments
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        operations = []
        
        for i in range(3):
            const_operand = ConstantInteger(value=str(i))
            negate_node = Negate(operand=const_operand)
            operations.append(negate_node)
        
        results = []
        for op in operations:
            result = self.lowerer.visit_negate(op, self.instructions)
            results.append(result)
        
        # Verify temp names are unique and incremental
        expected_names = ["tmp.0", "tmp.1", "tmp.2"]
        actual_names = [r.value for r in results]
        self.assertEqual(actual_names, expected_names)
        
        # Verify final counter value
        self.assertEqual(self.allocator.temp_counter, 3)

    def test_stack_allocation_per_operation(self):
        """Test that each operation allocates stack space."""
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        initial_offset = self.allocator.stack_offset
        
        # Perform a negate operation
        const_operand = ConstantInteger(value="5")
        negate_node = Negate(operand=const_operand)
        
        result = self.lowerer.visit_negate(negate_node, self.instructions)
        
        # Stack offset should have decreased (allocated space)
        self.assertLess(self.allocator.stack_offset, initial_offset)
        
        # The pseudo should be registered in the allocator
        self.assertIn(result.value, self.allocator.register_map)

    def test_complex_expression_lowering(self):
        """Test lowering a complex expression: -(~42)."""
        # Create inner constant
        from modules.models.nodes.AST.Operands.ConstantInteger import ConstantInteger
        const_node = ConstantInteger(value="42")
        
        # Create bitwise not
        not_node = BitwiseNot(operand=const_node)
        self.lowerer.visit_bitwise_not(not_node, self.instructions)
        
        # Create negate of another constant to test separate operations
        negate_const = ConstantInteger(value="42")
        negate_node = Negate(operand=negate_const)
        
        final_result = self.lowerer.visit_negate(negate_node, self.instructions)
        
        # Should have 4 instructions total:
        # 1. Move 42 to tmp.0
        # 2. NOT tmp.0
        # 3. Move tmp.0 to tmp.1
        # 4. NEG tmp.1
        self.assertEqual(len(self.instructions), 4)
        
        # Verify instruction sequence
        self.assertIsInstance(self.instructions[0], IRMoveValue)  # Move 42
        self.assertIsInstance(self.instructions[1], UnaryInstruction)  # NOT
        self.assertEqual(self.instructions[1].operator, UnaryOperationEnum.NOT)
        self.assertIsInstance(self.instructions[2], IRMoveValue)  # Move result
        self.assertIsInstance(self.instructions[3], UnaryInstruction)  # NEG
        self.assertEqual(self.instructions[3].operator, UnaryOperationEnum.NEG)
        
        # Final result should be tmp.1
        self.assertEqual(final_result.value, "tmp.1")


if __name__ == '__main__':
    unittest.main()