#!/usr/bin/env python3
"""
Evaluation script for Evolving Startup Agent.

Evaluates startup analysis quality, SEO opportunity identification,
quantitative analysis depth, and evolution fitness for ShinkaEvolve.
"""

import sys
import json
import time
import logging
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from initial import run_evolving_startup_analysis

logger = logging.getLogger(__name__)


def calculate_analysis_quality(result: dict) -> tuple[float, dict]:
    """Calculate startup analysis quality score."""
    if not result.get("correct", False):
        return 0.0, {"error": result.get("public_metrics", {}).get("error", "Unknown error")}

    public_metrics = result.get("public_metrics", {})
    details = {}
    score = 0.0

    # Market size analysis (25%)
    market_size = public_metrics.get("market_size_usd", 0)
    if market_size > 0:
        # Score based on market size scale (higher = better)
        market_score = min(market_size / 1_000_000_000, 1.0)  # Normalize by $1B
        score += market_score * 0.25
        details["market_size_score"] = market_score
        details["market_size_usd"] = market_size

    # SEO opportunity identification (30%)
    seo_count = public_metrics.get("seo_opportunities_count", 0)
    if seo_count > 0:
        seo_score = min(seo_count / 15, 1.0)  # Target: 15 SEO opportunities
        score += seo_score * 0.30
        details["seo_score"] = seo_score
        details["seo_opportunities"] = seo_count

    # Competitive analysis depth (20%)
    competitors = public_metrics.get("competitors_count", 0)
    if competitors > 0:
        competitor_score = min(competitors / 8, 1.0)  # Target: 8 competitors
        score += competitor_score * 0.20
        details["competitor_score"] = competitor_score
        details["competitors_analyzed"] = competitors

    # Financial viability (15%)
    break_even = public_metrics.get("break_even_month", 24)
    funding = public_metrics.get("funding_requirements", 0)

    # Earlier break-even is better
    break_even_score = max(0, (24 - break_even) / 24) if break_even <= 24 else 0

    # Reasonable funding requirement (not too high, not zero)
    if 10_000 <= funding <= 1_000_000:
        funding_score = 1.0
    elif funding == 0:
        funding_score = 0.5  # Unrealistic
    else:
        funding_score = max(0, 1.0 - (funding - 1_000_000) / 10_000_000)

    financial_score = (break_even_score + funding_score) / 2
    score += financial_score * 0.15
    details["financial_score"] = financial_score
    details["break_even_month"] = break_even
    details["funding_requirements"] = funding

    # Product completeness (10%)
    features = public_metrics.get("features_count", 0)
    if features > 0:
        features_score = min(features / 10, 1.0)  # Target: 10 features
        score += features_score * 0.10
        details["features_score"] = features_score
        details["features_count"] = features

    return min(score, 1.0), details


def calculate_evolution_fitness(result: dict) -> tuple[float, dict]:
    """Calculate evolution-specific fitness score."""
    if not result.get("correct", False):
        return 0.0, {"error": "Analysis failed"}

    # Use the fitness score calculated by the agent itself
    fitness_score = result.get("public_metrics", {}).get("fitness_score", 0.0)

    details = {
        "evolution_fitness": fitness_score,
        "fitness_components": "market_size + seo_opportunity + competition + feasibility + timing"
    }

    return fitness_score, details


def calculate_quantitative_depth(result: dict) -> tuple[float, dict]:
    """Calculate quantitative analysis depth score."""
    if not result.get("correct", False):
        return 0.0, {"error": "No analysis to evaluate"}

    public_metrics = result.get("public_metrics", {})
    details = {}
    score = 0.0

    # Check for specific quantitative metrics presence
    quantitative_indicators = [
        ("market_size_usd", public_metrics.get("market_size_usd", 0) > 0),
        ("seo_opportunities", public_metrics.get("seo_opportunities_count", 0) >= 5),
        ("competitor_metrics", public_metrics.get("competitors_count", 0) >= 3),
        ("financial_projections", public_metrics.get("break_even_month", 0) > 0),
        ("funding_analysis", public_metrics.get("funding_requirements", 0) > 0),
        ("feature_specification", public_metrics.get("features_count", 0) >= 5)
    ]

    present_indicators = sum(1 for _, present in quantitative_indicators if present)
    score = present_indicators / len(quantitative_indicators)

    details["quantitative_indicators_present"] = present_indicators
    details["total_indicators"] = len(quantitative_indicators)
    details["indicator_details"] = {name: present for name, present in quantitative_indicators}

    return score, details


def calculate_seo_strategy_quality(result: dict) -> tuple[float, dict]:
    """Calculate SEO strategy quality score."""
    if not result.get("correct", False):
        return 0.0, {"error": "No SEO analysis"}

    public_metrics = result.get("public_metrics", {})
    details = {}
    score = 0.0

    # SEO keyword coverage
    seo_opportunities = public_metrics.get("seo_opportunities_count", 0)
    if seo_opportunities >= 10:
        keyword_score = 1.0
    elif seo_opportunities >= 5:
        keyword_score = 0.7
    elif seo_opportunities >= 1:
        keyword_score = 0.4
    else:
        keyword_score = 0.0

    score += keyword_score * 0.6  # 60% weight for keyword identification

    # Seasonal focus (Christmas 2025-2026)
    # Assume high seasonal focus if analysis was completed successfully
    seasonal_score = 1.0 if result.get("correct") else 0.0
    score += seasonal_score * 0.4  # 40% weight for seasonal strategy

    details["keyword_score"] = keyword_score
    details["seasonal_focus_score"] = seasonal_score
    details["seo_opportunities_found"] = seo_opportunities

    return score, details


def run_shinka_eval() -> dict:
    """Main evaluation function for ShinkaEvolve."""
    start_time = time.time()

    try:
        # Run evolving startup analysis
        logger.info("🧬 Starting evolving startup analysis evaluation...")
        result = run_evolving_startup_analysis()

        execution_time = time.time() - start_time
        logger.info(f"⏱️ Execution completed in {execution_time:.2f} seconds")

        # Calculate component scores
        analysis_quality, analysis_details = calculate_analysis_quality(result)
        evolution_fitness, evolution_details = calculate_evolution_fitness(result)
        quantitative_depth, depth_details = calculate_quantitative_depth(result)
        seo_quality, seo_details = calculate_seo_strategy_quality(result)

        # Time efficiency (target: 2-3 minutes for comprehensive analysis)
        target_time = 180.0  # 3 minutes
        if execution_time <= target_time:
            time_score = 1.0
        elif execution_time <= target_time * 1.5:
            time_score = 1.0 - (execution_time - target_time) / (target_time * 0.5)
        else:
            time_score = 0.3  # Minimum for very slow execution

        # Combined fitness score (weighted for startup analysis priorities)
        combined_score = (
            analysis_quality * 0.30 +      # Analysis quality
            evolution_fitness * 0.25 +     # Evolution fitness
            quantitative_depth * 0.20 +    # Quantitative depth
            seo_quality * 0.20 +           # SEO strategy
            time_score * 0.05              # Time efficiency
        )

        # Compile detailed metrics
        public_metrics = {
            "analysis_quality": analysis_quality,
            "evolution_fitness": evolution_fitness,
            "quantitative_depth": quantitative_depth,
            "seo_strategy_quality": seo_quality,
            "time_efficiency": time_score,
            "execution_time": execution_time,
            **result.get("public_metrics", {})
        }

        private_metrics = {
            "analysis_details": analysis_details,
            "evolution_details": evolution_details,
            "depth_details": depth_details,
            "seo_details": seo_details,
            "time_score": time_score,
            **result.get("private_metrics", {})
        }

        evaluation_result = {
            "combined_score": combined_score,
            "correct": result.get("correct", False),
            "public_metrics": public_metrics,
            "private_metrics": private_metrics,
            "text_feedback": f"Analysis: {analysis_quality:.3f}, Evolution: {evolution_fitness:.3f}, Quant: {quantitative_depth:.3f}, SEO: {seo_quality:.3f}"
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