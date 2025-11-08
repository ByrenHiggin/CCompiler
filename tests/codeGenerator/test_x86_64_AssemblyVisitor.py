# type: ignore
from typing import List
import unittest
from unittest.mock import Mock, patch
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.codeGenerator.Visitors.x86_64_AssemblyVisitor import x86_64_AssemblyVisitor
from modules.models.nodes.IR.IRMoveValue import IRMoveValue
from modules.models.nodes.IR.IRProgramNode import IRFunctionDefinition
from modules.models.nodes.IR.Operands.Immediate import Immediate
from modules.models.nodes.IR.Operands.Register import Register, RegisterEnum
from modules.models.nodes.IR.Operands.Stack import Stack
from modules.models.nodes.IR.Operands.UnaryInstruction import UnaryInstruction, UnaryOperationEnum
from modules.models.nodes.IR.Statements.IRReturnValue import IRreturn


class TestX86_64AssemblyVisitor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.visitor = x86_64_AssemblyVisitor()
        self.instructions: List[str] = []

    def test_init(self):
        """Test that x86_64_AssemblyVisitor initializes correctly."""
        self.assertEqual(self.visitor.lines, [])

    def test_operand_to_asm_register_eax(self):
        """Test converting EAX register to assembly."""
        reg = Register(value=RegisterEnum.EAX)
        result = self.visitor._operand_to_asm(reg)
        self.assertEqual(result, "%eax")

    def test_operand_to_asm_register_r10(self):
        """Test converting R10 register to assembly."""
        reg = Register(value=RegisterEnum.R10)
        result = self.visitor._operand_to_asm(reg)
        self.assertEqual(result, "%r10d")

    def test_operand_to_asm_stack_negative_offset(self):
        """Test converting stack operand with negative offset."""
        stack = Stack(offset=-4)
        result = self.visitor._operand_to_asm(stack)
        self.assertEqual(result, "-4(%rbp)")

    def test_operand_to_asm_stack_positive_offset(self):
        """Test converting stack operand with positive offset."""
        stack = Stack(offset=8)
        result = self.visitor._operand_to_asm(stack)
        self.assertEqual(result, "8(%rbp)")

    def test_operand_to_asm_immediate(self):
        """Test converting immediate operand to assembly."""
        immediate = Immediate(value="42")
        result = self.visitor._operand_to_asm(immediate)
        self.assertEqual(result, "$42")

    def test_operand_to_asm_unknown_operand(self):
        """Test that unknown operand type raises ValueError."""
        unknown_operand = Mock()
        unknown_operand.__class__ = type('UnknownOperand', (), {})
        
        with self.assertRaises(ValueError) as context:
            self.visitor._operand_to_asm(unknown_operand)
        
        self.assertIn("Unknown operand type", str(context.exception))

    def test_visit_function_definition_basic(self):
        """Test visiting a basic function definition."""
        # Create mock IR instructions
        mock_instr1 = Mock()
        mock_instr2 = Mock()
        
        # Create function definition
        func_def = IRFunctionDefinition(
            name="test_func",
            offset=8,
            instructions=[mock_instr1, mock_instr2]
        )
        
        self.visitor.visit_function_definition(func_def, self.instructions)
        
        # Verify the function preamble is generated
        expected_preamble = [
            ".globl _test_func\n",
            "_test_func:\n",
            "\tpushq %rbp\n",
            "\tmovq %rsp, %rbp\n",
            "\tsubq $8, %rsp\n"
        ]
        
        self.assertEqual(self.instructions[:5], expected_preamble)
        
        # Verify that each instruction was processed
        mock_instr1.accept.assert_called_once_with(self.visitor, self.instructions)
        mock_instr2.accept.assert_called_once_with(self.visitor, self.instructions)

    def test_visit_function_definition_zero_offset(self):
        """Test function definition with zero stack offset."""
        func_def = IRFunctionDefinition(
            name="no_locals",
            offset=0,
            instructions=[]
        )
        
        self.visitor.visit_function_definition(func_def, self.instructions)
        
        # Should still include subq $0, %rsp
        self.assertIn("\tsubq $0, %rsp\n", self.instructions)

    def test_visit_unary_instruction_negate(self):
        """Test visiting a negate unary instruction."""
        stack_operand = Stack(offset=-4)
        unary_instr = UnaryInstruction(
            operator=UnaryOperationEnum.NEG,
            operand=stack_operand
        )
        
        self.visitor.visit_unary_instruction(unary_instr, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], "\tnegl -4(%rbp)\n")

    def test_visit_unary_instruction_bitwise_not(self):
        """Test visiting a bitwise NOT unary instruction."""
        reg_operand = Register(value=RegisterEnum.EAX)
        unary_instr = UnaryInstruction(
            operator=UnaryOperationEnum.NOT,
            operand=reg_operand
        )
        
        self.visitor.visit_unary_instruction(unary_instr, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], "\tnotl %eax\n")

    def test_visit_ir_move_value_register_to_register(self):
        """Test visiting a move instruction between registers."""
        src_reg = Register(value=RegisterEnum.EAX)
        dest_reg = Register(value=RegisterEnum.R10)
        move_instr = IRMoveValue(src=src_reg, dest=dest_reg)
        
        self.visitor.visit_ir_move_value(move_instr, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], "\tmovl %eax, %r10d\n")

    def test_visit_ir_move_value_immediate_to_stack(self):
        """Test visiting a move instruction from immediate to stack."""
        src_imm = Immediate(value="100")
        dest_stack = Stack(offset=-8)
        move_instr = IRMoveValue(src=src_imm, dest=dest_stack)
        
        self.visitor.visit_ir_move_value(move_instr, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], "\tmovl $100, -8(%rbp)\n")

    def test_visit_ir_move_value_stack_to_register(self):
        """Test visiting a move instruction from stack to register."""
        src_stack = Stack(offset=-4)
        dest_reg = Register(value=RegisterEnum.EAX)
        move_instr = IRMoveValue(src=src_stack, dest=dest_reg)
        
        self.visitor.visit_ir_move_value(move_instr, self.instructions)
        
        self.assertEqual(len(self.instructions), 1)
        self.assertEqual(self.instructions[0], "\tmovl -4(%rbp), %eax\n")

    def test_visit_ir_return(self):
        """Test visiting an IR return instruction."""
        return_val = Register(value=RegisterEnum.EAX)
        return_instr = IRreturn(value=return_val)
        
        self.visitor.visit_ir_return(return_instr, self.instructions)
        
        expected_return = [
            "\tmovq %rbp, %rsp\n",
            "\tpopq %rbp\n",
            "\tret\n"
        ]
        
        self.assertEqual(self.instructions, expected_return)

    def test_visit_stack_method(self):
        """Test the visit_stack method."""
        # Note: This method seems incomplete in the original code
        # It references self.offset which doesn't exist
        stack_node = Stack(offset=-12)
        
        # The current implementation has a bug - it uses self.offset instead of node.offset
        # We'll test what it currently does, but this should be fixed
        with self.assertRaises(AttributeError):
            self.visitor.visit_stack(stack_node, self.instructions)

    def test_visit_ir_program_node(self):
        """Test visiting an IR program node."""
        # The method is currently empty (pass statement)
        program_node = Mock()
        
        # Should not raise any exceptions
        self.visitor.visit_ir_program_node(program_node, self.instructions)
        
        # Should not modify instructions
        self.assertEqual(len(self.instructions), 0)

    def test_complete_function_with_instructions(self):
        """Test a complete function with various instructions."""
        # Create a realistic set of instructions
        instructions_list = [
            IRMoveValue(
                src=Immediate(value="42"),
                dest=Stack(offset=-4)
            ),
            UnaryInstruction(
                operator=UnaryOperationEnum.NEG,
                operand=Stack(offset=-4)
            ),
            IRMoveValue(
                src=Stack(offset=-4),
                dest=Register(value=RegisterEnum.EAX)
            ),
            IRreturn(value=Register(value=RegisterEnum.EAX))
        ]
        
        func_def = IRFunctionDefinition(
            name="main",
            offset=4,
            instructions=instructions_list
        )
        
        # Mock the accept method for each instruction
        for instr in instructions_list:
            instr.accept = Mock()
        
        self.visitor.visit_function_definition(func_def, self.instructions)
        
        # Verify function preamble
        expected_start = [
            ".globl _main\n",
            "_main:\n",
            "\tpushq %rbp\n",
            "\tmovq %rsp, %rbp\n",
            "\tsubq $4, %rsp\n"
        ]
        
        self.assertEqual(self.instructions[:5], expected_start)
        
        # Verify all instructions were processed
        for instr in instructions_list:
            instr.accept.assert_called_once_with(self.visitor, self.instructions)

    def test_multiple_functions(self):
        """Test processing multiple function definitions."""
        func1 = IRFunctionDefinition(name="func1", offset=4, instructions=[])
        func2 = IRFunctionDefinition(name="func2", offset=8, instructions=[])
        
        self.visitor.visit_function_definition(func1, self.instructions)
        self.visitor.visit_function_definition(func2, self.instructions)
        
        # Should have two function labels
        func_labels = [line for line in self.instructions if line.startswith(".globl")]
        self.assertEqual(len(func_labels), 2)
        self.assertIn(".globl _func1\n", func_labels)
        self.assertIn(".globl _func2\n", func_labels)

    def test_register_mapping_completeness(self):
        """Test that all expected registers are mapped correctly."""
        # Test EAX
        eax = Register(value=RegisterEnum.EAX)
        self.assertEqual(self.visitor._operand_to_asm(eax), "%eax")
        
        # Test R10
        r10 = Register(value=RegisterEnum.R10)
        self.assertEqual(self.visitor._operand_to_asm(r10), "%r10d")

    def test_instruction_formatting(self):
        """Test that instructions are properly formatted with tabs and newlines."""
        # Test move instruction formatting
        move_instr = IRMoveValue(
            src=Immediate(value="5"),
            dest=Stack(offset=-4)
        )
        
        self.visitor.visit_ir_move_value(move_instr, self.instructions)
        
        # Should start with tab and end with newline
        self.assertTrue(self.instructions[0].startswith("\t"))
        self.assertTrue(self.instructions[0].endswith("\n"))
        
        # Test unary instruction formatting
        self.instructions.clear()
        unary_instr = UnaryInstruction(
            operator=UnaryOperationEnum.NOT,
            operand=Register(value=RegisterEnum.EAX)
        )
        
        self.visitor.visit_unary_instruction(unary_instr, self.instructions)
        
        self.assertTrue(self.instructions[0].startswith("\t"))
        self.assertTrue(self.instructions[0].endswith("\n"))


if __name__ == '__main__':
    unittest.main()