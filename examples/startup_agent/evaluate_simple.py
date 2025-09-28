#!/usr/bin/env python3
"""
Simple evaluation script for Startup Agent.
Works with basic PRD generation without web research.
"""

import sys
import json
import time
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from test_basic import test_basic_prd_generation

logger = logging.getLogger(__name__)


def calculate_prd_quality(result: dict) -> tuple[float, dict]:
    """Calculate PRD quality score."""
    if not result.get("success", False):
        return 0.0, {"error": result.get("error", "Unknown error")}

    prd = result.get("prd")
    if not prd:
        return 0.0, {"error": "No PRD generated"}

    details = {}
    score = 0.0

    # Core fields completeness (40%)
    core_score = 0.0
    if hasattr(prd, 'product_name') and prd.product_name:
        core_score += 0.15
        details["has_product_name"] = True
    if hasattr(prd, 'vision') and prd.vision and len(prd.vision) > 20:
        core_score += 0.15
        details["has_vision"] = True
    if hasattr(prd, 'target_market') and prd.target_market:
        core_score += 0.1
        details["has_target_market"] = True

    score += core_score * 0.4
    details["core_score"] = core_score

    # Features quality (35%)
    features_score = 0.0
    features_count = result.get("features_count", 0)
    if features_count >= 3:
        features_score += min(features_count / 5.0, 1.0)  # Optimal: 5 features
        details["features_count"] = features_count
        details["features_adequate"] = True

    score += features_score * 0.35
    details["features_score"] = features_score

    # Metrics quality (25%)
    metrics_score = 0.0
    metrics_count = result.get("metrics_count", 0)
    if metrics_count >= 3:
        metrics_score += min(metrics_count / 5.0, 1.0)  # Optimal: 5 metrics
        details["metrics_count"] = metrics_count
        details["metrics_adequate"] = True

    score += metrics_score * 0.25
    details["metrics_score"] = metrics_score

    return min(score, 1.0), details


def run_shinka_eval() -> dict:
    """Main evaluation function for ShinkaEvolve."""
    start_time = time.time()

    try:
        # Run startup PRD generation test
        logger.info("🚀 Starting startup PRD evaluation...")
        result = test_basic_prd_generation()

        execution_time = time.time() - start_time
        logger.info(f"⏱️ Execution completed in {execution_time:.2f} seconds")

        # Calculate quality score
        prd_quality, quality_details = calculate_prd_quality(result)

        # Time efficiency (faster is better, but not too fast)
        target_time = 30.0  # 30 seconds target for simple test
        if execution_time <= target_time:
            time_score = 1.0
        elif execution_time <= target_time * 2:
            time_score = 1.0 - (execution_time - target_time) / target_time
        else:
            time_score = 0.3  # Minimum for very slow execution

        # Combined score
        combined_score = prd_quality * 0.8 + time_score * 0.2

        # Public metrics
        public_metrics = {
            "prd_quality": prd_quality,
            "time_efficiency": time_score,
            "execution_time": execution_time,
            "features_count": result.get("features_count", 0),
            "metrics_count": result.get("metrics_count", 0),
            "success": result.get("success", False)
        }

        # Private metrics
        private_metrics = {
            "quality_details": quality_details,
            "full_result": result
        }

        evaluation_result = {
            "combined_score": combined_score,
            "correct": result.get("success", False),
            "public_metrics": public_metrics,
            "private_metrics": private_metrics,
            "text_feedback": f"PRD Quality: {prd_quality:.3f}, Time: {time_score:.3f}, Features: {result.get('features_count', 0)}"
        }

        logger.info(f"✅ Evaluation completed - Combined Score: {combined_score:.3f}")
        return evaluation_result

    except Exception as e:
        logger.error(f"❌ Evaluation failed: {e}")
        execution_time = time.time() - start_time

        return {
            "combined_score": 0.0,
            "correct": False,
            "public_metrics": {
                "error": str(e),
                "execution_time": execution_time
            },
            "private_metrics": {},
            "text_feedback": f"Evaluation failed: {str(e)}"
        }


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run evaluation
    result = run_shinka_eval()

    # Output result as JSON for ShinkaEvolve
    print(json.dumps(result, indent=2, default=str))