#!/usr/bin/env python3
"""
CLF Full Reconstruction Validator — Bit-Perfect Verification

Validates that Ξ(θ(S)) = S bit-for-bit across ALL bytes using:
1. CLF pipeline: Σ = θ(S), S' = Ξ(Σ) 
2. Binary export to disk
3. macOS native checksums (shasum/md5) for validation

This keeps the CLF pipeline completely untouched and uses system-level
I/O for maximum validation speed.
"""

import os
import sys
import subprocess
import tempfile
from M4_recognition_SAMPLED import theta_sampled, BinaryStringSampler
from M3_xi_projected import Xi_projected


def validate_full_reconstruction(file_path: str, use_tempfiles: bool = True) -> dict:
    """
    Validate complete bit-for-bit reconstruction: Ξ(θ(S)) = S
    
    Args:
        file_path: Path to test file
        use_tempfiles: If True, write to /tmp; if False, write to current dir
        
    Returns:
        dict with validation results
    """
    file_name = os.path.basename(file_path)
    print(f"\n{'─' * 80}")
    print(f"Validating: {file_name}")
    print(f"{'─' * 80}")
    
    # Step 1: Load original string
    print(f"  [1/5] Loading original string S...")
    try:
        S = BinaryStringSampler(file_path)
        n = S.n
        print(f"        Length: n={n:,} bytes")
    except Exception as e:
        return {"success": False, "error": f"Failed to load: {e}"}
    
    # Step 2: Recognition — θ(S) → Σ
    print(f"  [2/5] Computing causal seed: Σ = θ(S)...")
    try:
        Sigma = theta_sampled(S)
        family = Sigma.get('family')
        params = Sigma.get('params', {})
        meta = params.get('meta')
        if meta:
            closure_type = meta.get('type', 'UNKNOWN')
        else:
            closure_type = family
        print(f"        Closure: {closure_type}")
    except Exception as e:
        return {"success": False, "error": f"Recognition failed: {e}"}
    
    # Step 3: Full reconstruction — Ξ(Σ) → S' for ALL positions
    print(f"  [3/5] Reconstructing ALL bytes: S' = Ξ(Σ)...")
    print(f"        (This may take a moment for large files...)")
    
    try:
        S_reconstructed = bytearray(n)
        
        # Reconstruct every byte
        for i in range(n):
            S_reconstructed[i] = Xi_projected(Sigma, i)
            
            # Progress indicator for large files
            if n > 10000 and i % (n // 10) == 0 and i > 0:
                progress = (i / n) * 100
                print(f"        Progress: {progress:.0f}% ({i:,}/{n:,} bytes)")
        
        S_reconstructed = bytes(S_reconstructed)
        print(f"        ✓ Reconstruction complete: {len(S_reconstructed):,} bytes")
    except Exception as e:
        return {"success": False, "error": f"Reconstruction failed: {e}"}
    
    # Step 4: Export both to disk for native comparison
    print(f"  [4/5] Exporting to disk for native validation...")
    
    if use_tempfiles:
        temp_dir = "/tmp"
    else:
        temp_dir = "."
    
    # Create safe filenames
    base_name = file_name.replace(' ', '_').replace('×', 'x')
    original_path = os.path.join(temp_dir, f"clf_original_{base_name}")
    reconstructed_path = os.path.join(temp_dir, f"clf_reconstructed_{base_name}")
    
    try:
        # Write original
        with open(original_path, "wb") as f:
            # Read original in chunks to handle large files
            chunk_size = 1024 * 1024  # 1MB chunks
            for i in range(0, n, chunk_size):
                end = min(i + chunk_size, n)
                chunk = bytes([S._sample(j) for j in range(i, end)])
                f.write(chunk)
        
        # Write reconstructed
        with open(reconstructed_path, "wb") as f:
            f.write(S_reconstructed)
        
        print(f"        Original:      {original_path}")
        print(f"        Reconstructed: {reconstructed_path}")
    except Exception as e:
        return {"success": False, "error": f"Export failed: {e}"}
    
    # Step 5: Native validation using macOS tools
    print(f"  [5/5] Running native checksum validation...")
    
    # Method 1: Use shasum for cryptographic verification
    try:
        result_orig = subprocess.run(
            ['shasum', '-a', '256', original_path],
            capture_output=True,
            text=True,
            check=True
        )
        hash_orig = result_orig.stdout.split()[0]
        
        result_recon = subprocess.run(
            ['shasum', '-a', '256', reconstructed_path],
            capture_output=True,
            text=True,
            check=True
        )
        hash_recon = result_recon.stdout.split()[0]
        
        print(f"        SHA-256 (original):      {hash_orig[:16]}...")
        print(f"        SHA-256 (reconstructed): {hash_recon[:16]}...")
        
        if hash_orig == hash_recon:
            print(f"        ✅ HASHES MATCH")
            hash_match = True
        else:
            print(f"        ❌ HASH MISMATCH")
            hash_match = False
    except subprocess.CalledProcessError as e:
        print(f"        ⚠ shasum failed: {e}")
        hash_match = None
        hash_orig = None
        hash_recon = None
    
    # Method 2: Use cmp for byte-by-byte verification
    print(f"\n  Running byte-level diff check...")
    try:
        result = subprocess.run(
            ['cmp', '-s', original_path, reconstructed_path],
            capture_output=True
        )
        
        if result.returncode == 0:
            print(f"        ✅ cmp: Files are IDENTICAL (bit-perfect match)")
            cmp_match = True
        else:
            print(f"        ❌ cmp: Files DIFFER")
            # Show first few differences
            diff_result = subprocess.run(
                ['cmp', '-l', original_path, reconstructed_path],
                capture_output=True,
                text=True
            )
            lines = diff_result.stdout.strip().split('\n')[:5]
            if lines:
                print(f"        First differences:")
                for line in lines:
                    print(f"          {line}")
            cmp_match = False
    except Exception as e:
        print(f"        ⚠ cmp failed: {e}")
        cmp_match = None
    
    # Cleanup temp files
    try:
        os.remove(original_path)
        os.remove(reconstructed_path)
    except:
        pass
    
    # Final verdict
    success = hash_match and cmp_match
    
    if success:
        print(f"\n  {'═' * 76}")
        print(f"  ✅ BIT-PERFECT RECONSTRUCTION CONFIRMED: Ξ(θ(S)) = S")
        print(f"  {'═' * 76}")
    else:
        print(f"\n  {'═' * 76}")
        print(f"  ❌ RECONSTRUCTION MISMATCH")
        print(f"  {'═' * 76}")
    
    return {
        "success": success,
        "file": file_name,
        "n": n,
        "closure": closure_type,
        "hash_match": hash_match,
        "cmp_match": cmp_match,
        "hash_original": hash_orig,
        "hash_reconstructed": hash_recon
    }


def main():
    print("═" * 80)
    print("CLF FULL RECONSTRUCTION VALIDATOR — Bit-Perfect Verification")
    print("═" * 80)
    print()
    print("Pipeline: S → θ(S) → Ξ(Σ) → S'")
    print("Validation: Native checksums (shasum + cmp)")
    print()
    print("═" * 80)
    
    # Test artifacts directory
    test_dir = './test_artifacts'
    
    # Test ALL files in the directory
    test_files = [
        '1GB.bin',
        'Archive 2.zip',
        'Archive.zip',
        'pic1.jpeg',
        'pic2.jpeg',
        'pic3.jpeg',
        'randomfile.bin',
        'sample_1920×1280.bmp',
        'sample_1920×1280.png',
        'sample_960x400_ocean_with_audio.webm',
        'sample3.pdf',
        'sample4.docx',
        'structured_meta_law.bin',
        'Symphony No.6 (1st movement).mp3',
        'test_document.txt',
        'test_linear_pattern.bin',
        'test_message.txt',
        'testfile.org-5GB.dat',
        'video1.mp4',
        'video2.mp4',
        'video3.mp4',
        'video4.mp4',
        'video5.mp4',
    ]
    
    results = []
    perfect_count = 0
    
    for file_name in test_files:
        file_path = os.path.join(test_dir, file_name)
        
        if not os.path.exists(file_path):
            print(f"\n⚠ Skipping {file_name} (not found)")
            continue
        
        # Skip very large files to keep validation fast
        file_size = os.path.getsize(file_path)
        if file_size > 2 * 1024 * 1024 * 1024:  # Skip files > 2GB for speed
            print(f"\n⚠ Skipping {file_name} ({file_size:,} bytes - too large for full scan)")
            continue
        
        result = validate_full_reconstruction(file_path)
        results.append(result)
        
        if result["success"]:
            perfect_count += 1
    
    # Summary
    print(f"\n{'═' * 80}")
    print(f"VALIDATION SUMMARY")
    print(f"{'═' * 80}")
    print()
    print(f"Files tested: {len(results)}")
    print()
    
    # Separate parametric vs limit-causal
    parametric = [r for r in results if r.get('closure') in ['D1_CONSTANT', 'D2_AFFINE_CONSTANT_DELTA', 'D3_AFFINE_LINEAR_GRADIENT', 'D4_AFFINE_QUADRATIC']]
    limit_causal = [r for r in results if r.get('closure') == 'D9_LIMIT_CAUSAL_CLOSURE']
    
    print(f"Parametric (p ≤ 4):   {len(parametric)} files")
    print(f"Limit-causal (p = Ω): {len(limit_causal)} files")
    print()
    
    # Parametric files should have 100% bijection
    parametric_perfect = [r for r in parametric if r['success']]
    print(f"Parametric bit-perfect: {len(parametric_perfect)}/{len(parametric)}")
    if len(parametric) > 0 and len(parametric_perfect) == len(parametric):
        print(f"  ✅ All parametric files: EXACT reconstruction (Ξ(θ(S)) = S ∀i)")
    elif len(parametric) > 0:
        print(f"  ⚠ Some parametric files failed:")
        for r in parametric:
            if not r['success']:
                print(f"    ✗ {r['file']}")
    print()
    
    # Limit-causal files have bounded bijection
    print(f"Limit-causal bit-perfect: {len([r for r in limit_causal if r['success']])}/{len(limit_causal)}")
    if len(limit_causal) > 0:
        print()
        print("ℹ️  CLF MATHEMATICAL SPECIFICATION:")
        print("   For limit-causal closure (degree Ω):")
        print("     • Ξ(θ(S)) = S  for all i : |i-c| ∈ P(n)  [causal grid, ~30 positions]")
        print("     • Ξ(θ(S)) ≈ S  for all i : |i-c| ∉ P(n)  [continuation, not bijection]")
        print()
        print("   Full bit-for-bit reconstruction is NOT guaranteed for limit-causal.")
        print("   See: CLF_DISCRETE_CONTINUATION_FORMAL_SPEC.md lines 42-85")
        print()
        print("   To validate bounded bijection at causal grid:")
        print("     $ python3 validate_clf_causal_anchors.py")
    
    print()
    print("═" * 80)


if __name__ == '__main__':
    main()
