"""
M5_construction.py - Program Construction (Π₀)
CLF 2.txt Section 3: Recognition → program construction

Implements: Π₀ : Dₙ → Prog(n) with R_n(Π₀(S)) = S

Constructs programs from recognized patterns (θ output).
Guarantees: Every S ∈ Dₙ has a program Π₀(S) that replays to S.

Key principle: Construction is deterministic from θ(S).
Selection by (cost, priority, lex) per CLF 2.txt Section 6.5.
"""

from typing import Dict, List, Tuple, Optional
from M1_codec import Lgamma
from M2_types import Atom, Prog, make_inverse_atom


# ============================================================================
# Atom Construction Helpers
# ============================================================================

def make_RLE_SHORT_atom() -> Atom:
    """
    Construct RLE_SHORT atom pair (forward + inverse)
    
    Returns:
        Atom with inverse relationship established
    """
    forward = Atom("RLE_SHORT", {})
    inverse = Atom("RLE_SHORT_INV", {})
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_RLE_EXPLICIT_atom(s0: int, delta_mod: int) -> Atom:
    """
    Construct RLE_EXPLICIT atom pair
    
    Args:
        s0: Initial value (0-255)
        delta_mod: Δ mod 256 (0-255)
    
    Returns:
        Atom with inverse relationship
    """
    theta_params = {"s0": s0, "delta_mod": delta_mod}
    forward = Atom("RLE_EXPLICIT", theta_params)
    inverse = Atom("RLE_EXPLICIT_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_CONST_atom(c: int, ell: int) -> Atom:
    """
    Construct CONST atom pair
    
    Args:
        c: Constant value (0-255)
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"c": c, "ell": ell}
    forward = Atom("CONST", theta_params)
    inverse = Atom("CONST_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_COPY_atom(off: int, ell: int) -> Atom:
    """
    Construct COPY atom pair
    
    Args:
        off: Offset backward
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"off": off, "ell": ell}
    forward = Atom("COPY", theta_params)
    inverse = Atom("COPY_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_XOR_CONST_atom(off: int, ell: int, c: int) -> Atom:
    """
    Construct XOR_CONST atom pair
    
    Args:
        off: Offset backward
        ell: Length
        c: XOR constant
    
    Returns:
        Atom with inverse
    """
    theta_params = {"off": off, "ell": ell, "c": c}
    forward = Atom("XOR_CONST", theta_params)
    inverse = Atom("XOR_CONST_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_PERMUTE_atom(permutation: list, ell: int) -> Atom:
    """
    Construct PERMUTE atom pair
    
    Args:
        permutation: 256-byte permutation map π[i] → byte
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"permutation": permutation, "ell": ell}
    forward = Atom("PERMUTE", theta_params)
    
    # Compute inverse permutation
    inv_perm = [0] * 256
    for i in range(256):
        inv_perm[permutation[i]] = i
    
    inverse = Atom("PERMUTE_INV", {"permutation": inv_perm, "ell": ell})
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_MOD_ARITH_atom(a: int, b: int, m: int, ell: int) -> Atom:
    """
    Construct MOD_ARITH atom pair
    
    Evaluator: E(i) = (a*i + b) mod m
    
    Args:
        a: Multiplier
        b: Additive constant
        m: Modulus
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"a": a, "b": b, "m": m, "ell": ell}
    forward = Atom("MOD_ARITH", theta_params)
    
    # Inverse: solve (a*i + b) mod m = y → i = (a_inv * (y - b)) mod m
    # For simplicity, inverse is same params (requires runtime inversion)
    inverse = Atom("MOD_ARITH_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_REV_LOGIC_atom(gate: str, params: dict, ell: int) -> Atom:
    """
    Construct REV_LOGIC atom pair
    
    Args:
        gate: Gate type ("NOT", "ROTATE_LEFT", "BIT_REVERSE")
        params: Gate-specific parameters
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"gate": gate, "params": params, "ell": ell}
    forward = Atom("REV_LOGIC", theta_params)
    
    # Compute inverse gate
    if gate == "NOT":
        inv_gate = "NOT"  # Self-inverse
        inv_params = params.copy()
    elif gate == "ROTATE_LEFT":
        inv_gate = "ROTATE_RIGHT"
        inv_params = {"rotation": params["rotation"]}
    elif gate == "BIT_REVERSE":
        inv_gate = "BIT_REVERSE"  # Self-inverse
        inv_params = params.copy()
    else:
        inv_gate = gate
        inv_params = params.copy()
    
    inverse = Atom("REV_LOGIC_INV", {"gate": inv_gate, "params": inv_params, "ell": ell})
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_CELLULAR_AUTO_atom(rule: int, seed: bytes, ell: int) -> Atom:
    """
    Construct CELLULAR_AUTO atom pair
    
    Args:
        rule: CA rule number
        seed: Initial seed
        ell: Length (output length)
    
    Returns:
        Atom with inverse
    """
    theta_params = {"rule": rule, "seed": seed, "ell": ell}
    forward = Atom("CELLULAR_AUTO", theta_params)
    
    # CA inversion requires reverse rule (not trivial)
    # For now, inverse stores same params (requires special handling)
    inverse = Atom("CELLULAR_AUTO_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_GRAMMAR_atom(grammar_type: str, params: dict, ell: int) -> Atom:
    """
    Construct GRAMMAR atom pair
    
    Args:
        grammar_type: Grammar type ("periodic", "balanced_delimiters", etc.)
        params: Grammar-specific parameters
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"grammar_type": grammar_type, "params": params, "ell": ell}
    forward = Atom("GRAMMAR", theta_params)
    
    # Grammar inversion (parse → generate)
    inverse = Atom("GRAMMAR_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_AUTOMATA_atom(automaton_type: str, states: list, period: int, ell: int) -> Atom:
    """
    Construct AUTOMATA atom pair
    
    Args:
        automaton_type: Automaton type ("cyclic", etc.)
        states: State list
        period: Cycle period
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"automaton_type": automaton_type, "states": states, "period": period, "ell": ell}
    forward = Atom("AUTOMATA", theta_params)
    
    # Automaton inverse (trace → input)
    inverse = Atom("AUTOMATA_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


def make_SYMMETRY_atom(symmetry_type: str, params: dict, ell: int) -> Atom:
    """
    Construct SYMMETRY atom pair
    
    Args:
        symmetry_type: Symmetry type ("palindrome", "reversed_offset", "reversed_complement")
        params: Symmetry-specific parameters
        ell: Length
    
    Returns:
        Atom with inverse
    """
    theta_params = {"symmetry_type": symmetry_type, "params": params, "ell": ell}
    forward = Atom("SYMMETRY", theta_params)
    
    # Symmetry inverse (depends on type, many are self-inverse)
    inverse = Atom("SYMMETRY_INV", theta_params.copy())
    forward.inv = inverse
    inverse.inv = forward
    return forward


# ============================================================================
# Π₀ Constructors (per pattern)
# ============================================================================

def Pi_0_RLE_SHORT(n: int) -> Prog:
    """
    Construct Π₀ for D1 (zero law)
    
    Program: RLE_SHORT
    Output: n zeros
    
    Args:
        n: Arity
    
    Returns:
        Program with R_n(Π₀) = zeros(n)
    """
    atom = make_RLE_SHORT_atom()
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x01}
    )


def Pi_0_RLE_EXPLICIT(n: int, s0: int, delta: int) -> Prog:
    """
    Construct Π₀ for D2 (affine law)
    
    Program: RLE_EXPLICIT(s0, δ_mod)
    Output: s0, s0+Δ, s0+2Δ, ... (mod 256)
    
    Args:
        n: Arity
        s0: Initial value (0-255)
        delta: Delta (−128 to 127)
    
    Returns:
        Program with R_n(Π₀) = affine_sequence(s0, delta, n)
    """
    # Convert canonical delta to modular form
    delta_mod = delta if delta >= 0 else (256 + delta)
    atom = make_RLE_EXPLICIT_atom(s0, delta_mod)
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x01}
    )


def Pi_0_COMPOSE_per_byte(S: bytes) -> Prog:
    """
    Construct Π₀ using run-length encoding - EXISTENCE-DRIVEN
    
    CLF PRINCIPLE: The string's existence provides its causal structure.
    All data has structure: runs of identical bytes.
    
    This is O(n) single-pass, producing canonical atoms directly.
    
    Program: CONST(c₁, ℓ₁), CONST(c₂, ℓ₂), ... (fused runs)
    Output: S
    
    Args:
        S: Input string
    
    Returns:
        Program with R_n(Π₀) = S in canonical form (already normalized)
    """
    n = len(S)
    atoms = []
    
    # INSTANT: Single-pass fusion (O(n), canonical output)
    i = 0
    while i < n:
        byte_val = S[i]
        run_length = 1
        
        # Count consecutive identical bytes
        while i + run_length < n and S[i + run_length] == byte_val:
            run_length += 1
        
        atoms.append(make_CONST_atom(byte_val, run_length))
        i += run_length
    
    return Prog(
        n=n,
        BODY=atoms,
        HEAD={"edition": "v3.3.8", "omega": 0x03}
    )


def Pi_0_COMPOSE_with_COPY(S: bytes, pattern: Dict) -> Prog:
    """
    Construct Π₀ using COPY pattern
    
    Program: CONST(base) + COPY(offset, length) * count
    
    Args:
        S: Input string
        pattern: Pattern dict from D3
    
    Returns:
        Program using COPY operations
    """
    n = len(S)
    atoms = []
    
    # Extract pattern info
    p = pattern["patterns"][0]
    base_length = p["length"]
    offset = p["offset"]
    
    # Write base with CONST operations
    for i in range(base_length):
        atoms.append(make_CONST_atom(S[i], 1))
    
    # Write repetitions with COPY
    pos = base_length
    while pos + base_length <= n:
        if S[pos:pos + base_length] == S[pos - offset:pos - offset + base_length]:
            atoms.append(make_COPY_atom(offset, base_length))
            pos += base_length
        else:
            # Not matching, use CONST
            atoms.append(make_CONST_atom(S[pos], 1))
            pos += 1
    
    # Handle remainder
    while pos < n:
        atoms.append(make_CONST_atom(S[pos], 1))
        pos += 1
    
    return Prog(
        n=n,
        BODY=atoms,
        HEAD={"edition": "v3.3.8", "omega": 0x03}
    )


def Pi_0_D4_XOR_AFFINE(n: int, s0: int, delta: int, xor_const: int) -> Prog:
    """
    Π₀ for D₄_XOR_AFFINE law
    
    Constructs program that generates: S[i] = ((s₀ + i·δ) mod 256) ⊕ c
    
    Strategy (Bijective CLF Boolean):
      Single D4_XOR_AFFINE atom that writes entire output atomically.
      No cursor needed - writes directly to ℓ_out like RLE_EXPLICIT.
    
    Args:
        n: String length
        s0: Affine start value
        delta: Affine delta
        xor_const: XOR constant
    
    Returns:
        Program Π₀(S) for D₄_XOR_AFFINE
    """
    # Single atom: D4_XOR_AFFINE writes XOR-affine sequence atomically
    atom = Atom("D4_XOR_AFFINE", {"s0": s0, "delta_mod": delta, "xor_const": xor_const})
    atom_inv = Atom("D4_XOR_AFFINE_INV", {"s0": s0, "delta_mod": delta, "xor_const": xor_const})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x04}
    )


def Pi_0_D5_QUADRATIC(n: int, a: int, b: int, c: int) -> Prog:
    """
    Π₀ for D₅_QUADRATIC law
    
    Constructs program that generates: S[i] = (a·i² + b·i + c) mod 256
    
    Strategy (Bijective CLF Boolean):
      Single D5_QUADRATIC atom that writes entire output atomically.
    
    Args:
        n: String length
        a: Quadratic coefficient
        b: Linear coefficient  
        c: Constant term
    
    Returns:
        Program Π₀(S) for D₅_QUADRATIC
    """
    atom = Atom("D5_QUADRATIC", {"a": a, "b": b, "c": c})
    atom_inv = Atom("D5_QUADRATIC_INV", {"a": a, "b": b, "c": c})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x05}
    )


def Pi_0_D6_LCG(n: int, seed: int, a: int, c: int) -> Prog:
    """
    Π₀ for D₆_LCG law
    
    Constructs program that generates: S[0] = seed, S[i] = (a·S[i-1] + c) mod 256
    
    Strategy (Bijective CLF Boolean):
      Single D6_LCG atom that writes entire output atomically via recurrence.
    
    Args:
        n: String length
        seed: Initial value S[0]
        a: Multiplier
        c: Increment
    
    Returns:
        Program Π₀(S) for D₆_LCG
    """
    atom = Atom("D6_LCG", {"seed": seed, "a": a, "c": c})
    atom_inv = Atom("D6_LCG_INV", {"seed": seed, "a": a, "c": c})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x06}
    )


def Pi_0_D9_COMPOSITIONAL(n: int, header_prog: 'Prog', body_prog: 'Prog') -> Prog:
    """
    Π₀ for D₉_COMPOSITIONAL law
    
    Constructs program that generates: S = concat(header, body)
    where header and body are recursively constructed.
    
    Strategy (Recursive Composition):
      Single D9_COMPOSITIONAL atom containing sub-programs.
    
    Args:
        n: Total string length
        header_prog: Program generating header segment
        body_prog: Program generating body segment
    
    Returns:
        Program Π₀(S) for D₉_COMPOSITIONAL
    """
    atom = Atom("D9_COMPOSITIONAL", {
        "header_prog": header_prog,
        "body_prog": body_prog
    })
    atom_inv = Atom("D9_COMPOSITIONAL_INV", {
        "header_prog": header_prog,
        "body_prog": body_prog
    })
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x09}
    )


def Pi_0_D10_DICTIONARY(n: int, dictionary: list, indices: list) -> Prog:
    """
    Π₀ for D₁₀_DICTIONARY law
    
    Constructs program that generates: S[i] = D[I[i]]
    where D = dictionary, I = index sequence.
    
    Strategy (Symbol Table):
      Single D10_DICTIONARY atom containing dictionary and indices.
    
    Args:
        n: Total string length
        dictionary: List of unique symbols
        indices: List of dictionary indices
    
    Returns:
        Program Π₀(S) for D₁₀_DICTIONARY
    """
    atom = Atom("D10_DICTIONARY", {
        "dictionary": dictionary,
        "indices": indices,
        "dict_size": len(dictionary)
    })
    atom_inv = Atom("D10_DICTIONARY_INV", {
        "dictionary": dictionary,
        "indices": indices,
        "dict_size": len(dictionary)
    })
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return Prog(
        n=n,
        BODY=[atom],
        HEAD={"edition": "v3.3.8", "omega": 0x0A}
    )


# ============================================================================
# Canonical Π₀ Construction (with selection)
# ============================================================================

def Pi_0(S: bytes, theta_params: Optional[Dict] = None) -> Prog:
    """
    Π₀ : Dₙ → Prog(n) (total function)
    
    Canonical program construction from S using strict theta recognition.
    
    Args:
        S: Input string (S ∈ Dₙ)
        theta_params: Optional pre-computed θ(S) (if None, will compute)
    
    Returns:
        Program Π₀(S) such that R_n(Π₀(S)) = S
    """
    n = len(S)
    
    # Use strict theta recognition
    from M4_recognition_STRICT import theta_strict
    
    if theta_params is None:
        result = theta_strict(S)
        family = result['family']
        params = result['params']
    else:
        # Direct format
        family = theta_params.get('family')
        params = theta_params.get('params', {})
    
    # Dispatch to appropriate constructor
    if family == 'D1':
        return Pi_0_RLE_SHORT(n)
    
    elif family == 'D2':
        return Pi_0_RLE_EXPLICIT(n, params['s0'], params['delta'])
    
    elif family == 'D3':
        return Pi_0_COMPOSE_with_COPY(S, params)
    
    elif family == 'D4_XOR_AFFINE':
        return Pi_0_D4_XOR_AFFINE(n, params['base_s0'], params['base_delta'], params['xor_const'])
    
    elif family == 'D5_QUADRATIC':
        return Pi_0_D5_QUADRATIC(n, params['a'], params['b'], params['c'])
    
    elif family == 'D6_LCG':
        return Pi_0_D6_LCG(n, params['seed'], params['a'], params['c'])
    
    elif family == 'D9_COMPOSITIONAL':
        # Recursively construct header and body
        header_len = params['header_length']
        header = S[:header_len]
        body = S[header_len:]
        
        header_prog = Pi_0(header)  # Recursive
        body_prog = Pi_0(body)      # Recursive
        
        return Pi_0_D9_COMPOSITIONAL(n, header_prog, body_prog)
    
    elif family == 'D10_DICTIONARY':
        return Pi_0_D10_DICTIONARY(n, params['dictionary'], params['indices'])
    
    else:
        # Per-byte CONST construction
        return Pi_0_COMPOSE_per_byte(S)


# ============================================================================
# Verification Helpers
# ============================================================================

def verify_construction(S: bytes, P: Prog) -> bool:
    """
    Verify: R_n(P) = S
    
    Check that constructed program replays to original string.
    
    Args:
        S: Original string
        P: Constructed program
    
    Returns:
        True if R_n(P) = S
    """
    from M3_tau_pure import R_n_pure as R_n
    
    S_replayed = R_n(P)
    return S_replayed == S


# ============================================================================
# Module Metadata
# ============================================================================

__all__ = [
    # Atom constructors
    'make_RLE_SHORT_atom',
    'make_RLE_EXPLICIT_atom',
    'make_CONST_atom',
    'make_COPY_atom',
    'make_XOR_CONST_atom',
    
    # Program constructors
    'Pi_0_RLE_SHORT',
    'Pi_0_RLE_EXPLICIT',
    'Pi_0_COMPOSE_per_byte',
    'Pi_0_COMPOSE_with_COPY',
    
    # Canonical construction
    'Pi_0',
    
    # Verification
    'verify_construction',
]
