# Target Discovery Filter Example

## Overview

This example implements the **PDB Filtering algorithm (Algorithm 1)** from the PharmAgents paper for target discovery in drug development. The algorithm filters protein structures from the PDB database to identify the most promising therapeutic targets for **Diabetes** using **real data from UniProt and PDB databases via bioservices**.

## Based on PharmAgents Research

**Paper**: "PharmAgents: Building a Virtual Pharma with Large Language Model Agents" (2025)
**Algorithm**: Algorithm 1 - PDB Filtering for Target Discovery
**Source**: arXiv:2503.22164v1 [q-bio.BM]

### Key Innovation

The algorithm uses a three-stage filtering approach:

1. **Group Filtering**: Process candidates in groups of 100, selecting top 10 from each group
2. **Reverse Order Consistency**: Reduce sequence bias by processing in both forward and reverse order
3. **UniProt Filtering**: Ensure diversity by limiting max 3 PDBs per UniProt ID

## Real Data Integration

This example uses **bioservices** to fetch real diabetes therapeutic targets:

### Diabetes Proteins (from UniProt)
- **P06213**: INSR - Insulin receptor (72 PDB structures)
- **P35557**: GCK - Glucokinase (35 PDB structures)
- **P37231**: PPARG - PPAR gamma (316 PDB structures)
- **P27487**: DPP4 - Dipeptidyl peptidase 4 (107 PDB structures)
- **P31639**: SLC5A2 - SGLT2 (8 PDB structures)

**Total**: ~88 real PDB structures fetched dynamically

## Files

- **`initial.py`**: Core algorithm implementation with Pydantic models
  - `PDBCandidate`: Protein structure data model
  - `FilteredTarget`: Filtering results with rationale
  - `target_discovery_filter()`: Main filtering algorithm (EVOLVE-BLOCK)

- **`evaluate.py`**: Fitness evaluation using real bioservices data
  - `fetch_real_diabetes_targets()`: Fetches real PDB structures from UniProt
  - `run_shinka_eval()`: ShinkaEvolve evaluation interface

- **`configs/task_config.yaml`**: Hydra configuration for evolution

## Pydantic Models

### PDBCandidate
```python
class PDBCandidate(BaseModel):
    pdb_id: str              # Real PDB identifier (e.g., "2ATH", "3FR0")
    description: str          # Structure description
    abstract: str            # Research context
    ligand_name: str         # Co-crystal ligand
    uniprot_id: str          # UniProt protein identifier
    relevance_score: float   # Diabetes relevance score
```

### FilteredTarget
```python
class FilteredTarget(BaseModel):
    selected_pdbs: List[PDBCandidate]
    filtering_rationale: str
    diversity_score: float
```

## Running the Example

### Quick Test (3 generations)
```bash
cd /Users/rustam/projects/ShinkaEvolve
uv run shinka_launch --config-name target_discovery_filter
```

### Small Budget (20 generations)
```bash
uv run shinka_launch --config-name target_discovery_filter evolution=small_budget
```

### Custom Configuration
```bash
uv run shinka_launch \
  --config-name target_discovery_filter \
  evolution=small_budget \
  database=island_large \
  evo_config.num_generations=30
```

### Test Evaluation Only
```bash
cd examples/target_discovery_filter
uv run python evaluate.py
```

## Current Performance

**Baseline Fitness: 0.740** (with real PDB data)

### Metrics Breakdown
- **Diversity Score**: 0.500 (4/5 proteins represented)
- **Selection Score**: 0.800 (8 structures selected)
- **Quality Score**: 1.000 (all valid structures)

### Selected Real PDB Structures
```
1. 2ATH - PPARG structure
2. 2BUB - DPP4 structure
3. 1W1I - DPP4 structure
4. 3A0I - GCK structure
5. 3FR0 - PPARG structure
```

**Target Fitness**: 0.850+ (improved relevance and diversity)

## Fitness Calculation

```python
fitness = (
    diversity_score * 0.4 +      # UniProt coverage
    selection_score * 0.3 +       # Optimal count (~10)
    quality_score * 0.3           # Valid structures
)
```

## Evolution Objectives

The algorithm can be evolved to improve:

1. **Relevance Scoring**: Better keyword matching and therapeutic indicators
2. **Group Size**: Optimal grouping for filtering efficiency
3. **Consistency Logic**: Enhanced forward/reverse intersection strategy
4. **Diversity Balance**: Better trade-off between relevance and protein diversity
5. **Therapeutic Focus**: Prioritize clinically-relevant structures

## EVOLVE-BLOCK

The core algorithm (lines 54-100 in `initial.py`) is marked for evolution:

```python
# EVOLVE-BLOCK-START
# Stage 1: Group Filtering
# Stage 2: Reverse Order Consistency
# Stage 3: UniProt Filtering
# EVOLVE-BLOCK-END
```

## Dependencies

```bash
uv add bioservices pandas
```

**bioservices**: Accesses UniProt and PDB APIs for real protein data
**pandas**: Data manipulation and analysis (if needed)

## Example Output

```
============================================================
Target Discovery Filter - Diabetes Example
============================================================

Fetching real diabetes targets from UniProt/PDB...
  Fetching INSR - Insulin receptor (P06213)...
    Found 72 PDB structures
  Fetching GCK - Glucokinase (P35557)...
    Found 35 PDB structures
  ...

Total candidates fetched: 88

============================================================
Disease: Diabetes
============================================================
Selected Structures: 8
Diversity Score: 0.500
Selection Score: 0.800
Quality Score: 1.000

Top PDB IDs: ['2ATH', '2BUB', '1W1I', '3A0I', '3FR0']

OVERALL FITNESS: 0.740
============================================================
```

## Best Practices Demonstrated

✅ **Complete Typing**: Uses `from typing import *` to avoid evolution errors
✅ **Pydantic Models**: Structured data validation and type safety
✅ **Real External Data**: Integration with bioservices for UniProt/PDB
✅ **EVOLVE-BLOCK Placement**: Core algorithm marked for targeted evolution
✅ **Clear Documentation**: Comprehensive docstrings and comments
✅ **Evaluation Interface**: Standard `run_experiment()` function

## Configuration Files

### Main Config
- **Location**: `/configs/target_discovery_filter.yaml`
- **Task Config**: `/configs/task/target_discovery_filter.yaml`

### Quick Test (3 generations)
- Uses: `/configs/evolution/quick_test.yaml`
- Model: `gpt-5-mini`
- Time: ~5-10 minutes
- Best for: Initial testing and validation

### Small Budget (20 generations)
- Uses: `/configs/evolution/small_budget.yaml`
- Model: `gpt-5-mini`
- Time: ~30-60 minutes
- Best for: Full evolution run with real improvements

## Real-World Application

In production PharmAgents system, this algorithm would:

1. Query live PDB/UniProt databases for latest structures
2. Use LLM reasoning for sophisticated relevance assessment
3. Integrate with downstream lead identification modules
4. Maintain explainable decision trails for regulatory compliance
5. Support iterative refinement based on experimental validation

## References

- **PharmAgents Paper**: arXiv:2503.22164v1 [q-bio.BM] (2025)
- **PDB Database**: https://www.rcsb.org/
- **UniProt Database**: https://www.uniprot.org/
- **Bioservices**: https://bioservices.readthedocs.io/