# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ShinkaEvolve is an open-source framework that combines Large Language Models (LLMs) with evolutionary algorithms for automated scientific code evolution. The system achieves unprecedented sample efficiency by using LLMs as intelligent mutation operators to evolve programs across generations, maintaining archives of successful solutions and supporting parallel evaluation locally or on Slurm clusters.

**Key Innovations:**
- **Adaptive parent sampling** that balances exploration and exploitation
- **Code novelty rejection-sampling** for efficient search space exploration
- **Bandit-based LLM ensemble selection** strategy that adapts to evolving program states
- **Sample efficiency**: Discovers state-of-the-art solutions with orders of magnitude fewer evaluations than existing approaches (e.g., 150 evaluations vs thousands)

## Core Architecture

### Main Components
- **`shinka/core/`**: Evolution engine with runner, sampler, and evaluation wrapper
- **`shinka/database/`**: Program archives, island populations, and selection strategies
- **`shinka/llm/`**: LLM clients supporting OpenAI, Azure OpenAI, Anthropic, Google, and DeepSeek models
- **`shinka/edit/`**: Code mutation via diff patches, full replacements, and crossover
- **`shinka/launch/`**: Job execution on local machines and Slurm clusters
- **`shinka/prompts/`**: Specialized prompts for different mutation types and meta-recommendations
- **`shinka/webui/`**: Real-time visualization of evolution progress

### Key Patterns
- **Island-based evolution**: Multiple populations evolve in parallel with periodic migration
- **EVOLVE-BLOCK markers**: Code sections marked with `# EVOLVE-BLOCK-START/END` for targeted evolution
- **Evaluation integration**: Programs must implement `run_experiment()` function for fitness evaluation
- **Hydra configuration**: All experiments configured via YAML files with override support

## Development Commands

### Environment Setup
```bash
# Create and activate environment
uv venv --python 3.11
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Testing and Quality
```bash
# Run tests
pytest

# Code formatting and linting
black .
isort .
flake8 .
```

### Running Experiments
```bash
# Launch with pre-configured variant
shinka_launch variant=circle_packing_example

# Launch with custom parameters
shinka_launch task=circle_packing database=island_large evolution=medium_budget

# Start WebUI for monitoring
shinka_visualize --port 8888 --open
```

## Configuration System

Uses Hydra for hierarchical configuration management:
- **`configs/task/`**: Problem-specific settings (evaluation scripts, initial programs)
- **`configs/database/`**: Archive sizes, island populations, selection strategies
- **`configs/evolution/`**: Generation counts, LLM models, mutation parameters
- **`configs/cluster/`**: Execution environments (local, Slurm Docker/Conda)
- **`configs/variant/`**: Pre-configured experiment combinations

### Azure OpenAI Setup
The system automatically detects Azure OpenAI when environment variables are present in `.env`:
```bash
AZURE_OPENAI_API_KEY="your-api-key"
AZURE_API_VERSION="2025-04-01-preview"
AZURE_API_ENDPOINT="https://your-resource.openai.azure.com"
```
When detected, standard OpenAI model names (e.g., `gpt-4o-mini`, `text-embedding-3-small`) automatically use Azure OpenAI instead of regular OpenAI.

## Working with Evolution

### Required Files for New Tasks
1. **Evaluation script** (`evaluate.py`): Defines fitness function via `run_shinka_eval()`
2. **Initial program** (`initial.py`): Starting solution with `# EVOLVE-BLOCK` markers
3. **Task config**: YAML file specifying evaluation and initialization paths

### Evolution Flow
1. `EvolutionRunner` loads initial program and creates database
2. Programs evaluated via `LocalJobConfig` or `SlurmJobConfig`
3. LLM models generate mutations (diff, full replacement, crossover)
4. Successful mutations added to island archives
5. Selection strategies choose parents for next generation
6. Process repeats for specified number of generations

### Key Classes
- `EvolutionConfig`: Controls mutation types, LLM models, generation count
- `DatabaseConfig`: Manages island populations and selection strategies
- `JobConfig`: Handles program execution (local vs cluster)
- `EvolutionRunner`: Main orchestration class

## Examples Structure

Each example in `examples/` contains:
- Task-specific evaluation logic
- Initial program with evolution blocks
- Configuration files for quick experimentation
- Problem-specific utilities and validators




## USE SUB-AGENTS FOR CONTEXT OPTIMIZATION

### 1. Always use the file-analyzer sub-agent when asked to read files.
The file-analyzer agent is an expert in extracting and summarizing critical information from files, particularly log files and verbose outputs. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 2. Always use the code-analyzer sub-agent when asked to search code, analyze code, research bugs, or trace logic flow.

The code-analyzer agent is an expert in code analysis, logic tracing, and vulnerability detection. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 3. Always use the test-runner sub-agent to run tests and analyze the test results.

Using the test-runner agent ensures:

- Full test output is captured for debugging
- Main conversation stays clean and focused
- Context usage is optimized
- All issues are properly surfaced
- No approval dialogs interrupt the workflow
