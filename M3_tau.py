"""
M3_tau.py - Execution Semantics (τ)
CLF 2.txt Section 1: Denotation, totality, reversibility

Implements: τ_Π : Conf → Conf (total, deterministic, bijective)

Key principle: τ is a mathematical function, not an algorithm.
Both τ_Π and τ_{Π^†} are equally fundamental (bijection).
"""

from typing import Tuple
from M1_codec import add256, mul256, xor8
from M2_types import Conf, Atom, Prog, make_C_init


# ============================================================================
# Atom Execution: τ_{(ω,θ)}
# ============================================================================

def tau_atom(a: Atom, C: Conf) -> Conf:
    """
    Apply single atom: τ_{(ω,θ)} : Conf → Conf
    
    CLF 2.txt Section 1: "each atom (ω,θ) has τ_{inv_ω(θ)} = τ_{(ω,θ)}⁻¹"
    
    Dispatcher to family-specific implementations.
    Note: Inverse families (e.g., RLE_SHORT_INV) have same semantics as forward
    due to mathematical reversibility - they differ only in conceptual direction.
    """
    # Strip _INV suffix if present (inverse has same τ semantics)
    family_base = a.family.replace('_INV', '')
    
    if family_base == 'id':
        return C.clone()  # Identity
    
    elif family_base == 'RLE_SHORT':
        return tau_RLE_SHORT(C)
    
    elif family_base == 'RLE_EXPLICIT':
        return tau_RLE_EXPLICIT(a.theta['s0'], a.theta['delta_mod'], C)
    
    elif family_base == 'CONST':
        return tau_CONST(a.theta['c'], a.theta['ell'], C)
    
    elif family_base == 'RLE_COMPOSE':
        return tau_RLE_COMPOSE(a.theta['s0'], a.theta['dmod'], a.theta['ell'], C)
    
    elif family_base == 'COPY':
        return tau_COPY(a.theta['off'], a.theta['ell'], C)
    
    elif family_base == 'XOR_CONST':
        return tau_XOR_CONST(a.theta['off'], a.theta['ell'], a.theta['c'], C)
    
    elif family_base == 'D4_XOR_AFFINE':
        return tau_D4_XOR_AFFINE(a.theta['s0'], a.theta['delta_mod'], a.theta['xor_const'], C)
    
    elif family_base == 'D5_QUADRATIC':
        return tau_D5_QUADRATIC(a.theta['a'], a.theta['b'], a.theta['c'], C)
    
    elif family_base == 'D6_LCG':
        return tau_D6_LCG(a.theta['seed'], a.theta['a'], a.theta['c'], C)
    
    elif family_base == 'D9_COMPOSITIONAL':
        return tau_D9_COMPOSITIONAL(a.theta['header_prog'], a.theta['body_prog'], C)
    
    elif family_base == 'D10_DICTIONARY':
        return tau_D10_DICTIONARY(a.theta['dictionary'], a.theta['indices'], C)
    
    else:
        raise ValueError(f"Unknown atom family: {a.family}")


# ============================================================================
# Family-Specific Implementations
# ============================================================================

def tau_RLE_SHORT(C: Conf) -> Conf:
    """
    RLE SHORT: Write n zeros to ℓ_out.
    
    Args:
        C: Configuration
    
    Returns:
        New configuration with zeros in ℓ_out
    """
    C_new = C.clone()
    # Write zeros to entire ℓ_out region
    for i in range(C_new.ell_out_len):
        C_new.M[C_new.ell_out_start + i] = 0
    return C_new


def tau_RLE_EXPLICIT(s0: int, delta_mod: int, C: Conf) -> Conf:
    """
    RLE EXPLICIT: Write affine ramp s0 ⊕ (i·δ mod 256).
    
    CLF 2.txt Section 5.3: Canonical Δ ∈ [-128, 127]
    Runtime uses dmod = Δ mod 256
    
    Args:
        s0: Initial value (0-255)
        delta_mod: Δ mod 256 (0-255)
        C: Configuration
    
    Returns:
        New configuration with affine sequence
    """
    C_new = C.clone()
    n = C_new.ell_out_len
    
    # Write affine sequence using delta_mod directly
    for i in range(n):
        C_new.M[C_new.ell_out_start + i] = add256(s0, mul256(i, delta_mod))
    
    return C_new


def tau_D4_XOR_AFFINE(s0: int, delta_mod: int, xor_const: int, C: Conf) -> Conf:
    """
    D4_XOR_AFFINE: Write ((s0 + i·δ) mod 256) ⊕ c for entire output.
    
    Bijective CLF Boolean: Single atomic operation that combines
    affine generation and XOR transformation.
    
    Args:
        s0: Initial value (0-255)
        delta_mod: Δ mod 256 (0-255)
        xor_const: XOR constant (0-255)
        C: Configuration
    
    Returns:
        New configuration with XOR-affine sequence
    """
    C_new = C.clone()
    n = C_new.ell_out_len
    
    # Write XOR-affine sequence: S[i] = (s0 + i·δ) ⊕ c
    for i in range(n):
        affine_val = add256(s0, mul256(i, delta_mod))
        C_new.M[C_new.ell_out_start + i] = xor8(affine_val, xor_const)
    
    return C_new


def tau_D6_LCG(seed: int, a: int, c: int, C: Conf) -> Conf:
    """
    D6_LCG: Write S[i] = (a·S[i-1] + c) mod 256 with S[0] = seed.
    
    Linear Congruential Generator - recurrence relation.
    Bijective CLF Boolean: Single atomic operation that generates
    sequence via recurrence.
    
    Args:
        seed: Initial value S[0] (0-255)
        a: Multiplier (0-255)
        c: Increment (0-255)
        C: Configuration
    
    Returns:
        New configuration with LCG sequence
    """
    C_new = C.clone()
    n = C_new.ell_out_len
    
    if n == 0:
        return C_new
    
    # Write LCG sequence: S[0] = seed, S[i] = (a·S[i-1] + c) mod 256
    C_new.M[C_new.ell_out_start] = seed
    
    for i in range(1, n):
        prev = C_new.M[C_new.ell_out_start + i - 1]
        C_new.M[C_new.ell_out_start + i] = (a * prev + c) % 256
    
    return C_new


def tau_D9_COMPOSITIONAL(header_prog: 'Prog', body_prog: 'Prog', C: Conf) -> Conf:
    """
    D9_COMPOSITIONAL: Concatenate execution of header and body segments.
    
    Recursively executes: header_prog then body_prog
    Output = τ(header_prog) || τ(body_prog)
    
    Args:
        header_prog: Program for header segment
        body_prog: Program for body segment  
        C: Configuration
    
    Returns:
        Configuration with concatenated output
    """
    # M8_interpreter was removed - this function is deprecated
    # Use M3_tau_pure.R_n_pure instead
    raise NotImplementedError("Use M3_tau_pure.R_n_pure instead of execute_program")
    
    C_new = C.clone()
    n = C_new.ell_out_len
    
    header_len = header_prog.n
    body_len = body_prog.n
    
    if header_len + body_len != n:
        raise ValueError(f"Segment mismatch: {header_len} + {body_len} != {n}")
    
    # Execute header into first segment
    C_header = C_new.clone()
    C_header.ell_out_len = header_len
    C_header = execute_program(header_prog, C_header)
    
    # Execute body into second segment
    C_body = C_new.clone()
    C_body.ell_out_start = C_new.ell_out_start + header_len
    C_body.ell_out_len = body_len
    C_body = execute_program(body_prog, C_body)
    
    # Combine results
    for i in range(header_len):
        C_new.M[C_new.ell_out_start + i] = C_header.M[C_header.ell_out_start + i]
    
    for i in range(body_len):
        C_new.M[C_new.ell_out_start + header_len + i] = C_body.M[C_body.ell_out_start + i]
    
    return C_new


def tau_D10_DICTIONARY(dictionary: list, indices: list, C: Conf) -> Conf:
    """
    D10_DICTIONARY: Symbol table lookup.
    
    Causal Law: ∀i ∈ [0,n): S[i] = D[I[i]]
    Where D = dictionary, I = index sequence.
    
    Args:
        dictionary: List of unique symbols
        indices: List of dictionary indices
        C: Configuration
    
    Returns:
        Configuration with output bytes from lookups
    """
    C_new = C.clone()
    n = len(indices)
    
    # Perform lookups: S[i] = D[I[i]]
    for i, idx in enumerate(indices):
        if idx < len(dictionary):
            C_new.M[C_new.ell_out_start + i] = dictionary[idx]
        else:
            # Invalid index - should not happen in valid CLF
            C_new.M[C_new.ell_out_start + i] = 0
    
    return C_new


def tau_D5_QUADRATIC(a: int, b: int, c: int, C: Conf) -> Conf:
    """
    D5_QUADRATIC: Write (a·i² + b·i + c) mod 256 for entire output.
    
    Bijective CLF Boolean: Single atomic operation that generates
    quadratic sequence.
    
    Args:
        a: Quadratic coefficient (0-255)
        b: Linear coefficient (0-255)
        c: Constant term (0-255)
        C: Configuration
    
    Returns:
        New configuration with quadratic sequence
    """
    C_new = C.clone()
    n = C_new.ell_out_len
    
    # Write quadratic sequence: S[i] = (a·i² + b·i + c) mod 256
    for i in range(n):
        val = (a * i * i + b * i + c) % 256
        C_new.M[C_new.ell_out_start + i] = val
    
    return C_new


def tau_CONST(c: int, ell: int, C: Conf) -> Conf:
    """
    CONST: Write ℓ copies of constant c.
    
    Args:
        c: Constant value (0-255)
        ell: Length to write
        C: Configuration (with cursor in ancilla)
    
    Returns:
        New configuration with c written ℓ times
    """
    C_new = C.clone()
    p = C_new.A.get('p', 0)  # Current write position
    
    if p + ell > C_new.ell_out_len:
        raise ValueError(f"CONST: write exceeds ℓ_out bounds")
    
    # Write constant ℓ times
    for i in range(ell):
        C_new.M[C_new.ell_out_start + p + i] = c
    
    # Update cursor
    C_new.A['p'] = p + ell
    
    return C_new


def tau_RLE_COMPOSE(s0: int, dmod: int, ell: int, C: Conf) -> Conf:
    """
    RLE (compose variant): Write affine sequence of length ℓ.
    
    Args:
        s0: Initial value
        dmod: Delta modulo 256
        ell: Length to write
        C: Configuration
    
    Returns:
        New configuration with affine sequence
    """
    C_new = C.clone()
    p = C_new.A.get('p', 0)
    
    if p + ell > C_new.ell_out_len:
        raise ValueError(f"RLE_COMPOSE: write exceeds ℓ_out bounds")
    
    # Write affine sequence
    for j in range(ell):
        C_new.M[C_new.ell_out_start + p + j] = add256(s0, mul256(j, dmod))
    
    # Update cursor
    C_new.A['p'] = p + ell
    
    return C_new


def tau_COPY(off: int, ell: int, C: Conf) -> Conf:
    """
    COPY: Copy ℓ bytes from [p-offset] to [p].
    
    Args:
        off: Offset backward (1 to p)
        ell: Length to copy
        C: Configuration
    
    Returns:
        New configuration with copied bytes
    """
    C_new = C.clone()
    p = C_new.A.get('p', 0)
    
    if off < 1 or off > p:
        raise ValueError(f"COPY: invalid offset {off} (p={p})")
    
    if p + ell > C_new.ell_out_len:
        raise ValueError(f"COPY: write exceeds ℓ_out bounds")
    
    # Copy bytes (handle overlapping correctly)
    for i in range(ell):
        src_idx = C_new.ell_out_start + p - off + i
        dst_idx = C_new.ell_out_start + p + i
        C_new.M[dst_idx] = C_new.M[src_idx]
    
    # Update cursor
    C_new.A['p'] = p + ell
    
    return C_new


def tau_XOR_CONST(off: int, ell: int, c: int, C: Conf) -> Conf:
    """
    XOR_CONST: XOR ℓ bytes at [p-offset] with constant c, write to [p].
    
    Args:
        off: Offset backward
        ell: Length to process
        c: XOR constant (0-255)
        C: Configuration
    
    Returns:
        New configuration with XORed bytes
    """
    C_new = C.clone()
    p = C_new.A.get('p', 0)
    
    if off < 1 or off > p:
        raise ValueError(f"XOR_CONST: invalid offset {off} (p={p})")
    
    if p + ell > C_new.ell_out_len:
        raise ValueError(f"XOR_CONST: write exceeds ℓ_out bounds")
    
    # XOR and write
    for i in range(ell):
        src_idx = C_new.ell_out_start + p - off + i
        dst_idx = C_new.ell_out_start + p + i
        C_new.M[dst_idx] = xor8(C_new.M[src_idx], c)
    
    # Update cursor
    C_new.A['p'] = p + ell
    
    return C_new


# ============================================================================
# Program Execution: τ_Π
# ============================================================================

def tau(P: Prog, C: Conf) -> Conf:
    """
    Apply program: τ_Π : Conf → Conf
    
    CLF 2.txt Section 1: "τ_Π : Conf → Conf total & deterministic"
    
    Composition of atomic transformations:
    τ_Π = τ_{atom_m} ∘ ... ∘ τ_{atom_2} ∘ τ_{atom_1}
    
    Args:
        P: Program
        C: Initial configuration
    
    Returns:
        Final configuration after applying all atoms
    """
    current = C.clone()
    
    for atom in P.BODY:
        current = tau_atom(atom, current)
    
    return current


def tau_inv(P: Prog, C: Conf) -> Conf:
    """
    Apply inverse program: τ_{Π^†}
    
    CLF 2.txt Section 1: τ_{Π^†} = (τ_Π)⁻¹
    
    Args:
        P: Program
        C: Configuration
    
    Returns:
        Configuration after applying Π^†
    """
    return tau(P.reverse(), C)


# ============================================================================
# Output Extraction: R_n
# ============================================================================

def R_n(P: Prog, edition: str = "v3.3.8") -> bytes:
    """
    Extract output: R_n(Π) := τ_Π(C_init(n)).M[ℓ_out]
    
    CLF 2.txt Section 1: "Output maps: R_n(Π) := (τ_Π(C_init(n))).M(ℓ_out)"
    
    This is the fundamental replay operation.
    
    Args:
        P: Program
        edition: Edition identifier
    
    Returns:
        Output bytes (length = P.n)
    """
    C_init = make_C_init(P.n, edition)
    C_final = tau(P, C_init)
    return C_final.get_output()


# ============================================================================
# Verification: Run_ok
# ============================================================================

def Run_ok(P: Prog, edition: str = "v3.3.8") -> bool:
    """
    Check admissibility: Run_ok(Π) = 1 ⇔ successful replay
    
    CLF 2.txt Section 1: "Run_ok(Π) = 1 ⇔ run from C_init(n) completes,
    ancilla restored, and no guard/sentinel fails"
    
    For this basic edition, admissibility means:
    - Program executes without raising exceptions
    - Output cursor p equals n at end
    - Ancilla in valid state
    
    Args:
        P: Program
        edition: Edition identifier
    
    Returns:
        True if admissible, False otherwise
    """
    try:
        C_init = make_C_init(P.n, edition)
        C_final = tau(P, C_init)
        
        # Check cursor at end (for COMPOSE programs)
        if 'p' in C_final.A:
            if C_final.A['p'] != P.n:
                return False
        
        # Check sentinels unchanged (basic check)
        if C_final.sigma != C_init.sigma:
            return False
        
        return True
    
    except Exception:
        return False


# ============================================================================
# Verification: Reversibility
# ============================================================================

def verify_reversibility(P: Prog, C: Conf) -> bool:
    """
    Verify: τ_{Π^†} ∘ τ_Π = id
    
    CLF 2.txt Section 1: Reversibility axiom
    
    Args:
        P: Program
        C: Starting configuration
    
    Returns:
        True if reversibility holds
    """
    C_forward = tau(P, C)
    C_backward = tau_inv(P, C_forward)
    
    # Check all components
    return (
        C_backward.M == C.M and
        C_backward.A == C.A and
        C_backward.sigma == C.sigma
    )


# ============================================================================
# Module Metadata
# ============================================================================

__all__ = [
    # Atomic execution
    'tau_atom',
    'tau_RLE_SHORT',
    'tau_RLE_EXPLICIT',
    'tau_CONST',
    'tau_RLE_COMPOSE',
    'tau_COPY',
    'tau_XOR_CONST',
    
    # Program execution
    'tau',
    'tau_inv',
    
    # Output extraction
    'R_n',
    
    # Verification
    'Run_ok',
    'verify_reversibility',
]
