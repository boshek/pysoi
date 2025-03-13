#!/usr/bin/env python
"""
Run tests for the pysoi package.

This script can be run directly to execute all the tests.
"""

import sys
import pytest


if __name__ == "__main__":
    # Run the tests
    result = pytest.main(["-xvs", "tests/test_pysoi"])
    
    # Exit with the appropriate code
    sys.exit(result)
