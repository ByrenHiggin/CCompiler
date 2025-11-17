#!/usr/bin/env python3
"""
Comprehensive test runner for CCompiler visitor classes.
Runs tests for ASTLegalizerVisitor, ASTLowererVisitor, and x86_64_AssemblyVisitor.
"""
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

def run_visitor_tests():
    """Run all visitor tests and return the results."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test modules
    try:
        # Import test modules
        from tests.parser.test_ASTLegalizerVisitor import TestASTLegalizer
        from tests.parser.test_ASTLowererVisitor import TestASTLowerer
        from tests.codeGenerator.test_x86_64_AssemblyVisitor import TestX86_64AssemblyVisitor
        
        # Add tests to suite
        suite.addTests(loader.loadTestsFromTestCase(TestASTLegalizer))
        suite.addTests(loader.loadTestsFromTestCase(TestASTLowerer))
        suite.addTests(loader.loadTestsFromTestCase(TestX86_64AssemblyVisitor))
        
        print("=== Running CCompiler Visitor Tests ===\n")
        
        # Run tests with detailed output
        runner = unittest.TextTestRunner(
            verbosity=2,
            stream=sys.stdout,
            descriptions=True,
            failfast=False
        )
        
        result = runner.run(suite)
        
        # Print summary
        print(f"\n=== Test Summary ===")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
        
        if result.failures:
            print(f"\n=== Failures ({len(result.failures)}) ===")
            for test, traceback in result.failures:
                print(f"FAIL: {test}")
                print(f"Traceback:\n{traceback}\n")
        
        if result.errors:
            print(f"\n=== Errors ({len(result.errors)}) ===")
            for test, traceback in result.errors:
                print(f"ERROR: {test}")
                print(f"Traceback:\n{traceback}\n")
        
        return result.wasSuccessful()
        
    except ImportError as e:
        print(f"Error importing test modules: {e}")
        print("Make sure all dependencies are available and paths are correct.")
        return False
    except Exception as e:
        print(f"Unexpected error running tests: {e}")
        return False

if __name__ == '__main__':
    success = run_visitor_tests()
    sys.exit(0 if success else 1)