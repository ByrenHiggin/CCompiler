"""
Integration test for the complete visitor pipeline.
This tests the interaction between ASTLowerer -> ASTLegalizer -> AssemblyVisitor
"""
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.IntermediateGenerator.IRGenerator import TackyGenerator
from modules.models.nodes.AST.ProgramNode import ProgramNode


class TestVisitorIntegration(unittest.TestCase):
    """Integration tests for the complete visitor pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.tacky_generator = TackyGenerator()

    def test_tacky_generator_initializes(self):
        """Test that TackyGenerator initializes correctly."""
        self.assertEqual(len(self.tacky_generator.first_pass_instructions), 0)
        self.assertEqual(len(self.tacky_generator.second_pass_instructions), 0)
        self.assertEqual(len(self.tacky_generator.third_pass_instructions), 0)

    def test_empty_program_processing(self):
        """Test processing an empty program."""
        # Create a mock empty program
        empty_program = ProgramNode(functions=[])
        
        result = self.tacky_generator.parse_ast(empty_program)
        
        # Should return an IR program with no functions
        self.assertEqual(len(result.functions), 0)

    def test_visitor_components_exist(self):
        """Test that all required visitor components can be imported."""
        try:
            from modules.parser.ASTLegalizerVisitor import ASTLegalizer
            from modules.parser.ASTLowererVisitor import ASTLowerer
            from modules.parser.visitors.StackAllocator import StackAllocator
            from modules.codeGenerator.Visitors.x86_64_AssemblyVisitor import x86_64_AssemblyVisitor
            
            # Try to instantiate each component
            allocator = StackAllocator()
            legalizer = ASTLegalizer(allocator)
            lowerer = ASTLowerer(allocator)
            assembly_visitor = x86_64_AssemblyVisitor()
            
            # Basic verification
            self.assertIsNotNone(allocator)
            self.assertIsNotNone(legalizer)
            self.assertIsNotNone(lowerer)
            self.assertIsNotNone(assembly_visitor)
            
        except ImportError as e:
            self.fail(f"Failed to import visitor components: {e}")

    def test_stack_allocator_integration(self):
        """Test that StackAllocator integrates properly with visitors."""
        from modules.parser.visitors.StackAllocator import StackAllocator
        from modules.parser.ASTLegalizerVisitor import ASTLegalizer
        from modules.parser.ASTLowererVisitor import ASTLowerer
        
        allocator = StackAllocator()
        legalizer = ASTLegalizer(allocator)
        lowerer = ASTLowerer(allocator)
        
        # Both visitors should reference the same allocator
        self.assertIs(legalizer.allocator, allocator)
        self.assertIs(lowerer.allocator, allocator)

    def test_visitor_method_signatures(self):
        """Test that visitor methods have expected signatures."""
        from modules.parser.ASTLegalizerVisitor import ASTLegalizer
        from modules.parser.ASTLowererVisitor import ASTLowerer
        from modules.codeGenerator.Visitors.x86_64_AssemblyVisitor import x86_64_AssemblyVisitor
        from modules.parser.visitors.StackAllocator import StackAllocator
        
        allocator = StackAllocator()
        legalizer = ASTLegalizer(allocator)
        lowerer = ASTLowerer(allocator)
        assembly_visitor = x86_64_AssemblyVisitor()
        
        # Check that expected methods exist
        self.assertTrue(hasattr(legalizer, 'visit_ir_copy'))
        self.assertTrue(hasattr(legalizer, 'visit_unary_instruction'))
        self.assertTrue(hasattr(legalizer, 'visit_ir_return'))
        
        self.assertTrue(hasattr(lowerer, 'visit_negate'))
        self.assertTrue(hasattr(lowerer, 'visit_bitwise_not'))
        self.assertTrue(hasattr(lowerer, 'visit_constant_integer'))
        self.assertTrue(hasattr(lowerer, 'visit_return_statement'))
        
        self.assertTrue(hasattr(assembly_visitor, 'visit_ir_copy'))
        self.assertTrue(hasattr(assembly_visitor, 'visit_unary_instruction'))
        self.assertTrue(hasattr(assembly_visitor, 'visit_ir_return'))
        self.assertTrue(hasattr(assembly_visitor, '_operand_to_asm'))

    def test_visitor_error_handling(self):
        """Test that visitors handle errors gracefully."""
        from modules.parser.visitors.StackAllocator import StackAllocator
        from modules.models.nodes.IR.Operands.Pseudo import Pseudo
        
        allocator = StackAllocator()
        
        # Test resolving unregistered pseudo
        unregistered_pseudo = Pseudo(value="unregistered")
        
        with self.assertRaises(KeyError):
            allocator.resolve_pseudo(unregistered_pseudo)

    def test_instruction_list_management(self):
        """Test that instruction lists are managed correctly."""
        # Verify that the TackyGenerator manages instruction lists properly
        self.assertIsInstance(self.tacky_generator.first_pass_instructions, list)
        self.assertIsInstance(self.tacky_generator.second_pass_instructions, list)
        self.assertIsInstance(self.tacky_generator.third_pass_instructions, list)
        
        # Lists should be independent
        self.assertIsNot(
            self.tacky_generator.first_pass_instructions,
            self.tacky_generator.second_pass_instructions
        )


if __name__ == '__main__':
    unittest.main()