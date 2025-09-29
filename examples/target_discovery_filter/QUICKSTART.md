# Target Discovery Filter - Quick Start Guide

## 1-Minute Setup

```bash

# Test the algorithm
uv run python examples/target_discovery_filter/evaluate.py
```

**Expected Output**: Fitness ~0.740 with 8 real PDB structures selected

## 5-Minute Evolution Run (Quick Test)

```bash
# Run 3 generations of evolution
uv run shinka_launch --config-name target_discovery_filter
```

**What happens**:
- Fetches 88 real PDB structures from UniProt for 5 diabetes proteins
- Evolves the filtering algorithm over 3 generations
- Uses `gpt-5-mini` for fast, cheap mutations
- Results saved to `results/target_discovery_filter/YYYYMMDDHHMMSS/`

## 1-Hour Evolution Run (Small Budget)

```bash
# Run 20 generations for better results
uv run shinka_launch --config-name target_discovery_filter evolution=small_budget
```

**Goal**: Improve fitness from 0.740 → 0.850+

## What Gets Evolved

The algorithm has **one EVOLVE-BLOCK** (lines 54-100 in `initial.py`):

```python
# EVOLVE-BLOCK-START
# Stage 1: Group Filtering (process in groups of 100)
# Stage 2: Reverse Order Consistency (reduce bias)
# Stage 3: UniProt Diversity Filtering (max 3 per protein)
# EVOLVE-BLOCK-END
```

## Key Metrics

| Metric | Weight | Baseline | Target |
|--------|--------|----------|--------|
| Diversity Score | 40% | 0.500 | 0.600+ |
| Selection Score | 30% | 0.800 | 1.000 |
| Quality Score | 30% | 1.000 | 1.000 |
| **Overall Fitness** | - | **0.740** | **0.850+** |

## Real Data

### Diabetes Proteins (from UniProt)
1. **P06213** - INSR (Insulin receptor) → 72 PDB structures
2. **P35557** - GCK (Glucokinase) → 35 PDB structures
3. **P37231** - PPARG (PPAR gamma) → 316 PDB structures
4. **P27487** - DPP4 (DPP-4) → 107 PDB structures
5. **P31639** - SLC5A2 (SGLT2) → 8 PDB structures

**Total**: ~88 structures fetched via bioservices

### Example Selected Structures
```
2ATH - PPARG (peroxisome proliferator-activated receptor)
2BUB - DPP4 (dipeptidyl peptidase 4)
1W1I - DPP4 (dipeptidyl peptidase 4)
3A0I - GCK (glucokinase)
3FR0 - PPARG (peroxisome proliferator-activated receptor)
```

## Configuration Files

### Main
- `configs/target_discovery_filter.yaml` - Top-level config
- `configs/task/target_discovery_filter.yaml` - Task-specific settings

### Presets
- `evolution=quick_test` - 3 generations (~10 min)
- `evolution=small_budget` - 20 generations (~60 min)
- `database=island_small` - Faster evolution (default)
- `database=island_large` - More thorough search

## Viewing Results

```bash
# Navigate to results directory
cd results/target_discovery_filter/<timestamp>

# Check fitness evolution
cat fitness_log.txt

# View best program
cat best_program.py
```

## Evolution Objectives

The LLM will try to improve:
1. **Relevance Scoring** - Better diabetes keyword matching
2. **Group Strategy** - Optimal group size and selection
3. **Consistency Logic** - Enhanced forward/reverse intersection
4. **Diversity Balance** - More proteins represented
5. **Therapeutic Focus** - Prioritize clinically-relevant structures

## Troubleshooting

### Issue: Config not found
```bash
# Make sure you're in the right directory
cd /Users/rustam/projects/ShinkaEvolve
```

### Issue: bioservices timeout
```bash
# The first run fetches data from UniProt - can take 30-60 seconds
# Subsequent evaluations reuse the cache
```

### Issue: No structures selected
```bash
# Check if bioservices is working
uv run python examples/target_discovery_filter/evaluate.py
```

## Next Steps

1. **Review Results**: Check `results/` directory after evolution
2. **Compare Fitness**: Look at fitness progression across generations
3. **Analyze Changes**: Read the evolved algorithm in `best_program.py`
4. **Iterate**: Run with `small_budget` or `medium_budget` for better results

## Based on Research

**Paper**: PharmAgents - Building a Virtual Pharma with LLM Agents
**Algorithm**: Algorithm 1 (PDB Filtering for Target Discovery)
**Source**: arXiv:2503.22164v1 [q-bio.BM] (2025)