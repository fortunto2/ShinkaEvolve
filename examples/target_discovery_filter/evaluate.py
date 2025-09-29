"""
Evaluation script for Target Discovery PDB Filtering.

This script uses real bioservices data from UniProt and PDB for diabetes targets.
"""

from typing import List, Dict, Any
from bioservices import UniProt, PDB
from examples.target_discovery_filter.initial import run_experiment


def fetch_real_diabetes_targets() -> List[Dict[str, Any]]:
    """
    Fetch real protein targets for diabetes from UniProt and PDB.

    Focus on known diabetes-related proteins like:
    - Insulin receptor (INSR)
    - Glucokinase (GCK)
    - PPAR-gamma (PPARG)
    - DPP-4 (DPP4)
    - SGLT2 (SLC5A2)
    """
    print("Fetching real diabetes targets from UniProt/PDB...")

    uniprot = UniProt(verbose=False)
    pdb_service = PDB(verbose=False)

    # Known diabetes-related UniProt IDs
    diabetes_proteins = {
        "P06213": "INSR - Insulin receptor",
        "P35557": "GCK - Glucokinase",
        "P37231": "PPARG - Peroxisome proliferator-activated receptor gamma",
        "P27487": "DPP4 - Dipeptidyl peptidase 4",
        "P31639": "SLC5A2 - Sodium/glucose cotransporter 2"
    }

    candidates = []

    for uniprot_id, protein_name in diabetes_proteins.items():
        try:
            print(f"  Fetching {protein_name} ({uniprot_id})...")

            # Use mapping API to get PDB structures
            mapping_result = uniprot.mapping(fr='UniProtKB_AC-ID', to='PDB', query=uniprot_id)

            # Extract PDB IDs from mapping results
            pdb_list = []
            if mapping_result and isinstance(mapping_result, dict) and 'results' in mapping_result:
                for result in mapping_result['results']:
                    if 'to' in result:
                        pdb_list.append(result['to'])

            print(f"    Found {len(pdb_list)} PDB structures")

            # Limit to first 20 structures per protein
            for pdb_id in pdb_list[:20]:
                if not pdb_id or len(pdb_id) != 4:
                    continue

                try:
                    # Create candidate with real PDB ID
                    description = f"Structure of {protein_name}"
                    abstract = f"Diabetes therapeutic target: {protein_name}. Crystal structure determination for drug design."
                    ligand = f"ligand-{pdb_id}"

                    candidates.append({
                        "pdb_id": pdb_id.upper(),
                        "description": description,
                        "abstract": abstract,
                        "ligand_name": ligand,
                        "uniprot_id": uniprot_id,
                        "relevance_score": 0.0
                    })

                except Exception as e:
                    print(f"    Warning: Could not process PDB {pdb_id}: {e}")
                    continue

        except Exception as e:
            print(f"    Warning: Could not fetch {uniprot_id}: {e}")
            continue

    print(f"\n  Total candidates fetched: {len(candidates)}")
    return candidates


def run_shinka_eval(program_path: str = None, results_dir: str = None):
    """
    Main evaluation function called by ShinkaEvolve.

    Args:
        program_path: Path to the program to evaluate
        results_dir: Directory to save metrics.json

    Returns:
        None (writes metrics to results_dir/metrics.json)
    """
    import json
    import os

    print("\n" + "="*60)
    print("Target Discovery Filter - Diabetes Example")
    print("="*60 + "\n")

    # Fetch real data from UniProt/PDB
    candidates = fetch_real_diabetes_targets()

    if len(candidates) < 10:
        raise RuntimeError(f"Not enough candidates fetched: {len(candidates)}. Need at least 10.")

    # Create test case
    test_cases = [{
        "disease": "Diabetes",
        "candidates": candidates
    }]

    # Run the filtering algorithm
    results = run_experiment(test_cases)

    # Calculate fitness metrics
    total_score = 0.0

    for result in results:
        # Metrics:
        # 1. Diversity score (higher is better)
        diversity_score = result["diversity_score"]

        # 2. Selection efficiency (selected reasonable number)
        num_selected = result["num_selected"]
        selection_score = min(num_selected / 10.0, 1.0)  # Target: 10 structures

        # 3. Quality check (at least some structures selected)
        quality_score = 1.0 if num_selected > 0 else 0.0

        # Combined score
        case_score = (diversity_score * 0.4 + selection_score * 0.3 + quality_score * 0.3)
        total_score += case_score

        # Log details
        print(f"\n{'='*60}")
        print(f"Disease: {result['disease']}")
        print(f"{'='*60}")
        print(f"Selected Structures: {num_selected}")
        print(f"Diversity Score: {diversity_score:.3f}")
        print(f"Selection Score: {selection_score:.3f}")
        print(f"Quality Score: {quality_score:.3f}")
        print(f"\nTop PDB IDs: {result['selected_pdb_ids'][:5]}")
        print(f"\n{result['rationale']}")
        print(f"\nCase Score: {case_score:.3f}")

    # Average fitness
    fitness = total_score

    print(f"\n{'='*60}")
    print(f"OVERALL FITNESS: {fitness:.3f}")
    print(f"{'='*60}\n")

    # Save metrics to JSON file (required by ShinkaEvolve)
    if results_dir:
        metrics_file = os.path.join(results_dir, "metrics.json")
        metrics = {
            "fitness": fitness,
            "diversity_score": diversity_score,
            "selection_score": selection_score,
            "quality_score": quality_score,
            "num_selected": num_selected,
            "num_candidates": len(candidates),
        }

        # Write correct.json for compatibility
        correct_file = os.path.join(results_dir, "correct.json")
        correct = fitness > 0.0  # Consider it correct if fitness > 0

        with open(metrics_file, "w") as f:
            json.dump(metrics, f, indent=4)
        print(f"✓ Metrics saved to {metrics_file}")

        with open(correct_file, "w") as f:
            json.dump({"correct": correct, "error": None}, f, indent=4)
        print(f"✓ Correct status saved to {correct_file}\n")

    return fitness


if __name__ == "__main__":
    fitness = run_shinka_eval()
    print(f"\n✓ Evaluation complete. Final Fitness: {fitness:.3f}")