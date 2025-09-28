#!/usr/bin/env python3
"""
SGR-Enhanced Evolution Runner for Fibonacci Optimization.

This example demonstrates the full ShinkaEvolve framework with SGR integration
for intelligent mutation strategy selection.
"""

from shinka.core import EvolutionRunner, EvolutionConfig
from shinka.core.sgr_prompt_sampler import SGRPromptSampler
from shinka.database import DatabaseConfig
from shinka.launch import LocalJobConfig
from shinka.llm import LLMClient


def create_sgr_evolution_config():
    """Create evolution configuration with SGR integration."""

    # Task-specific system message for Fibonacci optimization
    fibonacci_task_msg = """You are an expert Python programmer specializing in algorithm optimization, particularly for mathematical sequences like Fibonacci.

Your goal is to optimize Fibonacci implementations for both correctness and performance. Consider these approaches:

1. **Iterative Implementation**: Replace recursion with loops for better performance
2. **Memoization**: Cache results to avoid redundant calculations
3. **Dynamic Programming**: Build solutions bottom-up
4. **Mathematical Optimizations**: Use closed-form formulas or matrix exponentiation for very large numbers
5. **Input Validation**: Handle edge cases properly
6. **Code Quality**: Add proper documentation and error handling

The current implementation is a naive recursive approach that becomes exponentially slow. Focus on:
- Maintaining correctness for all test cases
- Dramatically improving performance (sub-millisecond for n=30)
- Writing clean, readable, well-documented code

Be creative but ensure all optimizations maintain mathematical correctness."""

    # Create LLM client with proper Azure configuration
    llm_client = LLMClient(
        model_names=["gpt-5-mini"],  # Use Azure model
        verbose=True,
    )

    # SGR PromptSampler replaces the standard sampler
    sgr_sampler = SGRPromptSampler(
        sgr_enabled=True,
        sgr_confidence_threshold=0.7,  # Moderate confidence threshold
        sgr_fallback_to_random=True,
        sgr_llm_client=llm_client,
        task_sys_msg=fibonacci_task_msg,
        language="python",
        patch_types=["diff", "full", "cross"],
        patch_type_probs=[0.5, 0.4, 0.1],  # Favor diff and full over cross
        use_text_feedback=True,
    )

    return EvolutionConfig(
        task_sys_msg=fibonacci_task_msg,
        patch_types=["diff", "full", "cross"],
        patch_type_probs=[0.5, 0.4, 0.1],
        num_generations=15,  # Smaller number for demo
        max_parallel_jobs=3,
        max_patch_resamples=2,
        max_patch_attempts=3,
        job_type="local",
        language="python",
        llm_models=["gpt-5-mini"],  # Azure model
        llm_kwargs=dict(
            temperatures=[0.2, 0.7],  # Lower temperature for more focused mutations
            max_tokens=8192,
        ),
        meta_rec_interval=5,  # Generate meta-recommendations every 5 programs
        meta_llm_models=["gpt-5-mini"],
        meta_llm_kwargs=dict(temperatures=[0.0], max_tokens=4096),
        embedding_model="text-embedding-3-small",
        code_embed_sim_threshold=0.99,  # High threshold for novelty
        novelty_llm_models=["gpt-5-mini"],
        novelty_llm_kwargs=dict(temperatures=[0.0], max_tokens=4096),
        init_program_path="initial.py",
        results_dir="results/sgr_fibonacci_evolution",  # Save to results directory
        use_text_feedback=True,
    ), sgr_sampler


def create_database_config():
    """Create database configuration optimized for SGR evolution."""
    return DatabaseConfig(
        db_path="fibonacci_evolution.sqlite",
        num_islands=2,  # Use island evolution for diversity
        archive_size=20,  # Moderate archive size
        # Inspiration parameters
        elite_selection_ratio=0.4,  # Favor elite programs
        num_archive_inspirations=3,
        num_top_k_inspirations=2,
        # Parent selection for optimization problems
        parent_selection_strategy="weighted",
        parent_selection_lambda=5.0,  # Strong bias toward better solutions
        # Island migration
        migration_interval=8,
        migration_rate=0.2,
        island_elitism=True,
    )


def main():
    """Run SGR-enhanced evolution for Fibonacci optimization."""
    print("=" * 70)
    print("🧠 SGR-Enhanced ShinkaEvolve: Fibonacci Optimization")
    print("=" * 70)

    # Create configurations
    evo_config, sgr_sampler = create_sgr_evolution_config()
    db_config = create_database_config()
    job_config = LocalJobConfig(eval_program_path="evaluate.py")

    print(f"📁 Results will be saved to: {evo_config.results_dir}")
    print(f"🧠 SGR enabled with confidence threshold: {sgr_sampler.sgr_confidence_threshold}")
    print(f"🔄 Running {evo_config.num_generations} generations with {evo_config.max_parallel_jobs} parallel jobs")
    print()

    # Create custom EvolutionRunner with SGR integration
    class SGREvolutionRunner(EvolutionRunner):
        """Enhanced EvolutionRunner with SGR integration."""

        def __init__(self, evo_config, job_config, db_config, sgr_sampler, verbose=True):
            super().__init__(evo_config, job_config, db_config, verbose)
            # Replace the prompt sampler with SGR version
            self.prompt_sampler = sgr_sampler

        def run(self):
            """Run evolution with SGR tracking."""
            print("🚀 Starting SGR-enhanced evolution...")
            super().run()

            # Print SGR statistics at the end
            print("\n" + "=" * 70)
            print("🧠 SGR Statistics Summary:")
            print("=" * 70)

            stats = self.prompt_sampler.get_sgr_statistics()
            for key, value in stats.items():
                if isinstance(value, float):
                    if 'rate' in key:
                        print(f"   {key}: {value:.1%}")
                    else:
                        print(f"   {key}: {value:.3f}")
                else:
                    print(f"   {key}: {value}")

            if stats.get('total_attempts', 0) > 0:
                print(f"\n💡 SGR successfully guided {stats.get('sgr_successes', 0)} out of {stats.get('total_attempts', 0)} mutation decisions!")

    # Create and run SGR evolution
    sgr_runner = SGREvolutionRunner(
        evo_config=evo_config,
        job_config=job_config,
        db_config=db_config,
        sgr_sampler=sgr_sampler,
        verbose=True,
    )

    sgr_runner.run()

    print("\n🎉 SGR-enhanced evolution completed!")
    print(f"📊 Check results in: {evo_config.results_dir}")


if __name__ == "__main__":
    main()