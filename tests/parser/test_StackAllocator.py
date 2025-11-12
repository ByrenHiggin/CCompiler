# type: ignore
import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from modules.parser.visitors.StackAllocator import StackAllocator
from modules.models.nodes.IR.Operands.Pseudo import Pseudo
from modules.models.nodes.IR.Operands.Stack import Stack


class TestStackAllocator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.allocator = StackAllocator()

    def test_init(self):
        """Test that StackAllocator initializes correctly."""
        self.assertEqual(self.allocator.temp_counter, 0)
        self.assertEqual(self.allocator.stack_offset, 0)
        self.assertEqual(self.allocator.register_map, {})

    def test_allocate_pseudo_basic(self):
        """Test basic pseudo allocation."""
        pseudo = self.allocator.allocate_pseudo("tmp.0")
        
        self.assertIsInstance(pseudo, Pseudo)
        self.assertEqual(pseudo.value, "tmp.0")
        self.assertEqual(self.allocator.stack_offset, -4)  # Default size is 4
        self.assertIn("tmp.0", self.allocator.register_map)
        self.assertEqual(self.allocator.register_map["tmp.0"], -4)

    def test_allocate_pseudo_custom_size(self):
        """Test pseudo allocation with custom size."""
        pseudo = self.allocator.allocate_pseudo("tmp.0", size=8)
        
        self.assertEqual(self.allocator.stack_offset, -8)
        self.assertEqual(self.allocator.register_map["tmp.0"], -8)

    def test_allocate_multiple_pseudos(self):
        """Test allocating multiple pseudos."""
        pseudo1 = self.allocator.allocate_pseudo("tmp.0")
        pseudo2 = self.allocator.allocate_pseudo("tmp.1")
        pseudo3 = self.allocator.allocate_pseudo("tmp.2", size=8)
        
        # Stack should grow downward
        self.assertEqual(self.allocator.stack_offset, -16)  # 4 + 4 + 8
        
        # Check individual offsets
        self.assertEqual(self.allocator.register_map["tmp.0"], -4)
        self.assertEqual(self.allocator.register_map["tmp.1"], -8)
        self.assertEqual(self.allocator.register_map["tmp.2"], -16)

    def test_resolve_pseudo_success(self):
        """Test successful pseudo resolution."""
        # Allocate a pseudo first
        pseudo = self.allocator.allocate_pseudo("test_var")
        
        # Resolve it back to stack
        stack = self.allocator.resolve_pseudo(pseudo)
        
        self.assertIsInstance(stack, Stack)
        self.assertEqual(stack.offset, -4)

    def test_resolve_pseudo_not_found(self):
        """Test pseudo resolution for unregistered pseudo."""
        # Create a pseudo without allocating it
        unregistered_pseudo = Pseudo(value="unregistered")
        
        with self.assertRaises(KeyError) as context:
            self.allocator.resolve_pseudo(unregistered_pseudo)
        
        self.assertIn("Pseudo not registered to stack", str(context.exception))

    def test_resolve_pseudo_multiple(self):
        """Test resolving multiple pseudos."""
        # Allocate several pseudos
        pseudo1 = self.allocator.allocate_pseudo("var1")
        pseudo2 = self.allocator.allocate_pseudo("var2")
        pseudo3 = self.allocator.allocate_pseudo("var3", size=8)
        
        # Resolve them
        stack1 = self.allocator.resolve_pseudo(pseudo1)
        stack2 = self.allocator.resolve_pseudo(pseudo2)
        stack3 = self.allocator.resolve_pseudo(pseudo3)
        
        self.assertEqual(stack1.offset, -4)
        self.assertEqual(stack2.offset, -8)
        self.assertEqual(stack3.offset, -16)

    def test_stack_allocation_pattern(self):
        """Test that stack allocation follows expected pattern."""
        initial_offset = self.allocator.stack_offset
        
        # Allocate in different sizes
        sizes = [4, 8, 4, 16, 4]
        expected_offsets = []
        current_offset = initial_offset
        
        for size in sizes:
            current_offset -= size
            expected_offsets.append(current_offset)
        
        # Actually allocate
        actual_offsets = []
        for i, size in enumerate(sizes):
            pseudo = self.allocator.allocate_pseudo(f"var_{i}", size=size)
            actual_offsets.append(self.allocator.register_map[pseudo.value])
        
        self.assertEqual(actual_offsets, expected_offsets)
        self.assertEqual(self.allocator.stack_offset, sum(sizes) * -1)

    def test_name_collision_handling(self):
        """Test behavior with duplicate pseudo names."""
        # Allocate first pseudo
        pseudo1 = self.allocator.allocate_pseudo("duplicate_name")
        
        # Allocate second pseudo with same name (should overwrite)
        pseudo2 = self.allocator.allocate_pseudo("duplicate_name")
        
        # The second allocation should have updated the mapping
        self.assertEqual(self.allocator.register_map["duplicate_name"], -8)
        self.assertEqual(self.allocator.stack_offset, -8)
        
        # Resolving should return the latest allocation
        resolved = self.allocator.resolve_pseudo(pseudo2)
        self.assertEqual(resolved.offset, -8)


if __name__ == '__main__':
    unittest.main()