#!/usr/bin/env python3
"""External full bit-for-bit verification (NOT part of pipeline).

This script validates that Ξ(θ(S)) = S by:
1. Running θ(S) via the sampled interface to get seed
2. Regenerating the full string using Xi_projected byte-by-byte
3. Comparing every byte position with the original

This is intentionally external and can take time - it's for validation,
not part of the operational pipeline.

Usage:
    python3 external_full_verification.py [file1] [file2] ...
    
    If no files specified, runs on all test_artifacts/ files.
"""

import sys
from pathlib import Path
from typing import Callable


def verify_full_bijection(file_path: Path) -> tuple[bool, str, int]:
    """Verify Ξ(θ(S)) = S for every byte.
    
    Returns:
        (success: bool, message: str, bytes_checked: int)
    """
    from M4_recognition_SAMPLED import BinaryStringSampler, theta_sampled
    from M3_xi_projected import Xi_projected
    
    print(f"\n{'='*70}")
    print(f"File: {file_path.name}")
    print(f"Size: {file_path.stat().st_size:,} bytes")
    
    # Step 1: Get seed via sampled recognition
    print("Step 1: Computing θ(S)...")
    sampler = BinaryStringSampler(str(file_path))
    try:
        seed = theta_sampled(sampler)
        n = seed.get('n', 0)
        family = seed.get('family', '?')
        print(f"  → Seed family: {family}, n={n:,}")
        
        if n != file_path.stat().st_size:
            return False, f"Seed size mismatch: seed.n={n} != file_size={file_path.stat().st_size}", 0
        
        # Step 2: Verify every byte using Xi_projected
        print(f"Step 2: Verifying Ξ(θ(S))[i] = S[i] for all {n:,} indices...")
        
        errors = []
        checkpoint_interval = max(1, n // 20)  # Report progress every 5%
        
        for i in range(n):
            # Progress reporting
            if i % checkpoint_interval == 0 and i > 0:
                progress = (i / n) * 100
                print(f"  ... {progress:.1f}% ({i:,}/{n:,} bytes verified)", end='\r', flush=True)
            
            # Get projected byte from seed
            try:
                projected = Xi_projected(seed, i)
            except Exception as e:
                errors.append(f"Xi_projected failed at i={i}: {e}")
                if len(errors) >= 10:
                    break
                continue
            
            # Get actual byte from original
            actual = sampler(i)
            
            # Compare
            if projected != actual:
                errors.append(
                    f"Mismatch at byte {i} ({(i/n)*100:.3f}%): "
                    f"Ξ(θ(S))[{i}]={projected} != S[{i}]={actual}"
                )
                if len(errors) >= 10:
                    errors.append("(stopping after 10 errors)")
                    break
        
        print()  # Clear progress line
        
        if errors:
            error_msg = "\n".join(errors)
            return False, f"FAILED: Bit-for-bit verification failed:\n{error_msg}", i + 1
        else:
            return True, f"PASSED: All {n:,} bytes match perfectly", n
            
    finally:
        close = getattr(sampler, 'close', None)
        if callable(close):
            close()


def main():
    args = sys.argv[1:]
    
    if not args:
        # Default: test all files in test_artifacts/
        test_dir = Path("test_artifacts")
        if not test_dir.exists():
            print(f"Error: {test_dir} directory not found", file=sys.stderr)
            return 1
        
        files = sorted(test_dir.iterdir())
        files = [f for f in files if f.is_file()]
    else:
        files = [Path(arg) for arg in args]
    
    if not files:
        print("No files to verify", file=sys.stderr)
        return 1
    
    print("EXTERNAL FULL BIT-FOR-BIT VERIFICATION")
    print("=" * 70)
    print(f"Files to verify: {len(files)}")
    print("This is NOT part of the pipeline - it's for external validation.")
    print()
    
    results = []
    total_bytes = 0
    
    for file_path in files:
        if not file_path.exists():
            print(f"\nSkipping {file_path}: File not found")
            results.append((file_path.name, False, "File not found", 0))
            continue
        
        success, message, bytes_checked = verify_full_bijection(file_path)
        results.append((file_path.name, success, message, bytes_checked))
        total_bytes += bytes_checked
        
        print(f"Result: {message}")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, success, _, _ in results if success)
    failed = len(results) - passed
    
    print(f"\nTotal files: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total bytes verified: {total_bytes:,}")
    
    if failed > 0:
        print("\nFailed files:")
        for name, success, message, _ in results:
            if not success:
                print(f"  ✗ {name}")
                print(f"    {message}")
    else:
        print("\n✓ ALL FILES PASSED FULL BIT-FOR-BIT VERIFICATION")
        print(f"✓ Ξ(θ(S)) = S holds for all {total_bytes:,} bytes across {len(results)} files")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
