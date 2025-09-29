"""
Target Discovery PDB Filtering Algorithm

This example implements the PDB filtering algorithm from PharmAgents paper (Algorithm 1).
The algorithm filters protein structures (PDB IDs) to select the best therapeutic targets
for a given disease using a multi-stage filtering approach with:
- Group Filtering: Process candidates in groups of 100
- Reverse Order Consistency: Reduce sequence bias
- UniProt Filtering: Ensure diversity across targets

Uses real bioservices data from UniProt and PDB databases.
"""

from typing import *
from pydantic import BaseModel, Field
import hashlib
import pandas as pd
from bioservices import UniProt, PDB


class PDBCandidate(BaseModel):
    """Represents a protein structure candidate from PDB database."""
    pdb_id: str = Field(description="PDB identifier")
    description: str = Field(description="Brief description of the structure")
    abstract: str = Field(description="Abstract from relevant papers")
    ligand_name: str = Field(description="Co-crystal ligand name")
    uniprot_id: str = Field(description="UniProt protein identifier")
    relevance_score: float = Field(default=0.0, description="Relevance score for the disease")


class FilteredTarget(BaseModel):
    """Result of target filtering process."""
    selected_pdbs: List[PDBCandidate] = Field(default_factory=list)
    filtering_rationale: str = Field(description="Explanation of selection process")
    diversity_score: float = Field(description="Measure of target diversity")


def target_discovery_filter(pdb_candidates: List[PDBCandidate], disease: str) -> FilteredTarget:
    """
    Main PDB filtering algorithm based on PharmAgents Algorithm 1.

    Implements three-stage filtering:
    1. Group Filtering: Select top 10 from each group of 100
    2. Reverse Order Consistency: Reduce sequence bias
    3. UniProt Filtering: Max 3 PDBs per UniProt ID

    Args:
        pdb_candidates: List of PDB structure candidates
        disease: Disease name for target identification

    Returns:
        FilteredTarget with selected PDBs and rationale
    """
    # EVOLVE-BLOCK-START

    # Stage 1: Group Filtering
    all_top10_groups = []
    group_size = 100

    for i in range(0, len(pdb_candidates), group_size):
        group = pdb_candidates[i:i + group_size]

        # Forward selection
        top10_forward = select_top_k_by_relevance(group, disease, k=10)

        # Reverse selection for consistency
        reversed_group = list(reversed(group))
        top10_reversed = select_top_k_by_relevance(reversed_group, disease, k=10)

        # Intersection for consistency
        intersection = find_intersection(top10_forward, top10_reversed)

        if not intersection:
            # No intersection - take first from each
            intersection = [top10_forward[0], top10_reversed[0]]

        all_top10_groups.extend(intersection)

    # Stage 2: Reverse Order Consistency on combined results
    combined = all_top10_groups
    reversed_combined = list(reversed(combined))

    final_top10_forward = select_top_k_by_relevance(combined, disease, k=10)
    final_top10_reversed = select_top_k_by_relevance(reversed_combined, disease, k=10)

    final_intersection = find_intersection(final_top10_forward, final_top10_reversed)

    if not final_intersection:
        final_intersection = [final_top10_forward[0], final_top10_reversed[0]]

    # Stage 3: UniProt Filtering - max 3 PDBs per UniProt ID
    filtered_results = uniprot_diversity_filter(final_intersection, max_per_uniprot=3)

    # Calculate diversity score
    unique_uniprots = len(set(pdb.uniprot_id for pdb in filtered_results))
    diversity_score = unique_uniprots / len(filtered_results) if filtered_results else 0.0

    rationale = generate_filtering_rationale(filtered_results, disease, diversity_score)

    # EVOLVE-BLOCK-END

    return FilteredTarget(
        selected_pdbs=filtered_results,
        filtering_rationale=rationale,
        diversity_score=diversity_score
    )


def select_top_k_by_relevance(candidates: List[PDBCandidate], disease: str, k: int) -> List[PDBCandidate]:
    """
    Select top K candidates based on relevance to disease.

    This function would ideally use an LLM to evaluate relevance,
    but for the basic implementation uses heuristic scoring.
    """
    scored_candidates = []

    for candidate in candidates:
        # Simple heuristic: score based on text similarity
        score = calculate_relevance_score(candidate, disease)
        candidate.relevance_score = score
        scored_candidates.append(candidate)

    # Sort by score descending and take top k
    scored_candidates.sort(key=lambda x: x.relevance_score, reverse=True)
    return scored_candidates[:k]


def calculate_relevance_score(candidate: PDBCandidate, disease: str) -> float:
    """
    Calculate relevance score based on text matching.

    In PharmAgents, this would be done by LLM reasoning.
    Here we use simple keyword matching as baseline.
    """
    disease_lower = disease.lower()
    text = f"{candidate.description} {candidate.abstract} {candidate.ligand_name}".lower()

    # Count disease keyword occurrences
    keyword_matches = text.count(disease_lower)

    # Bonus for specific therapeutic indicators
    therapeutic_keywords = ["inhibitor", "agonist", "antagonist", "therapeutic", "drug", "treatment"]
    therapeutic_score = sum(1 for kw in therapeutic_keywords if kw in text)

    # Combine scores
    base_score = keyword_matches * 0.6 + therapeutic_score * 0.4

    # Add hash-based pseudo-randomness for tie-breaking
    hash_val = int(hashlib.md5(candidate.pdb_id.encode()).hexdigest(), 16)
    noise = (hash_val % 100) / 1000.0  # 0.000 to 0.099

    return base_score + noise


def find_intersection(list1: List[PDBCandidate], list2: List[PDBCandidate]) -> List[PDBCandidate]:
    """Find intersection of two PDB candidate lists by PDB ID."""
    ids1 = {pdb.pdb_id for pdb in list1}
    return [pdb for pdb in list2 if pdb.pdb_id in ids1]


def uniprot_diversity_filter(candidates: List[PDBCandidate], max_per_uniprot: int = 3) -> List[PDBCandidate]:
    """
    Ensure no more than max_per_uniprot PDBs selected per UniProt ID.
    This promotes diversity across different protein targets.
    """
    uniprot_counts: Dict[str, int] = {}
    filtered = []

    for candidate in candidates:
        uniprot_id = candidate.uniprot_id
        count = uniprot_counts.get(uniprot_id, 0)

        if count < max_per_uniprot:
            filtered.append(candidate)
            uniprot_counts[uniprot_id] = count + 1

    return filtered


def generate_filtering_rationale(selected: List[PDBCandidate], disease: str, diversity: float) -> str:
    """Generate human-readable rationale for the filtering decisions."""
    if not selected:
        return f"No suitable PDB structures found for {disease}"

    uniprot_distribution = {}
    for pdb in selected:
        uniprot_distribution[pdb.uniprot_id] = uniprot_distribution.get(pdb.uniprot_id, 0) + 1

    rationale = f"""Target Discovery Filtering Results for {disease}:

Selected {len(selected)} PDB structures across {len(uniprot_distribution)} unique protein targets.

Diversity Score: {diversity:.2f} (higher is better, indicating broad target coverage)

UniProt Distribution:
"""

    for uniprot_id, count in uniprot_distribution.items():
        rationale += f"  - {uniprot_id}: {count} structure(s)\n"

    rationale += "\nTop Selected Structures:\n"
    for i, pdb in enumerate(selected[:3], 1):
        rationale += f"  {i}. {pdb.pdb_id} (Score: {pdb.relevance_score:.3f})\n"
        rationale += f"     Ligand: {pdb.ligand_name}\n"
        rationale += f"     {pdb.description[:100]}...\n\n"

    return rationale


def run_experiment(test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Required interface for ShinkaEvolve evaluation.

    Each test case should contain:
    - disease: str - Disease name
    - candidates: List[Dict] - PDB candidate data
    """
    results = []

    for case in test_cases:
        disease = case["disease"]
        candidate_dicts = case["candidates"]

        # Convert to Pydantic models
        candidates = [PDBCandidate(**c) for c in candidate_dicts]

        # Run filtering algorithm
        filtered = target_discovery_filter(candidates, disease)

        # Return result
        results.append({
            "disease": disease,
            "num_selected": len(filtered.selected_pdbs),
            "diversity_score": filtered.diversity_score,
            "selected_pdb_ids": [pdb.pdb_id for pdb in filtered.selected_pdbs],
            "rationale": filtered.filtering_rationale,
            "filter_result": filtered
        })

    return results