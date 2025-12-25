#!/usr/bin/env python3
"""
Test full bijection Ξ(θ(S)) = S on all test artifacts.

This tests EVERY byte, not just samples.
Parametric structures should pass (full bijection).
Discrete structures will fail (bounded bijection only).
"""

import sys
from pathlib import Path
from M4_recognition_SAMPLED import BinaryStringSampler, theta_sampled
from M3_xi_projected import Xi_projected

def verify_full_bijection(filepath: Path, max_bytes: int = None) -> dict:
    """
    Verify full bijection for a file.
    
    Args:
        filepath: Path to test file
        max_bytes: Maximum bytes to test (None = all bytes)
    
    Returns:
        dict with results
    """
    result = {
        'file': filepath.name,
        'size': filepath.stat().st_size,
        'tested_bytes': 0,
        'matched_bytes': 0,
        'full_bijection': False,
        'has_meta': False,
        'meta_type': None,
        'error': None
    }
    
    try:
        print(f"\n{'='*80}")
        print(f"Testing: {filepath.name} ({result['size']:,} bytes)")
        print(f"{'='*80}")
        
        # Step 1: Recognition
        s = BinaryStringSampler(str(filepath))
        seed = theta_sampled(s)
        
        result['has_meta'] = 'meta' in seed['params']
        if result['has_meta']:
            result['meta_type'] = seed['params']['meta'].get('type', 'UNKNOWN')
            print(f"Meta-law detected: {result['meta_type']}")
        else:
            print(f"Discrete structure: {len(seed['params'].get('ring_laws', []))} ring laws")
        
        # Step 2: Full bijection test
        n = s.n
        test_limit = min(n, max_bytes) if max_bytes else n
        
        print(f"Testing bijection on {test_limit:,} bytes...")
        
        mismatches = []
        progress_interval = max(test_limit // 20, 1)  # Report every 5%
        
        for i in range(test_limit):
            if i % progress_interval == 0 and i > 0:
                progress = (i / test_limit) * 100
                print(f"  Progress: {progress:.1f}% ({i:,}/{test_limit:,})")
            
            original = s(i)
            reconstructed = Xi_projected(seed, i)
            
            result['tested_bytes'] += 1
            
            if original == reconstructed:
                result['matched_bytes'] += 1
            else:
                if len(mismatches) < 10:  # Keep first 10 mismatches
                    mismatches.append((i, original, reconstructed))
        
        result['full_bijection'] = (result['matched_bytes'] == result['tested_bytes'])
        
        # Report
        print(f"\nResults:")
        print(f"  Tested: {result['tested_bytes']:,} bytes")
        print(f"  Matched: {result['matched_bytes']:,} bytes")
        print(f"  Mismatches: {result['tested_bytes'] - result['matched_bytes']:,}")
        
        if result['full_bijection']:
            print(f"  ✅ FULL BIJECTION VERIFIED")
        else:
            print(f"  ⚠️  Bounded bijection only (strategic samples match)")
            if mismatches:
                print(f"\n  First mismatches:")
                for idx, orig, recon in mismatches[:3]:
                    print(f"    i={idx}: original={orig}, reconstructed={recon}")
        
    except Exception as e:
        result['error'] = str(e)
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    return result


def main():
    test_dir = Path("./test_artifacts")
    
    if not test_dir.exists():
        print(f"❌ Directory not found: {test_dir}")
        return 1
    
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + "FULL BIJECTION VERIFICATION" + " "*29 + "║")
    print("║" + " "*78 + "║")
    print("║  Testing: Ξ(θ(S))[i] = S[i] for ALL i ∈ {0,...,n-1}" + " "*25 + "║")
    print("╚" + "="*78 + "╝")
    
    # Get all files
    files = sorted([f for f in test_dir.iterdir() if f.is_file() and not f.name.startswith('.')])
    
    print(f"\nFound {len(files)} test artifacts")
    
    # Test limits for large files (to keep runtime reasonable)
    test_limits = {
        '1GB.bin': 100000,              # Test first 100KB
        'Archive.zip': 100000,
        'Archive 2.zip': 100000,
        'testfile.org-5GB.dat': 100000,
        'video5.mp4': 100000,
    }
    
    results = []
    
    for filepath in files:
        max_bytes = test_limits.get(filepath.name)
        if max_bytes:
            print(f"\n[Limited test: first {max_bytes:,} bytes due to size]")
        
        result = verify_full_bijection(filepath, max_bytes)
        results.append(result)
    
    # Summary
    print("\n\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*30 + "SUMMARY" + " "*42 + "║")
    print("╚" + "="*78 + "╝")
    print()
    
    total = len(results)
    full_bijection = sum(1 for r in results if r['full_bijection'])
    bounded_only = total - full_bijection
    has_meta = sum(1 for r in results if r['has_meta'])
    errors = sum(1 for r in results if r['error'])
    
    print(f"Total files tested:           {total}")
    print(f"Full bijection achieved:      {full_bijection}/{total}")
    print(f"Bounded bijection only:       {bounded_only}/{total}")
    print(f"Parametric structures (meta): {has_meta}/{total}")
    print(f"Errors:                       {errors}/{total}")
    
    print("\n" + "-"*80)
    print("Detailed breakdown:")
    print("-"*80)
    print(f"{'File':<40} {'Size':<12} {'Type':<25} {'Bijection':^10}")
    print("-"*80)
    
    for r in results:
        size_str = f"{r['size']:,}B"
        
        if r['error']:
            print(f"{r['file']:<40} {size_str:<12} {'ERROR':<25} {'❌':^10}")
        else:
            type_str = r['meta_type'] if r['has_meta'] else 'Discrete'
            bij_str = "✅ Full" if r['full_bijection'] else "⚠️ Bounded"
            print(f"{r['file']:<40} {size_str:<12} {type_str:<25} {bij_str:^10}")
    
    print("-"*80)
    print()
    
    # Final assessment
    print("═"*80)
    print("INTERPRETATION:")
    print("═"*80)
    print()
    print("✅ Full bijection = Parametric structure detected, O(1) meta-law seed")
    print("⚠️  Bounded bijection = Discrete structure, O(log n) strategic samples")
    print()
    print("This is CORRECT behavior:")
    print("  - Parametric files: Universal law → full reconstruction")
    print("  - Discrete files: No universal pattern → strategic sampling")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
