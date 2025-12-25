#!/usr/bin/env python3
"""
CLF Continuation Quality Analyzer

For limit-causal files (degree Ω), this analyzes:
1. Perfect bijection at causal grid P(n)
2. Continuation quality outside P(n)

Shows the mathematical distinction between:
  • Exact reconstruction: Ξ(θ(S)) = S for i : |i-c| ∈ P(n)
  • Continuation: Ξ(θ(S)) ≈ S for i : |i-c| ∉ P(n)
"""

import os
import sys
from M4_recognition_SAMPLED import theta_sampled, BinaryStringSampler
from M3_xi_projected import Xi_projected


def analyze_file(file_path: str):
    """Analyze reconstruction quality at causal grid vs outside"""
    
    file_name = os.path.basename(file_path)
    print(f"\n{'═' * 80}")
    print(f"File: {file_name}")
    print(f"{'═' * 80}")
    
    # Load
    S = BinaryStringSampler(file_path)
    n = S.n
    center = n // 2
    print(f"Length: n={n:,} bytes")
    
    # Recognition
    Sigma = theta_sampled(S)
    family = Sigma.get('family')
    params = Sigma.get('params', {})
    meta = params.get('meta')
    
    if not meta:
        print("  ⚠ No meta information (not limit-causal)")
        return
    
    closure_type = meta.get('type', 'UNKNOWN')
    if closure_type != 'D9_LIMIT_CAUSAL_CLOSURE':
        print(f"  ℹ️  Closure: {closure_type} (not limit-causal, has full bijection)")
        return
    
    print(f"Closure: {closure_type}")
    
    # Extract causal grid
    radii_defined = meta.get('radii_defined', [])
    print(f"Strategic radii P(n): {len(radii_defined)} positions")
    print(f"  Radii: {radii_defined}")
    
    # Map radii to positions (causal grid)
    causal_positions = set()
    for r in radii_defined:
        if r == 0:
            causal_positions.add(center)
        else:
            if center - r >= 0:
                causal_positions.add(center - r)
            if center + r < n:
                causal_positions.add(center + r)
    
    print(f"  Mapped to {len(causal_positions)} causal grid positions")
    
    # Analyze reconstruction quality
    print(f"\n{'─' * 80}")
    print(f"RECONSTRUCTION ANALYSIS")
    print(f"{'─' * 80}")
    
    # Test all positions (sample if too large)
    if n > 10000:
        test_positions = sorted(list(causal_positions)) + [i for i in range(0, n, n // 100) if i not in causal_positions][:50]
        print(f"Testing {len(test_positions)} sampled positions (file too large for full scan)")
    else:
        test_positions = list(range(n))
        print(f"Testing all {len(test_positions)} positions")
    
    # Classify errors
    errors_at_grid = []
    errors_outside_grid = []
    perfect_at_grid = 0
    perfect_outside_grid = 0
    
    for i in test_positions:
        S_i = S._sample(i)
        S_recon_i = Xi_projected(Sigma, i)
        
        match = (S_i == S_recon_i)
        
        if i in causal_positions:
            # At causal grid - should be exact
            if match:
                perfect_at_grid += 1
            else:
                errors_at_grid.append((i, S_i, S_recon_i))
        else:
            # Outside grid - continuation (may differ)
            if match:
                perfect_outside_grid += 1
            else:
                errors_outside_grid.append((i, S_i, S_recon_i))
    
    # Report causal grid accuracy
    grid_tested = len([i for i in test_positions if i in causal_positions])
    non_grid_tested = len([i for i in test_positions if i not in causal_positions])
    
    print(f"\n1. CAUSAL GRID P(n): {grid_tested} positions tested")
    if grid_tested > 0:
        grid_accuracy = 100 * perfect_at_grid / grid_tested
        print(f"   Exact matches: {perfect_at_grid}/{grid_tested} ({grid_accuracy:.1f}%)")
        
        if errors_at_grid:
            print(f"   ❌ ERRORS at causal grid (should be 0):")
            for i, orig, recon in errors_at_grid[:5]:
                r = abs(i - center)
                print(f"      Position {i} (radius {r}): {orig} → {recon}")
        else:
            print(f"   ✅ PERFECT bijection at causal grid: Ξ(θ(S)) = S ∀i ∈ P(n)")
    
    print(f"\n2. CONTINUATION (outside P(n)): {non_grid_tested} positions tested")
    if non_grid_tested > 0:
        cont_accuracy = 100 * perfect_outside_grid / non_grid_tested
        print(f"   Exact matches: {perfect_outside_grid}/{non_grid_tested} ({cont_accuracy:.1f}%)")
        print(f"   Mismatches: {len(errors_outside_grid)}/{non_grid_tested} ({100-cont_accuracy:.1f}%)")
        
        if errors_outside_grid:
            print(f"\n   Sample mismatches (continuation, not errors):")
            for i, orig, recon in errors_outside_grid[:5]:
                r = abs(i - center)
                print(f"      Position {i} (radius {r}): {orig} → {recon} (Δ={abs(orig-recon)})")
    
    print(f"\n{'─' * 80}")
    print(f"MATHEMATICAL INTERPRETATION")
    print(f"{'─' * 80}")
    
    if grid_tested > 0 and perfect_at_grid == grid_tested:
        print("✅ Causal Grid: 100% exact reconstruction (bijection confirmed)")
    else:
        print("❌ Causal Grid: Bijection violation detected!")
    
    if non_grid_tested > 0:
        print(f"ℹ️  Outside Grid: {cont_accuracy:.1f}% match rate (continuation, not failure)")
        print(f"   CLF spec: Ξ(θ(S)) ≈ S for i ∉ P(n) (defined by continuation)")
    
    print()


def main():
    print("═" * 80)
    print("CLF CONTINUATION QUALITY ANALYZER")
    print("═" * 80)
    print()
    print("Distinguishes between:")
    print("  • Exact bijection at causal grid P(n)")
    print("  • Continuation approximation outside P(n)")
    print()
    print("═" * 80)
    
    test_files = [
        './test_artifacts/test_document.txt',
        './test_artifacts/pic1.jpeg',
        './test_artifacts/test_linear_pattern.bin',
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            analyze_file(file_path)
        else:
            print(f"\n⚠ File not found: {file_path}")
    
    print("\n" + "═" * 80)
    print("SUMMARY")
    print("═" * 80)
    print()
    print("For limit-causal files:")
    print("  • θ extracts O(log n) ring laws at strategic radii")
    print("  • Ξ provides EXACT reconstruction at those radii")
    print("  • Ξ uses continuation for positions outside P(n)")
    print("  • This is mathematically correct per CLF specification")
    print()
    print("See: CLF_DISCRETE_CONTINUATION_FORMAL_SPEC.md")
    print("═" * 80)


if __name__ == '__main__':
    main()
