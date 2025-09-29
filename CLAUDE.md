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

## Writing New Examples - Best Practices

### Essential Requirements
1. **Complete Typing Imports**: Always use `from typing import *` to avoid evolution errors with `Set`, `Dict`, etc.
2. **Pydantic Models**: Use Pydantic BaseModel for structured data validation and JSON serialization
3. **External Service Integration**: Implement caching for API calls (see TavilySearchService example)
4. **EVOLVE-BLOCK Placement**: Mark only core algorithm logic, not utility functions
5. **Evaluation Interface**: Implement proper ShinkaEvolve evaluation interface with metrics.json output

### Directory Structure Template

```
examples/your_example/
├── initial.py              # Algorithm with EVOLVE-BLOCK markers
├── evaluate.py             # Evaluation function with metrics output
├── README.md               # Full documentation
├── QUICKSTART.md           # Quick start guide (optional)
└── configs/
    └── task_config.yaml    # Legacy task config (optional, for reference)
```

Main configs in project root:
```
configs/
├── your_example.yaml              # Main launch config
└── task/
    └── your_example.yaml          # Task-specific config with system message
```

### Example Structure Template
```python
from typing import *  # CRITICAL: Prevents Set/Dict NameError during evolution
import json
from pydantic import BaseModel, Field
from shinka.utils.your_service import YourService  # External integrations

class YourDataModel(BaseModel):
    """Pydantic model for structured data validation."""
    field1: str = Field(description="Description")
    field2: List[int] = Field(default_factory=list)

def your_algorithm(input_data: str) -> YourDataModel:
    """Main algorithm with EVOLVE-BLOCK markers."""
    # EVOLVE-BLOCK-START
    # Core algorithm logic here
    result = YourDataModel(field1=input_data)
    # EVOLVE-BLOCK-END
    return result

def run_experiment(test_cases: List[str]) -> List[Dict[str, Any]]:
    """Required evaluation interface."""
    results = []
    for case in test_cases:
        strategy = your_algorithm(case)
        results.append({"case": case, "strategy": strategy})
    return results
```

### Performance Optimizations
- **File-based Caching**: Implement persistent caching like TavilySearchService for expensive operations
- **Pydantic JSON Serialization**: Use `model_dump()` and custom encoders for complex types
- **Timeout Handling**: Set reasonable timeouts for external API calls
- **Error Resilience**: Handle API failures gracefully without fallbacks during evolution

### Advanced Integration Example (SEO Research)
```python
# External service with file caching
service = TavilySearchService(cache_dir=".your_cache")
cached_results = service.search(query)  # Automatic file caching

# Pydantic model with validation
strategy = AdvancedStrategy(niche=niche_topic)
competitor_analysis = content_extractor.analyze_competitor(domain, niche, keywords)
strategy.competitor_analyses.append(competitor_analysis)

# JSON serialization for evaluation
return strategy  # Returns Pydantic model, not dict
```

### File-based Caching Implementation

For external API integrations, implement persistent file caching to dramatically speed up evolution:

```python
import hashlib
import json
from pathlib import Path

class YourServiceWithCache:
    def __init__(self, cache_dir: str = ".your_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self._memory_cache = {}

    def _get_cache_key(self, query: str, **params) -> str:
        cache_string = f"{query}_{params}"
        return hashlib.md5(cache_string.encode('utf-8')).hexdigest()

    def _load_from_cache(self, cache_key: str):
        cache_path = self.cache_dir / f"{cache_key}.json"
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None

    def _save_to_cache(self, cache_key: str, data):
        cache_path = self.cache_dir / f"{cache_key}.json"
        with open(cache_path, 'w') as f:
            json.dump(data, f, indent=2)

    def api_call(self, query: str, **params):
        cache_key = self._get_cache_key(query, **params)

        # Check memory cache first
        if cache_key in self._memory_cache:
            return self._memory_cache[cache_key]

        # Check file cache
        cached_data = self._load_from_cache(cache_key)
        if cached_data:
            self._memory_cache[cache_key] = cached_data
            return cached_data

        # Make actual API call
        result = self._actual_api_call(query, **params)

        # Cache results
        self._memory_cache[cache_key] = result
        self._save_to_cache(cache_key, result)
        return result
```

**Benefits**: 27,000x+ speed improvement for repeated queries, consistent results across evolution generations.

### Common Pitfalls to Avoid
1. **Missing Typing**: Don't use `Set[str]` without importing from typing - causes evolution errors
2. **No Caching**: Expensive API calls will slow evolution - implement file caching
3. **Dict Returns**: Return Pydantic models, not dicts, for better type safety
4. **Large EVOLVE-BLOCKs**: Keep evolution blocks focused on core algorithm logic only
5. **No Error Handling**: External services must handle failures gracefully
6. **Cache Directory**: Add your cache directory to `.gitignore` to avoid committing cached data

### Real-World Results

The SEO research example demonstrates these best practices in action:

**Before optimizations:**
- Score: 0.0 (competitor analysis completely failed)
- Multiple timeout errors and API failures
- No persistent caching between evolution runs

**After implementing best practices:**
- Score: 0.685 (significant improvement)
- Real competitor discovery: Canva, Shutterstock, Etsy, etc.
- 27,000x faster repeated searches via file caching
- Robust error handling without evolution failures

**Key improvements:**
- Fixed typing imports prevented `Set`/`Dict` NameErrors during LLM mutations
- File-based Tavily caching dramatically reduced API calls
- Pydantic models ensured type safety and proper JSON serialization
- Focused EVOLVE-BLOCKs allowed LLM to optimize core algorithm logic




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
