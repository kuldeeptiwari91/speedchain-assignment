#!/usr/bin/env python3
"""
Test runner script
Usage: python tests/run_tests.py
"""

import pytest
import sys
from pathlib import Path

def run_tests():
    """Run all tests with coverage"""
    
    # Change to backend directory
    backend_dir = Path(__file__).parent.parent
    
    # Run pytest with coverage
    exit_code = pytest.main([
        str(backend_dir / "tests"),
        "-v",  # Verbose
        "--cov=services",  # Coverage for services
        "--cov=utils",  # Coverage for utils
        "--cov=routes",  # Coverage for routes
        "--cov-report=html",  # HTML coverage report
        "--cov-report=term-missing",  # Show missing lines in terminal
    ])
    
    print("\n" + "="*50)
    if exit_code == 0:
        print("✅ All tests passed!")
        print(f"📊 Coverage report: {backend_dir}/htmlcov/index.html")
    else:
        print("❌ Some tests failed!")
    print("="*50)
    
    return exit_code

if __name__ == "__main__":
    sys.exit(run_tests())