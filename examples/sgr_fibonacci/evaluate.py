#!/usr/bin/env python3
"""
Evaluation script for Fibonacci optimization using SGR.

This script evaluates different Fibonacci implementations for correctness and performance.
"""

import sys
import json
import time
import importlib.util
from pathlib import Path


def run_shinka_eval():
    """Run evaluation of the Fibonacci implementation."""
    try:
        # Import the program to evaluate
        spec = importlib.util.spec_from_file_location("program", "main.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        results = {
            "correct": {"correct": False},
            "metrics": {
                "combined_score": 0.0,
                "public": {},
                "private": {},
                "text_feedback": ""
            }
        }

        # Test 1: Correctness for small values
        correctness_score = 0.0
        expected_values = [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 5), (6, 8), (7, 13), (8, 21), (9, 34), (10, 55)]

        try:
            for n, expected in expected_values:
                if hasattr(module, 'fibonacci'):
                    result = module.fibonacci(n)
                    if result == expected:
                        correctness_score += 1.0
                else:
                    break

            correctness_score = correctness_score / len(expected_values)

        except Exception as e:
            correctness_score = 0.0
            results["metrics"]["text_feedback"] += f"Correctness test failed: {e}. "

        # Test 2: Performance test (time limit)
        performance_score = 0.0

        if correctness_score > 0.8:  # Only test performance if correct
            try:
                # Test performance on larger value
                start_time = time.time()
                if hasattr(module, 'fibonacci'):
                    result = module.fibonacci(30)  # Should be fast for good implementations
                    end_time = time.time()

                    execution_time = end_time - start_time

                    # Performance scoring based on execution time
                    if execution_time < 0.001:  # Very fast (likely iterative/memoized)
                        performance_score = 1.0
                    elif execution_time < 0.01:  # Fast
                        performance_score = 0.8
                    elif execution_time < 0.1:  # Acceptable
                        performance_score = 0.6
                    elif execution_time < 1.0:  # Slow but works
                        performance_score = 0.4
                    else:  # Very slow
                        performance_score = 0.2

                    results["metrics"]["private"]["execution_time"] = execution_time

                else:
                    performance_score = 0.0

            except Exception as e:
                performance_score = 0.0
                results["metrics"]["text_feedback"] += f"Performance test failed: {e}. "

        # Test 3: Code quality assessment
        code_quality_score = 0.0

        try:
            # Read the source code
            with open("main.py", "r") as f:
                source_code = f.read()

            # Basic code quality checks
            quality_points = 0
            total_checks = 5

            # Check for memoization or iterative approach
            if "memo" in source_code.lower() or "cache" in source_code.lower():
                quality_points += 1
                results["metrics"]["text_feedback"] += "Uses memoization. "
            elif "for" in source_code or "while" in source_code:
                quality_points += 1
                results["metrics"]["text_feedback"] += "Uses iterative approach. "

            # Check for proper function definition
            if "def fibonacci(" in source_code:
                quality_points += 1

            # Check for docstring
            if '"""' in source_code or "'''" in source_code:
                quality_points += 1
                results["metrics"]["text_feedback"] += "Has documentation. "

            # Check for input validation
            if "if n <" in source_code or "if n ==" in source_code:
                quality_points += 1
                results["metrics"]["text_feedback"] += "Has input validation. "

            # Check for good variable names
            if len([line for line in source_code.split('\n') if 'fibonacci' in line.lower()]) >= 2:
                quality_points += 1

            code_quality_score = quality_points / total_checks

        except Exception as e:
            code_quality_score = 0.0
            results["metrics"]["text_feedback"] += f"Code quality assessment failed: {e}. "

        # Calculate combined score
        combined_score = (
            correctness_score * 0.6 +  # 60% weight on correctness
            performance_score * 0.3 +  # 30% weight on performance
            code_quality_score * 0.1   # 10% weight on code quality
        )

        # Set results
        results["correct"]["correct"] = correctness_score >= 0.8
        results["metrics"]["combined_score"] = combined_score
        results["metrics"]["public"] = {
            "correctness": correctness_score,
            "performance": performance_score,
            "code_quality": code_quality_score,
            "total_score": combined_score
        }
        results["metrics"]["private"]["test_cases_passed"] = int(correctness_score * len(expected_values))

        # Add improvement suggestions based on performance
        if performance_score < 0.6 and correctness_score > 0.8:
            results["metrics"]["text_feedback"] += "Consider optimizing for better performance (iterative or memoization). "
        if code_quality_score < 0.5:
            results["metrics"]["text_feedback"] += "Consider adding documentation and input validation. "
        if combined_score > 0.9:
            results["metrics"]["text_feedback"] += "Excellent implementation! "

        return results

    except Exception as e:
        return {
            "correct": {"correct": False},
            "metrics": {
                "combined_score": 0.0,
                "public": {"error": str(e)},
                "private": {"exception": str(e)},
                "text_feedback": f"Evaluation failed with error: {e}"
            }
        }


if __name__ == "__main__":
    result = run_shinka_eval()
    print(json.dumps(result, indent=2))