"""
SGR-Enhanced PromptSampler for ShinkaEvolve.

This module extends the original PromptSampler with Schema-Guided Reasoning
capabilities for intelligent mutation strategy selection.
"""

import logging
from typing import List, Optional, Tuple
import numpy as np
from shinka.database import Program
from shinka.llm import LLMClient
from shinka.prompts import (
    construct_eval_history_msg,
    perf_str,
    format_text_feedback_section,
    BASE_SYSTEM_MSG,
    DIFF_SYS_FORMAT,
    DIFF_ITER_MSG,
    FULL_ITER_MSG,
    FULL_SYS_FORMATS,
    CROSS_SYS_FORMAT,
    CROSS_ITER_MSG,
    get_cross_component,
)
from shinka.prompts.prompts_init import INIT_SYSTEM_MSG, INIT_USER_MSG
from .sampler import PromptSampler  # Original sampler for fallback
from .sgr_mutation_planner import SGRMutationPlanner
from .sgr_schemas import CodeMutationPlan

logger = logging.getLogger(__name__)


class SGRPromptSampler(PromptSampler):
    """
    SGR-enhanced PromptSampler that uses structured reasoning for strategy selection.

    Maintains backward compatibility with original PromptSampler while adding
    intelligent mutation planning capabilities.
    """

    def __init__(
        self,
        task_sys_msg: Optional[str] = None,
        language: str = "python",
        patch_types: Optional[List[str]] = None,
        patch_type_probs: Optional[List[float]] = None,
        use_text_feedback: bool = False,
        # SGR-specific parameters
        sgr_enabled: bool = True,
        sgr_llm_client: Optional[LLMClient] = None,
        sgr_confidence_threshold: float = 0.7,
        sgr_fallback_to_random: bool = True,
    ):
        """
        Initialize SGR-enhanced PromptSampler.

        Args:
            task_sys_msg: Task-specific system message
            language: Programming language
            patch_types: Available patch types
            patch_type_probs: Probabilities for each patch type
            use_text_feedback: Whether to use text feedback
            sgr_enabled: Whether to use SGR for strategy selection
            sgr_llm_client: LLM client for SGR (if None, uses default models)
            sgr_confidence_threshold: Minimum confidence for accepting SGR decisions
            sgr_fallback_to_random: Whether to fallback to random on SGR failure
        """
        # Initialize parent class
        super().__init__(
            task_sys_msg=task_sys_msg,
            language=language,
            patch_types=patch_types,
            patch_type_probs=patch_type_probs,
            use_text_feedback=use_text_feedback,
        )

        # SGR-specific initialization
        self.sgr_enabled = sgr_enabled
        self.sgr_confidence_threshold = sgr_confidence_threshold
        self.sgr_fallback_to_random = sgr_fallback_to_random

        # Initialize SGR mutation planner if enabled
        if self.sgr_enabled:
            if sgr_llm_client is None:
                # Create a default LLM client for SGR
                # Using a reasonable model for structured output
                sgr_llm_client = LLMClient(
                    model_names=["gpt-4o-mini-2024-07-18"],  # Good for structured output
                    verbose=False,
                )

            self.sgr_planner = SGRMutationPlanner(
                llm_client=sgr_llm_client,
                language=language,
                task_sys_msg=task_sys_msg,
                use_text_feedback=use_text_feedback,
                fallback_to_random=sgr_fallback_to_random,
            )
        else:
            self.sgr_planner = None

        # Tracking statistics
        self.sgr_stats = {
            "total_attempts": 0,
            "sgr_successes": 0,
            "sgr_failures": 0,
            "fallback_used": 0,
            "low_confidence": 0,
        }

    def sample(
        self,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
    ) -> Tuple[str, str, str]:
        """
        Sample mutation strategy using SGR or fallback to original method.

        Returns:
            Tuple of (system_message, user_message, patch_type)
        """
        self.sgr_stats["total_attempts"] += 1

        # Try SGR-based strategy selection first
        if self.sgr_enabled and self.sgr_planner:
            try:
                sgr_result = self._try_sgr_strategy(
                    parent, archive_inspirations, top_k_inspirations, meta_recommendations
                )
                if sgr_result:
                    system_msg, user_msg, patch_type = sgr_result
                    self.sgr_stats["sgr_successes"] += 1
                    logger.debug(f"SGR strategy selected: {patch_type}")
                    return system_msg, user_msg, patch_type
                else:
                    self.sgr_stats["sgr_failures"] += 1
                    logger.debug("SGR strategy selection failed, using fallback")
            except Exception as e:
                self.sgr_stats["sgr_failures"] += 1
                logger.warning(f"SGR strategy selection error: {e}")

        # Fallback to original sampling method
        self.sgr_stats["fallback_used"] += 1
        return super().sample(parent, archive_inspirations, top_k_inspirations, meta_recommendations)

    def _try_sgr_strategy(
        self,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
    ) -> Optional[Tuple[str, str, str]]:
        """
        Attempt SGR-based strategy selection.

        Returns:
            Tuple of (system_msg, user_msg, patch_type) or None if failed
        """
        # Get SGR mutation plan
        mutation_plan, fallback_strategy = self.sgr_planner.plan_mutation(
            parent, archive_inspirations, top_k_inspirations, meta_recommendations
        )

        if mutation_plan is None:
            # SGR planning failed
            if fallback_strategy:
                # Use simple fallback strategy
                return self._build_prompts_for_strategy(
                    fallback_strategy, parent, archive_inspirations,
                    top_k_inspirations, meta_recommendations
                )
            return None

        # Check confidence threshold
        if mutation_plan.strategy.confidence < self.sgr_confidence_threshold:
            self.sgr_stats["low_confidence"] += 1
            logger.debug(f"SGR confidence too low: {mutation_plan.strategy.confidence:.2f} "
                        f"< {self.sgr_confidence_threshold}")
            return None

        # Build prompts for the selected strategy
        strategy_type = mutation_plan.strategy.strategy_type

        # Map SGR strategy types to original patch types
        if strategy_type == "focused":
            # Map focused to diff for now (could be enhanced later)
            strategy_type = "diff"

        # Validate strategy type
        if strategy_type not in ["diff", "full", "cross"]:
            logger.warning(f"Unknown SGR strategy type: {strategy_type}, using diff")
            strategy_type = "diff"

        return self._build_prompts_for_strategy(
            strategy_type, parent, archive_inspirations,
            top_k_inspirations, meta_recommendations, mutation_plan
        )

    def _build_prompts_for_strategy(
        self,
        strategy_type: str,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
        mutation_plan: Optional[CodeMutationPlan] = None,
    ) -> Tuple[str, str, str]:
        """
        Build prompts for a specific strategy type.

        Args:
            strategy_type: The mutation strategy to use
            parent: Parent program
            archive_inspirations: Archive inspiration programs
            top_k_inspirations: Top-k inspiration programs
            meta_recommendations: Meta recommendations
            mutation_plan: Optional SGR mutation plan for enhanced prompts

        Returns:
            Tuple of (system_msg, user_msg, patch_type)
        """
        # Start with base system message
        if self.task_sys_msg is None:
            sys_msg = BASE_SYSTEM_MSG
        else:
            sys_msg = self.task_sys_msg

        # Add strategy-specific formatting
        if strategy_type == "diff":
            sys_msg += DIFF_SYS_FORMAT
        elif strategy_type == "full":
            # Randomly sample from different full rewrite variants
            full_variant_idx = np.random.randint(0, len(FULL_SYS_FORMATS))
            selected_format = FULL_SYS_FORMATS[full_variant_idx]
            sys_msg += selected_format
        elif strategy_type == "cross":
            sys_msg += CROSS_SYS_FORMAT

        # Add SGR-specific guidance if available
        if mutation_plan:
            sgr_guidance = self._build_sgr_guidance(mutation_plan)
            sys_msg += sgr_guidance

        # Build evaluation history message
        eval_history_msg = ""
        if len(archive_inspirations) > 0:
            eval_history_msg = construct_eval_history_msg(
                archive_inspirations,
                language=self.language,
                include_text_feedback=self.use_text_feedback,
            )

        # Add top-k inspirations
        if len(top_k_inspirations) > 0:
            eval_history_msg += construct_eval_history_msg(
                top_k_inspirations,
                language=self.language,
                include_text_feedback=self.use_text_feedback,
            )

        # Format text feedback section for current program
        text_feedback_section = ""
        if self.use_text_feedback:
            text_feedback_section = "\n" + format_text_feedback_section(
                parent.text_feedback
            )

        # Build iteration message based on strategy
        if strategy_type == "diff":
            iter_msg = DIFF_ITER_MSG.format(
                language=self.language,
                code_content=parent.code,
                performance_metrics=perf_str(
                    parent.combined_score, parent.public_metrics
                ),
                text_feedback_section=text_feedback_section,
            )
        elif strategy_type == "full":
            iter_msg = FULL_ITER_MSG.format(
                language=self.language,
                code_content=parent.code,
                performance_metrics=perf_str(
                    parent.combined_score, parent.public_metrics
                ),
                text_feedback_section=text_feedback_section,
            )
        elif strategy_type == "cross":
            iter_msg = CROSS_ITER_MSG.format(
                language=self.language,
                code_content=parent.code,
                performance_metrics=perf_str(
                    parent.combined_score, parent.public_metrics
                ),
                text_feedback_section=text_feedback_section,
            )
            iter_msg += "\n\n" + get_cross_component(
                archive_inspirations,
                top_k_inspirations,
                language=self.language,
            )
        else:
            raise ValueError(f"Invalid strategy type: {strategy_type}")

        # Add meta-recommendations if provided and not cross strategy
        sum_rec_msg = ""
        if meta_recommendations not in [None, "none"] and strategy_type != "cross":
            sum_rec_msg += "\n\n# Potential Recommendations"
            sum_rec_msg += (
                "\nThe following are potential recommendations for the "
                "next program generations:\n\n"
            )
            sum_rec_msg += f"\n{meta_recommendations}"

        return (
            sys_msg + sum_rec_msg,
            eval_history_msg + "\n" + iter_msg,
            strategy_type,
        )

    def _build_sgr_guidance(self, mutation_plan: CodeMutationPlan) -> str:
        """
        Build SGR-specific guidance to include in the system message.

        Args:
            mutation_plan: The SGR mutation plan

        Returns:
            String with SGR guidance
        """
        guidance = "\n\n# SGR Mutation Guidance\n"
        guidance += f"**Strategy Reasoning:** {mutation_plan.strategy.reasoning}\n"
        guidance += f"**Expected Improvement:** {mutation_plan.strategy.expected_improvement}\n"
        guidance += f"**Risk Level:** {mutation_plan.strategy.risk_level}\n"

        if mutation_plan.strategy.target_areas:
            guidance += f"**Focus Areas:** {', '.join(mutation_plan.strategy.target_areas)}\n"

        if mutation_plan.analysis.performance_bottlenecks:
            guidance += f"**Performance Bottlenecks:** {', '.join(mutation_plan.analysis.performance_bottlenecks)}\n"

        if mutation_plan.analysis.optimization_opportunities:
            guidance += f"**Optimization Opportunities:** {', '.join(mutation_plan.analysis.optimization_opportunities)}\n"

        guidance += f"**Success Criteria:** {mutation_plan.success_criteria}\n"

        return guidance

    def get_sgr_statistics(self) -> dict:
        """Get SGR usage statistics."""
        total = self.sgr_stats["total_attempts"]
        if total == 0:
            return self.sgr_stats

        stats = self.sgr_stats.copy()
        stats["sgr_success_rate"] = stats["sgr_successes"] / total
        stats["fallback_rate"] = stats["fallback_used"] / total
        return stats

    def reset_sgr_statistics(self):
        """Reset SGR statistics."""
        self.sgr_stats = {
            "total_attempts": 0,
            "sgr_successes": 0,
            "sgr_failures": 0,
            "fallback_used": 0,
            "low_confidence": 0,
        }