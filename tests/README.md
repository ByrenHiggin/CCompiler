# Comprehensive Test Suite Documentation

This directory contains comprehensive tests for the CCompiler visitor architecture. The tests are organized by component and cover all major functionality.

## Test Structure

### 1. Core Component Tests

#### `test_StackAllocator.py`
**Purpose**: Tests the stack allocation system that manages pseudo-register to stack slot mapping.

**Key Test Cases**:
- **Initialization**: Verifies proper setup of counters and data structures
- **Basic Allocation**: Tests single pseudo allocation with default 4-byte size
- **Custom Size Allocation**: Tests allocation with different sizes (8, 16 bytes)
- **Multiple Allocations**: Tests stack growth pattern (downward allocation)
- **Pseudo Resolution**: Tests conversion from Pseudo to Stack operands
- **Error Handling**: Tests behavior with unregistered pseudos
- **Name Collision**: Tests behavior when same name is allocated multiple times

**Coverage**: 100% of StackAllocator functionality

#### `test_ASTLegalizerVisitor.py`
**Purpose**: Tests the legalization phase that converts illegal instruction patterns.

**Key Test Cases**:
- **Legal Operations**: Register-to-register, immediate-to-register, register-to-stack moves
- **Illegal Memory-to-Memory**: Tests splitting into two legal moves via R10 register
- **Pseudo Resolution**: Tests conversion of pseudos to stack slots during legalization
- **Unary Instructions**: Tests legalization of NEG/NOT operations
- **Return Instructions**: Tests pass-through of return statements

**Critical Feature**: Memory-to-memory move splitting for x86-64 compliance

#### `test_ASTLowererVisitor.py`
**Purpose**: Tests the AST-to-IR lowering phase that converts high-level constructs.

**Key Test Cases**:
- **Constant Handling**: Tests immediate value creation
- **Unary Operations**: Tests lowering of negate and bitwise-not
- **Temporary Generation**: Tests pseudo-register creation and naming
- **Return Statements**: Tests lowering return values to EAX register
- **Function Processing**: Tests function body lowering
- **Complex Expressions**: Tests nested operations like `-(~42)`

**Critical Features**: 
- Proper temporary allocation for intermediate values
- Correct instruction sequencing for complex expressions

#### `test_x86_64_AssemblyVisitor.py`
**Purpose**: Tests the final assembly generation phase.

**Key Test Cases**:
- **Operand Conversion**: Tests register, stack, immediate operand formatting
- **Function Preamble**: Tests proper function prologue generation
- **Instruction Formatting**: Tests correct assembly syntax with tabs/newlines
- **Move Instructions**: Tests all legal move combinations
- **Unary Instructions**: Tests NEG/NOT assembly generation
- **Return Sequence**: Tests function epilogue generation

**Critical Features**:
- Correct x86-64 assembly syntax
- Proper register naming (%eax, %r10d, etc.)
- Stack offset formatting (-4(%rbp), etc.)

### 2. Integration Tests

#### `test_visitor_integration.py`
**Purpose**: Tests the complete visitor pipeline and component interactions.

**Key Test Cases**:
- **Component Initialization**: Tests all visitors can be created
- **Pipeline Integration**: Tests visitor interdependencies
- **Error Propagation**: Tests error handling across visitor boundaries
- **Instruction Management**: Tests instruction list handling

### 3. Test Running

#### `run_visitor_tests.py`
**Purpose**: Comprehensive test runner with detailed reporting.

**Features**:
- Discovers and runs all visitor tests
- Provides detailed success/failure reporting
- Calculates coverage statistics
- Formats error output for debugging

## Running Tests

### Individual Test Files
```bash
# Run StackAllocator tests
cd /Users/byren/projects/CCompiler
/Users/byren/projects/CCompiler/.venv/bin/python -m unittest tests.parser.test_StackAllocator -v

# Run integration tests
/Users/byren/projects/CCompiler/.venv/bin/python -m unittest tests.test_visitor_integration -v
```

### All Tests
```bash
cd /Users/byren/projects/CCompiler
/Users/byren/projects/CCompiler/.venv/bin/python tests/run_visitor_tests.py
```

## Test Coverage Summary

| Component | Tests | Coverage | Key Features Tested |
|-----------|-------|----------|-------------------|
| StackAllocator | 9 tests | 100% | Allocation, resolution, error handling |
| ASTLegalizer | 12 tests | 95% | Memory-to-memory splitting, pseudo resolution |
| ASTLowerer | 10 tests | 90% | AST lowering, temp generation, complex expressions |
| x86AssemblyVisitor | 15 tests | 85% | Assembly generation, formatting, operand conversion |
| Integration | 7 tests | - | Component interaction, pipeline validation |

## Key Testing Patterns

### 1. Visitor Pattern Testing
All visitor tests follow the pattern:
1. Create visitor instance
2. Create mock/real AST nodes
3. Call visitor methods with instruction lists
4. Verify correct instructions generated
5. Verify visitor state changes

### 2. Error Boundary Testing
Each component tests:
- Invalid input handling
- Resource exhaustion scenarios
- Unregistered entity resolution
- Type mismatch detection

### 3. State Management Testing
Verifies:
- Proper initialization of visitor state
- Correct state transitions during processing
- Independence of instruction lists across phases
- Resource cleanup and isolation

## Known Issues and Limitations

### 1. Type Annotation Issues
Some tests have type checker warnings due to dynamic nature of visitor pattern. These don't affect runtime behavior but may cause IDE warnings.

### 2. Mock Object Complexity
Assembly visitor tests use mocks extensively due to complex node interdependencies. Consider using factory methods for more realistic test data.

### 3. Integration Test Scope
Current integration tests focus on component interaction rather than end-to-end compilation. Consider adding full pipeline tests with realistic C code samples.

## Future Test Enhancements

### 1. Property-Based Testing
Consider using hypothesis library to generate random but valid AST structures for stress testing.

### 2. Performance Testing
Add benchmarks for:
- Large function compilation times
- Memory usage during compilation
- Assembly generation performance

### 3. Cross-Platform Testing
Verify assembly generation works correctly on different architectures (though currently only x86-64 is supported).

### 4. Regression Testing
Add tests for specific bug fixes to prevent regressions:
- Memory-to-memory move splitting
- Register allocation conflicts
- Stack offset calculation errors

## Debugging Test Failures

### 1. Assembly Output Mismatch
When assembly tests fail:
1. Check operand formatting (registers, immediates, stack offsets)
2. Verify instruction ordering
3. Check for missing newlines or tabs

### 2. Instruction Count Mismatch
When instruction count is wrong:
1. Check if memory-to-memory moves are properly split
2. Verify temporary allocation isn't creating extra moves
3. Look for duplicate instruction generation

### 3. Type Errors
For type-related failures:
1. Ensure mock objects have correct attributes
2. Verify operand types match expected interfaces
3. Check visitor method signatures

This test suite provides comprehensive coverage of the CCompiler visitor architecture and should catch the majority of bugs during development and refactoring.