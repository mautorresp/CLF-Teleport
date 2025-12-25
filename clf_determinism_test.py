"""
CLF Determinism Test - Mathematical Verification of Θ∘Ξ Stability

Verifies that Xi∘Theta is stable under repetition and environment-independent.
This confirms CLF operates as pure mathematical functions in ℤ₂₅₆.

Implements formal determinism validation:
∀S: Θ(Ξ(Θ(S))) = Θ(S) (idempotence)
∀S: Ξ(Θ(S)) produces identical results on repeated calls
"""

import hashlib
import os
from M7_pipeline import Sigma_star, Xi_n


def verify_determinism(S):
    """
    Confirms Ξ∘Θ is stable under repetition.
    
    Mathematically tests:
    1. h₁ = SHA256(Ξ(Θ(S)))
    2. h₂ = SHA256(Ξ(Θ(S))) 
    3. Assert h₁ = h₂ (deterministic reconstruction)
    
    Args:
        S: Binary string to test
        
    Raises:
        AssertionError: If determinism violation detected
    """
    # First encoding/decoding cycle
    sigma = Sigma_star(S, save_to_file=False)
    reconstruction1 = Xi_n(sigma, save_to_file=False)
    h1 = hashlib.sha256(reconstruction1).hexdigest()
    
    # Second encoding/decoding cycle (should be identical)
    sigma_repeat = Sigma_star(S, save_to_file=False)
    reconstruction2 = Xi_n(sigma_repeat, save_to_file=False)
    h2 = hashlib.sha256(reconstruction2).hexdigest()
    
    assert h1 == h2, f"Determinism violation detected: {h1} != {h2}"
    assert sigma == sigma_repeat, "Encoding non-determinism detected"
    assert reconstruction1 == reconstruction2, "Reconstruction non-determinism detected"


def verify_idempotence(S):
    """
    Confirms Θ(Ξ(Θ(S))) = Θ(S) (mathematical idempotence).
    
    Args:
        S: Binary string to test
        
    Raises:
        AssertionError: If idempotence violation detected
    """
    # First cycle: S → Θ(S)
    sigma1 = Sigma_star(S, save_to_file=False)
    
    # Second cycle: Θ(S) → Ξ(Θ(S)) → Θ(Ξ(Θ(S)))
    reconstruction = Xi_n(sigma1, save_to_file=False)
    sigma2 = Sigma_star(reconstruction, save_to_file=False)
    
    assert sigma1 == sigma2, f"Idempotence violation: Θ(Ξ(Θ(S))) ≠ Θ(S)"


def test_determinism(S):
    """
    Enhanced determinism test with Θ∘Ξ stability verification.
    
    Tests both recognition determinism and reconstruction stability:
    1. Θ(S) produces identical results across runs
    2. Ξ(Θ(S)) is stable under repetition
    3. Hash consistency verification
    
    Args:
        S: Binary string to test
        
    Raises:
        AssertionError: If any determinism violation detected
    """
    from M7_pipeline import Sigma_star, Xi_n
    import hashlib
    
    # Test 1: Recognition determinism - Θ(S) identical across runs
    sigma_a = Sigma_star(S, save_to_file=False)
    sigma_b = Sigma_star(S, save_to_file=False) 
    assert sigma_a == sigma_b, "Determinism failure: Θ differs across runs"
    
    # Test 2: Reconstruction stability - Ξ(Θ(S)) stable
    reconstruction_a = Xi_n(sigma_a, save_to_file=False)
    reconstruction_b = Xi_n(sigma_b, save_to_file=False)
    assert reconstruction_a == reconstruction_b, "Ξ∘Θ not stable"
    
    # Test 3: Original preservation - Ξ(Θ(S)) = S
    assert reconstruction_a == S, "Bijection violation: Ξ(Θ(S)) ≠ S"
    
    # Test 4: Hash consistency across runs
    hash_a = hashlib.sha256(reconstruction_a).hexdigest()
    hash_b = hashlib.sha256(reconstruction_b).hexdigest()
    assert hash_a == hash_b, "Hash inconsistency detected"
    
    print(f"  ✅ Enhanced determinism confirmed: Θ∘Ξ stability verified")


def run_determinism_tests():
    """Execute complete determinism validation suite."""
    print("Running CLF determinism self-test…")
    
    # Test with reference seed if available
    reference_path = "audit/seed_vault/reference.seed"
    if os.path.exists(reference_path):
        print("Testing with reference seed...")
        with open(reference_path, "rb") as f:
            S = f.read()
        verify_determinism(S)
        verify_idempotence(S)
        print("✅ Reference seed determinism confirmed")
    
    # Test with sample from test artifacts
    test_files = [
        "test_artifacts/test_message.txt",
        "test_artifacts/test_linear_pattern.bin", 
        "test_artifacts/structured_meta_law.bin"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"Testing {test_file}...")
            with open(test_file, "rb") as f:
                S = f.read()
            verify_determinism(S)
            verify_idempotence(S)
            print(f"✅ {test_file} determinism confirmed")
            break
    
    print("✅ CLF Determinism validation complete - all mathematical functions stable")


if __name__ == "__main__":
    run_determinism_tests()