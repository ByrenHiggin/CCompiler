#!/usr/bin/env python3
# tests/test_all_test_files.py

import os
import subprocess
import sys
from pathlib import Path
import traceback

# Directory containing the files you want to run tests on
TEST_DIR = Path(os.path.dirname(os.path.dirname(__file__))) / "writing-a-c-compiler-tests" / "tests" / "chapter_4"
# Pattern to match C files
PATTERN = "*.c"

# Path to main.py in the root directory
MAIN_SCRIPT = Path(os.path.dirname(os.path.dirname(__file__))) / "main.py"

def collect_files():
    """Collect all .c files from the test directory"""
    if not TEST_DIR.exists():
        raise FileNotFoundError(f"TEST_DIR not found: {TEST_DIR}")
    return sorted(p for p in TEST_DIR.rglob(PATTERN) if p.is_file())

def process_file(path: Path):
    """Run main.py with the given file as input"""
    print(f"Testing: {path}")
    
    result = subprocess.run(
        [sys.executable, str(MAIN_SCRIPT), str(path)],
        capture_output=True,
        text=True,
        check=False
    )
    
    # For pass/fail tests based on expected return code
    if result.returncode != 0:
        # If we're in an invalid/ directory, failure is expected
        if "invalid" in str(path) or "invalid_parse" in str(path):
            print(f"✅ PASS: {path.name} (expected failure)")
            return True
        else:
            # Test fails because valid file caused an error
            print(f"❌ FAIL: {path.name}")
            print(f"Error processing file. Exit code: {result.returncode}")
            if result.stdout.strip():
                print(f"STDOUT: {result.stdout}")
            if result.stderr.strip():
                print(f"STDERR: {result.stderr}")
            return False
    else:
        # If we're in an invalid/ directory, success is unexpected
        if "invalid" in str(path) or "invalid_parse" in str(path):
            # Test fails because invalid file didn't cause an error
            print(f"❌ FAIL: {path.name}")
            print(f"Invalid test case unexpectedly passed with exit code 0")
            return False
        else:
            # Test passes because valid file was processed successfully
            print(f"✅ PASS: {path.name}")
            return True

def run_all_tests():
    """Run all test files and report results"""
    try:
        test_files = collect_files()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    
    if not test_files:
        print(f"No test files found in {TEST_DIR}")
        return 1
    
    print(f"Found {len(test_files)} test files")
    print("-" * 50)
    
    # Run each test file
    passed = 0
    failed = 0
    failed_tests: list[str] = []
    
    for path in test_files:
        try:
            if process_file(path):
                passed += 1
            else:
                failed += 1
                failed_tests.append(path.name)
        except Exception:
            failed += 1
            failed_tests.append(path.name)
            tb = traceback.format_exc()
            print(f"❌ FAIL: {path.name}")
            print(f"Exception: {tb}")
        
        print("-" * 50)
    
    # Summary
    print(f"\nTest Results: {passed} passed, {failed} failed")
    if failed_tests:
        print("Failed tests:")
        for test in failed_tests:
            print(f"  - {test}")
        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(run_all_tests())