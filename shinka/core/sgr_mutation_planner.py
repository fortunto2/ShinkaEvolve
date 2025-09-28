"""
SGR-based Mutation Planning for ShinkaEvolve.

This module implements Schema-Guided Reasoning for intelligent mutation strategy selection.
Instead of random strategy selection, it uses LLM with structured output to analyze
code and choose optimal mutation approaches.
"""

import logging
from typing import List, Optional, Tuple
from shinka.database import Program
from shinka.llm import LLMClient
from shinka.prompts import (
    construct_eval_history_msg,
    perf_str,
    format_text_feedback_section,
)
from .sgr_schemas import CodeAnalysis, MutationStrategy, CodeMutationPlan

logger = logging.getLogger(__name__)


SGR_ANALYSIS_SYSTEM_PROMPT = """You are an expert code analyst specializing in evolutionary programming optimization.

Your task is to analyze a given program and provide a structured assessment of its characteristics, performance bottlenecks, and optimization opportunities. This analysis will guide the selection of the most effective mutation strategy for code evolution.

Key considerations:
1. Code complexity and structure
2. Performance characteristics and bottlenecks
3. Code quality and maintainability issues
4. Optimization opportunities
5. Areas suitable for targeted improvements

Provide your analysis in a structured format that enables informed decision-making for code mutations."""


SGR_STRATEGY_SYSTEM_PROMPT = """You are an expert mutation strategy selector for evolutionary programming.

Given a code analysis and context from previous evolution attempts, select the most appropriate mutation strategy and provide detailed reasoning.

Available mutation strategies:
- "diff": Apply targeted patches to specific code sections (best for localized improvements)
- "full": Complete rewrite of the program (best for structural changes)
- "cross": Combine elements from multiple successful programs (best when good inspirations exist)
- "focused": Targeted modifications to specific functions/algorithms (best for performance optimization)

Consider:
1. Code complexity and current performance
2. Available inspiration programs and their success patterns
3. Risk vs. potential reward for each strategy
4. Stage of evolution (early exploration vs. late optimization)

Provide structured reasoning and high-confidence strategy selection."""


class SGRMutationPlanner:
    """Schema-Guided Reasoning based mutation planner."""

    def __init__(
        self,
        llm_client: LLMClient,
        language: str = "python",
        task_sys_msg: Optional[str] = None,
        use_text_feedback: bool = False,
        fallback_to_random: bool = True,
    ):
        """
        Initialize SGR Mutation Planner.

        Args:
            llm_client: LLM client with structured output support
            language: Programming language
            task_sys_msg: Task-specific system message
            use_text_feedback: Whether to include text feedback in analysis
            fallback_to_random: Whether to fallback to random selection on SGR failure
        """
        self.llm_client = llm_client
        self.language = language
        self.task_sys_msg = task_sys_msg
        self.use_text_feedback = use_text_feedback
        self.fallback_to_random = fallback_to_random

        # Create LLM clients with structured output for each step
        self.analysis_llm = LLMClient(
            model_names=llm_client.model_names,
            model_selection=llm_client.llm_selection,
            output_model=CodeAnalysis,
            verbose=llm_client.verbose,
            **llm_client.__dict__.get('llm_kwargs', {})
        )

        self.strategy_llm = LLMClient(
            model_names=llm_client.model_names,
            model_selection=llm_client.llm_selection,
            output_model=MutationStrategy,
            verbose=llm_client.verbose,
            **llm_client.__dict__.get('llm_kwargs', {})
        )

    def analyze_code(self, program: Program) -> Optional[CodeAnalysis]:
        """
        Analyze code characteristics using SGR.

        Args:
            program: Program to analyze

        Returns:
            CodeAnalysis object or None if analysis fails
        """
        try:
            # Prepare analysis prompt
            analysis_prompt = self._build_analysis_prompt(program)

            # Query LLM with structured output
            result = self.analysis_llm.query(
                msg=analysis_prompt,
                system_msg=SGR_ANALYSIS_SYSTEM_PROMPT,
                msg_history=[]
            )

            if result and hasattr(result, 'parsed_content') and result.parsed_content:
                logger.debug(f"SGR: Using parsed_content: {type(result.parsed_content)}")
                return result.parsed_content
            elif result and result.content:
                # Try to parse manually if structured parsing failed
                logger.debug(f"SGR: Attempting manual parsing of content: {result.content[:200]}...")
                try:
                    import json
                    # First try to parse as JSON
                    parsed = json.loads(result.content)
                    logger.debug(f"SGR: Successfully parsed JSON: {parsed}")
                    return CodeAnalysis(**parsed)
                except json.JSONDecodeError as e:
                    logger.debug(f"SGR: JSON parsing failed: {e}")
                    # Try to extract JSON from markdown or other formats
                    content = result.content.strip()

                    # Check if it's wrapped in markdown code blocks
                    if "```json" in content:
                        import re
                        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1)
                            try:
                                parsed = json.loads(json_str)
                                logger.debug(f"SGR: Successfully parsed markdown JSON: {parsed}")
                                return CodeAnalysis(**parsed)
                            except Exception as e2:
                                logger.debug(f"SGR: Markdown JSON parsing failed: {e2}")

                    # Check if it's wrapped in plain code blocks
                    if "```" in content:
                        import re
                        code_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
                        if code_match:
                            json_str = code_match.group(1)
                            try:
                                parsed = json.loads(json_str)
                                logger.debug(f"SGR: Successfully parsed code block JSON: {parsed}")
                                return CodeAnalysis(**parsed)
                            except Exception as e3:
                                logger.debug(f"SGR: Code block JSON parsing failed: {e3}")

                    logger.warning(f"SGR: Failed to parse analysis result. Content: {content[:500]}")
                except Exception as e:
                    logger.warning(f"SGR: Manual parsing failed with error: {e}")
                    logger.debug(f"SGR: Raw content was: {result.content}")
            else:
                logger.warning("SGR: No content received from LLM")

        except Exception as e:
            logger.warning(f"SGR code analysis failed: {e}")

        return None

    def select_strategy(
        self,
        analysis: CodeAnalysis,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
    ) -> Optional[MutationStrategy]:
        """
        Select mutation strategy using SGR.

        Args:
            analysis: Code analysis from analyze_code
            parent: Parent program
            archive_inspirations: Archive inspiration programs
            top_k_inspirations: Top-k inspiration programs
            meta_recommendations: Meta recommendations

        Returns:
            MutationStrategy object or None if selection fails
        """
        try:
            # Prepare strategy selection prompt
            strategy_prompt = self._build_strategy_prompt(
                analysis, parent, archive_inspirations, top_k_inspirations, meta_recommendations
            )

            # Query LLM with structured output
            result = self.strategy_llm.query(
                msg=strategy_prompt,
                system_msg=SGR_STRATEGY_SYSTEM_PROMPT,
                msg_history=[]
            )

            if result and hasattr(result, 'parsed_content') and result.parsed_content:
                logger.debug(f"SGR: Using strategy parsed_content: {type(result.parsed_content)}")
                return result.parsed_content
            elif result and result.content:
                # Try to parse manually if structured parsing failed
                logger.debug(f"SGR: Attempting manual parsing of strategy: {result.content[:200]}...")
                try:
                    import json
                    # First try to parse as JSON
                    parsed = json.loads(result.content)
                    logger.debug(f"SGR: Successfully parsed strategy JSON: {parsed}")
                    return MutationStrategy(**parsed)
                except json.JSONDecodeError as e:
                    logger.debug(f"SGR: Strategy JSON parsing failed: {e}")
                    # Try to extract JSON from markdown or other formats
                    content = result.content.strip()

                    # Check if it's wrapped in markdown code blocks
                    if "```json" in content:
                        import re
                        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group(1)
                            try:
                                parsed = json.loads(json_str)
                                logger.debug(f"SGR: Successfully parsed strategy markdown JSON: {parsed}")
                                return MutationStrategy(**parsed)
                            except Exception as e2:
                                logger.debug(f"SGR: Strategy markdown JSON parsing failed: {e2}")

                    # Check if it's wrapped in plain code blocks
                    if "```" in content:
                        import re
                        code_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', content, re.DOTALL)
                        if code_match:
                            json_str = code_match.group(1)
                            try:
                                parsed = json.loads(json_str)
                                logger.debug(f"SGR: Successfully parsed strategy code block JSON: {parsed}")
                                return MutationStrategy(**parsed)
                            except Exception as e3:
                                logger.debug(f"SGR: Strategy code block JSON parsing failed: {e3}")

                    logger.warning(f"SGR: Failed to parse strategy result. Content: {content[:500]}")
                except Exception as e:
                    logger.warning(f"SGR: Strategy manual parsing failed with error: {e}")
                    logger.debug(f"SGR: Raw strategy content was: {result.content}")
            else:
                logger.warning("SGR: No strategy content received from LLM")

        except Exception as e:
            logger.warning(f"SGR strategy selection failed: {e}")

        return None

    def plan_mutation(
        self,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
    ) -> Tuple[Optional[CodeMutationPlan], Optional[str]]:
        """
        Create complete mutation plan using SGR.

        Args:
            parent: Parent program
            archive_inspirations: Archive inspiration programs
            top_k_inspirations: Top-k inspiration programs
            meta_recommendations: Meta recommendations

        Returns:
            Tuple of (CodeMutationPlan or None, fallback_strategy or None)
        """
        # Step 1: Analyze code
        analysis = self.analyze_code(parent)
        if not analysis:
            logger.info("SGR analysis failed, will use fallback")
            return None, self._get_fallback_strategy()

        logger.info(f"SGR Analysis: complexity={analysis.complexity}, "
                   f"algorithm={analysis.main_algorithm}")

        # Step 2: Select strategy
        strategy = self.select_strategy(
            analysis, parent, archive_inspirations, top_k_inspirations, meta_recommendations
        )
        if not strategy:
            logger.info("SGR strategy selection failed, will use fallback")
            return None, self._get_fallback_strategy()

        logger.info(f"SGR Strategy: {strategy.strategy_type} "
                   f"(confidence: {strategy.confidence:.2f})")

        # Step 3: Create complete plan
        plan = CodeMutationPlan(
            analysis=analysis,
            strategy=strategy,
            mutation_focus=strategy.target_areas,
            success_criteria=f"Improve {strategy.expected_improvement} while maintaining correctness"
        )

        return plan, None

    def _build_analysis_prompt(self, program: Program) -> str:
        """Build prompt for code analysis."""
        prompt = f"""# Code Analysis Request

Analyze the following {self.language} program and provide structured assessment:

```{self.language}
{program.code}
```

**Current Performance:**
{perf_str(program.combined_score, program.public_metrics)}

**Correctness:** {'Correct' if program.correct else 'Incorrect'}
"""

        # Add text feedback if available
        if self.use_text_feedback and program.text_feedback:
            text_feedback_section = format_text_feedback_section(program.text_feedback)
            prompt += f"\n{text_feedback_section}"

        prompt += """

Please analyze this code for:
1. Complexity level (low/medium/high)
2. Main algorithm description
3. Performance bottlenecks
4. Code quality issues
5. Optimization opportunities

Provide your analysis in the structured format."""

        return prompt

    def _build_strategy_prompt(
        self,
        analysis: CodeAnalysis,
        parent: Program,
        archive_inspirations: List[Program],
        top_k_inspirations: List[Program],
        meta_recommendations: Optional[str] = None,
    ) -> str:
        """Build prompt for strategy selection."""

        prompt = f"""# Mutation Strategy Selection

**Code Analysis Results:**
- Complexity: {analysis.complexity}
- Main Algorithm: {analysis.main_algorithm}
- Performance Bottlenecks: {', '.join(analysis.performance_bottlenecks) if analysis.performance_bottlenecks else 'None identified'}
- Quality Issues: {', '.join(analysis.code_quality_issues) if analysis.code_quality_issues else 'None identified'}
- Optimization Opportunities: {', '.join(analysis.optimization_opportunities) if analysis.optimization_opportunities else 'None identified'}

**Current Program Performance:**
{perf_str(parent.combined_score, parent.public_metrics)}
"""

        # Add inspiration programs context
        total_inspirations = len(archive_inspirations) + len(top_k_inspirations)
        if total_inspirations > 0:
            prompt += f"\n**Available Inspirations:** {total_inspirations} programs"

            if archive_inspirations:
                best_archive_score = max(p.combined_score for p in archive_inspirations)
                prompt += f"\n- Best archive score: {best_archive_score:.2f}"

            if top_k_inspirations:
                best_topk_score = max(p.combined_score for p in top_k_inspirations)
                prompt += f"\n- Best top-k score: {best_topk_score:.2f}"
        else:
            prompt += "\n**Available Inspirations:** None (consider diff or full strategies)"

        # Add meta recommendations
        if meta_recommendations:
            prompt += f"\n\n**Meta Recommendations:**\n{meta_recommendations}"

        prompt += """

Based on this analysis and context, select the optimal mutation strategy:

**Strategy Options:**
- `diff`: Targeted patches (safe, incremental improvements)
- `full`: Complete rewrite (high risk/reward, structural changes)
- `cross`: Combine inspirations (requires good examples)
- `focused`: Targeted function modifications (performance optimization)

Consider evolution stage, risk tolerance, and potential for improvement.
Provide structured strategy selection with detailed reasoning."""

        return prompt

    def _get_fallback_strategy(self) -> Optional[str]:
        """Get fallback strategy when SGR fails."""
        if not self.fallback_to_random:
            return None

        # Simple fallback logic
        import random
        strategies = ["diff", "full"]  # Conservative fallback options
        return random.choice(strategies)