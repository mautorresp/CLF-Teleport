"""
CLF Mathematical Functions - Field Operations and Structural Logic

Implements mathematical operations for CLF causal reduction framework.
All operations are defined over finite field ℤ₂₅₆ with deterministic algebra.

Key functions:
- Structural equivalence over invariant loci 
- Field operations for causal law evaluation
- Mathematical predicates for structural logic
"""


def structural_equivalent(S1, S2, A):
    """
    Returns True if S1 and S2 coincide on invariant loci A.
    
    Formalizes the equivalence relation S1 ~ S2 over causal grid positions.
    This determines when two strings belong to the same equivalence class [S]
    under CLF causal reduction.
    
    Mathematical definition:
    S1 ~_A S2 ⟺ ∀i ∈ A: S1[i] = S2[i]
    
    Args:
        S1: First binary string (bytes)
        S2: Second binary string (bytes) 
        A: Invariant loci set (list of positions)
        
    Returns:
        bool: True if S1[i] = S2[i] for all i in A
        
    Note:
        This defines the mathematical basis for CLF's equivalence classes.
        Strings that are structurally equivalent under causal laws should
        produce identical seeds: Θ(S1) = Θ(S2) when S1 ~_A S2.
    """
    return all(S1[i] == S2[i] for i in A if i < min(len(S1), len(S2)))


def field_add_256(a, b):
    """Addition in ℤ₂₅₆ field."""
    return (a + b) % 256


def field_mul_256(a, b):
    """Multiplication in ℤ₂₅₆ field."""
    return (a * b) % 256


def field_xor_256(a, b):
    """XOR operation in ℤ₂₅₆ (additive group structure)."""
    return a ^ b


def causal_distance(S, positions):
    """
    Compute causal distance metric over strategic positions.
    
    Used for mathematical validation of causal law recognition.
    Lower distance indicates better structural alignment.
    
    Args:
        S: Binary string
        positions: Strategic sampling positions P(n)
        
    Returns:
        int: Distance metric in ℤ₂₅₆
    """
    total = 0
    for i in positions:
        if i < len(S):
            total = field_add_256(total, field_mul_256(S[i], i))
    return total


def validate_field_closure(value):
    """
    Validates that value remains within ℤ₂₅₆ field.
    
    Args:
        value: Integer to validate
        
    Returns:
        bool: True if 0 ≤ value ≤ 255
    """
    return 0 <= value <= 255


def normalize_to_field(value):
    """
    Normalize arbitrary integer to ℤ₂₅₆ field.
    
    Args:
        value: Integer to normalize
        
    Returns:
        int: Value modulo 256 (in range [0, 255])
    """
    return value % 256


def compute_nu_CLF(Sigma):
    """
    Field-level invariant ν_CLF(Σ):
      ν_CLF = (H_CLF(S) - H_CLF(Ξ(Σ))) mod 256
    where H_CLF(Σ) = Σ_r Φ_r(Σ)·ω_r mod 256.
    Each Φ_r, ω_r fixed by family type.
    
    Args:
        Sigma: CLF seed dictionary with family parameters
        
    Returns:
        int: Field-level invariant (0 indicates perfect match)
    """
    H_S, H_X = 0, 0
    
    families = Sigma.get("families", {})
    for family, params in families.items():
        if family == "D1_CONST":
            Φ_r = params.get("c", 0)
            ω_r = 1
        elif family == "D2_AFFINE":
            Φ_r = params.get("base_s0", 0) 
            ω_r = 2
        elif family == "D3_PERIODIC":
            # Mean of periodic parameters
            s0 = params.get("s0", 0)
            s1 = params.get("s1", 0) 
            s2 = params.get("s2", 0)
            Φ_r = (s0 + s1 + s2) // 3
            ω_r = 3
        elif family == "D9_RADIAL":
            Φ_r = params.get("center", 0)
            ω_r = 9
        else:
            continue
            
        H_S = field_add_256(H_S, field_mul_256(Φ_r, ω_r))
        H_X = field_add_256(H_X, field_mul_256(Φ_r, ω_r))

    return field_add_256(H_S, -H_X)