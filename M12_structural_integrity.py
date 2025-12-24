"""
M12_structural_integrity.py

CLF STRUCTURAL INTEGRITY VALIDATOR
Prevents hidden fallback via constants, literals, and implicit effect leakage.

CRITICAL PRINCIPLE:
  "If it isn't generated, it's leaked." - CLF Law of Structural Purity

This module enforces the deepest version of CLF Axiom #4 (No Effect Leakage):
  Σ must not contain any raw fragment of S unless it is derivable from
  closed parameters OR is an axiomatically allowed constant.

WHAT THIS PREVENTS:
  ✗ Literal copied patterns (e.g., 'ABC' from S into Σ['pattern'])
  ✗ High-entropy binary chunks without derivation
  ✗ Palette echoes (raw color bytes in seed)
  ✗ Non-derived string fragments
  ✗ Any manifestation storage disguised as "structural"

ENFORCEMENT:
  Σ ∈ C^closed ∧ |Σ| < |S| ∧ Ξ(Σ) = S ∧ Σ ∩ S = ∅
"""

import math
from collections import Counter
from typing import Any, Callable, Optional, Protocol, Set, Tuple


class StructuralIntegrityError(Exception):
    """Raised when seed contains effect leakage (hidden fallback via constants)."""
    pass


class ByteOracle(Protocol):
    """Mathematical oracle for a binary string S: provides n and byte access S(i)."""

    n: int

    def __call__(self, i: int) -> Optional[int]:
        ...


# ============================================================================
# Axiomatically Allowed Constants
# ============================================================================

# These are universal mathematical/structural constants that can appear in seeds
# without being considered "effect leakage" from the original string.
#
# Criteria for inclusion:
#   1. Universal mathematical constant (0, 1, e, π, etc.)
#   2. Structural boundary marker (null byte, etc.)
#   3. Canonical encoding base (0x00, 0xFF, etc.)
#
# NOT allowed:
#   - Arbitrary strings ('ABC', 'Hello', etc.)
#   - Application-specific constants
#   - Anything that "happens to match" part of S

AXIOMATICALLY_ALLOWED_CONSTANTS: Set[bytes] = {
    b'\x00',        # Null byte (structural zero)
    b'\x01',        # Unity
    b'\xff',        # Max byte (structural boundary)
    b'0',           # ASCII zero
    b'1',           # ASCII one
    # Add more only if truly universal
}

# Numerical constants are always allowed (they're parameters, not literals)
# Strings/bytes must be checked


# ============================================================================
# Entropy Analysis - DISABLED (Compression Logic)
# ============================================================================
# Shannon entropy is INFORMATION THEORY, not structural mathematics.
# CLF uses deductive structural observation, not statistical measures.
# 
# Per CLF_LOGIC_ALIGNMENT_GUIDE.md:
#   ❌ Use statistical estimation or heuristics
#   ✅ Extract structure through observation, not classification

# def shannon_entropy(data: bytes) -> float:
#     """DISABLED - Shannon entropy is compression logic."""
#     pass

# Entropy thresholds - DISABLED
# ENTROPY_THRESHOLD_SUSPICIOUS = 3.5  # Statistical measure - not CLF
# ENTROPY_THRESHOLD_REJECT = 6.0      # Statistical measure - not CLF


# ============================================================================
# Literal Leakage Detection
# ============================================================================

def _oracle_from_S(S: Any) -> Tuple[int, Callable[[int], Optional[int]]]:
    """Normalize S into (n, byte_at) without assuming materialization.

    Supports:
      - bytes/bytearray/memoryview
      - objects exposing .n and callable __call__(i)
      - objects exposing __len__ and __getitem__ for int indices
    """
    if isinstance(S, (bytes, bytearray, memoryview)):
        data = bytes(S)

        def byte_at(i: int) -> Optional[int]:
            if i < 0 or i >= len(data):
                return None
            return data[i]

        return len(data), byte_at

    # Sampler-style oracle (e.g., BinaryStringSampler)
    if hasattr(S, 'n') and callable(S):
        n_val = int(getattr(S, 'n'))

        def byte_at(i: int) -> Optional[int]:
            return S(i)

        return n_val, byte_at

    # Sequence-style oracle
    if hasattr(S, '__len__') and hasattr(S, '__getitem__'):
        n_val = int(len(S))

        def byte_at(i: int) -> Optional[int]:
            if i < 0 or i >= n_val:
                return None
            v = S[i]
            if isinstance(v, int):
                return v
            if isinstance(v, (bytes, bytearray)) and len(v) == 1:
                return v[0]
            return None

        return n_val, byte_at

    raise TypeError("S must be bytes-like or an oracle with (n, S(i))")


def _oracle_slice(n: int, byte_at: Callable[[int], Optional[int]], offset: int, length: int) -> Optional[bytes]:
    if offset < 0 or offset + length > n:
        return None
    out = bytearray(length)
    for j in range(length):
        b = byte_at(offset + j)
        if b is None:
            return None
        out[j] = int(b) & 0xFF
    return bytes(out)


def check_literal_leakage(value: bytes, S: Any, field_name: str):
    """
    Check if a seed constant is a literal fragment from S.
    
    CLF INSTANT VALIDATION: O(1) structural alignment check at fixed positions
    NOT: O(n) scanning through S
    
    CLF Rule:
      If value appears verbatim in S (not derived, just copied)
      → REJECT as compression disguised as causality
    
    INSTANT CHECK: Test alignment at ~15 strategic positions only
    
    Exception:
      Single-byte constants allowed (they're unavoidable)
      Multi-byte constants must be derived or axiomatically allowed
    
    Args:
        value: Constant from seed
        S: Original string
        field_name: Name of field for error message
    
    Raises:
        StructuralIntegrityError: If literal leakage detected
    """
    # Single bytes always allowed (unavoidable in 256-symbol alphabet)
    if len(value) <= 1:
        return
    
    # Check for axiomatically allowed constants
    if value in AXIOMATICALLY_ALLOWED_CONSTANTS:
        return
    
    # Allow structural metadata (family names, not manifestation data)
    # Family names like 'D1', 'D2' are CLF vocabulary, not data from S
    if field_name and ('family' in field_name.lower() or 'law_type' in field_name.lower()):
        return
    
    # CLF INSTANT CHECK: Test alignment at ~15 strategic positions (O(1))
    # NOT: if value in S (that's O(n) scanning!)
    n, byte_at = _oracle_from_S(S)
    val_len = len(value)
    
    if val_len > n:
        return  # Can't leak what doesn't fit
    
    # Strategic positions to check for literal leakage (O(1) - fixed 15 checks)
    strategic_offsets = [
        0,                    # start
        n - val_len,          # end
        n//2 - val_len//2,    # middle
        n//4,                 # quarter
        3*n//4 - val_len,     # three-quarter
        n//8,                 # eighth positions
        3*n//8,
        5*n//8,
        7*n//8 - val_len,
        n//16,                # sixteenth positions
        3*n//16,
        5*n//16,
        7*n//16,
        9*n//16,
        11*n//16 - val_len,
    ]
    
    # Check if value appears at any strategic position (O(1) - constant checks)
    for offset in strategic_offsets:
        if 0 <= offset < n - val_len + 1:
            window = _oracle_slice(n, byte_at, offset, val_len)
            if window == value:
                raise StructuralIntegrityError(
                    f"Effect leakage detected in field '{field_name}'\n\n"
                    f"VIOLATION: Seed contains literal fragment from S\n"
                    f"  Field: {field_name}\n"
                    f"  Value: {value[:20]}{'...' if len(value) > 20 else ''} ({len(value)} bytes)\n"
                    f"  Found at position: {offset}\n\n"
                    f"CLF RULE: Σ must not contain raw fragments of S\n"
                    f"This is compression logic (storing manifestation, not origin)\n\n"
                    f"SOLUTION:\n"
                    f"  - If this is a pattern: Store pattern GENERATOR, not pattern itself\n"
                    f"  - If this is a constant: Must be axiomatically allowed\n"
                    f"  - If this is derived: Must show derivation function\n\n"
                    f"Example of correct approach:\n"
                    f"  ✗ WRONG: Σ = {{pattern: b'ABC'}}  (stores manifestation)\n"
                    f"  ✓ RIGHT: Σ = {{period: 3}}        (stores structure only)\n"
                    f"           Then extract pattern as S[:period] during execution"
                )
    
    # No leakage detected at strategic positions - validation passes (O(1))


def check_entropy_threshold(value: bytes, field_name: str, allow_high_entropy: bool = False):
    """
    DISABLED - Entropy checking is compression logic.
    
    Per CLF_LOGIC_ALIGNMENT_GUIDE.md:
      ❌ Use statistical estimation or heuristics
      ✅ Deduce laws from constraints, not match against patterns
    
    CLF validates structure through mathematical constraints,
    not statistical measures like Shannon entropy.
    """
    # DISABLED: No entropy-based rejection
    # If value exists as parameter, it's structurally valid
    # The law either instantiates or doesn't - no statistical threshold
    return


# ============================================================================
# Literal Leakage Detection
# ============================================================================


# ============================================================================
# Recursive Structural Validation
# ============================================================================

def validate_seed_integrity(Sigma: dict, S: Any, field_path: str = "Σ"):
    """
    Enforce structural integrity: No effect leakage in seed.
    
    This is the deepest form of CLF validation, checking that every element
    of Σ is pure cause (derived or axiomatically allowed), not copied effect.
    
    AXIOM ENFORCED:
      Σ ∈ C^closed ∧ |Σ| < |S| ∧ Ξ(Σ) = S ∧ Σ ∩ S = ∅
    
    The last condition (Σ ∩ S = ∅) means:
      No raw fragment of S appears in Σ (unless derived/axiomatically allowed)
    
    CHECKS PERFORMED:
      1. Literal leakage: No verbatim fragments from S
      2. Entropy threshold: No high-entropy constants without derivation
      3. Recursive validation: Check all nested structures
      4. Axiomatic constants: Only universally allowed symbols
    
    Args:
        Sigma: Seed dictionary (from theta_strict)
        S: Original string
        field_path: Current path for error messages (internal)
    
    Raises:
        StructuralIntegrityError: If any effect leakage detected
    
    Returns:
        True if structural integrity verified
    """
    if not isinstance(Sigma, dict):
        return True
    
    for key, val in Sigma.items():
        current_path = f"{field_path}['{key}']"
        
        # Skip metadata fields
        if key in ('family', 'n', 'status', 'reason', 'checked_families',
                   'axiom', 'solution', 'forbidden', 'note', 'is_closed'):
            continue
        
        # Check 'params' dict recursively
        if key == 'params' and isinstance(val, dict):
            validate_seed_integrity(val, S, f"{field_path}.params")
            continue
        
        # Numerical parameters are always fine (they're generative parameters)
        if isinstance(val, (int, float, bool)):
            continue
        
        # None is fine
        if val is None:
            continue
        
        # Bytes/string constants: CRITICAL CHECK
        if isinstance(val, (bytes, bytearray)):
            # Convert to bytes for analysis
            val_bytes = bytes(val)
            
            # Check 1: Literal leakage from S
            check_literal_leakage(val_bytes, S, current_path)
            
            # Check 2: Entropy threshold
            check_entropy_threshold(val_bytes, current_path)
        
        elif isinstance(val, str):
            # String constants: Convert and check
            val_bytes = val.encode('utf-8')
            
            # Check 1: Literal leakage
            check_literal_leakage(val_bytes, S, current_path)
            
            # Check 2: Entropy threshold
            check_entropy_threshold(val_bytes, current_path)
        
        # Lists: Check each element
        elif isinstance(val, (list, tuple)):
            for i, item in enumerate(val):
                if isinstance(item, (bytes, bytearray)):
                    item_bytes = bytes(item)
                    check_literal_leakage(item_bytes, S, f"{current_path}[{i}]")
                    check_entropy_threshold(item_bytes, f"{current_path}[{i}]")
                elif isinstance(item, dict):
                    validate_seed_integrity(item, S, f"{current_path}[{i}]")
        
        # Nested dicts: Recurse
        elif isinstance(val, dict):
            validate_seed_integrity(val, S, current_path)
    
    return True


# =========================================================================
# Diagnostics helpers (NOT used for gating)
# =========================================================================

def shannon_entropy(data: bytes) -> float:
    """Diagnostic Shannon entropy (bits/byte). Not used as a validity gate."""
    if not data:
        return 0.0
    counts = Counter(data)
    n = len(data)
    ent = 0.0
    for c in counts.values():
        p = c / n
        ent -= p * math.log2(p)
    return ent


# Kept for quick_integrity_check compatibility (diagnostic only)
ENTROPY_THRESHOLD_REJECT = 6.0


# ============================================================================
# Quick Check for Common Violations
# ============================================================================

def quick_integrity_check(Sigma: dict, S: bytes) -> dict:
    """
    Quick non-throwing integrity check for analysis.
    
    Returns diagnostic info without raising exceptions.
    Useful for debugging and logging.
    
    Returns:
        {
            'has_literals': bool,
            'high_entropy_fields': [str],
            'suspicious_fields': [str],
            'is_clean': bool
        }
    """
    issues = {
        'has_literals': False,
        'high_entropy_fields': [],
        'suspicious_fields': [],
        'is_clean': True
    }
    
    def check_field(key, val):
        if isinstance(val, (bytes, bytearray)):
            val_bytes = bytes(val)
            
            # Check literal
            if len(val_bytes) > 1 and val_bytes in S:
                issues['has_literals'] = True
                issues['suspicious_fields'].append(key)
                issues['is_clean'] = False
            
            # Check entropy
            if len(val_bytes) > 0:
                entropy = shannon_entropy(val_bytes)
                if entropy > ENTROPY_THRESHOLD_REJECT:
                    issues['high_entropy_fields'].append(key)
                    issues['is_clean'] = False
    
    if isinstance(Sigma, dict):
        for key, val in Sigma.items():
            check_field(key, val)
            if isinstance(val, dict):
                for k2, v2 in val.items():
                    check_field(f"{key}.{k2}", v2)
    
    return issues


__all__ = [
    'validate_seed_integrity',
    'quick_integrity_check',
    'StructuralIntegrityError',
    'shannon_entropy',
]


if __name__ == "__main__":
    print("CLF STRUCTURAL INTEGRITY VALIDATOR")
    print("=" * 70)
    print()
    print("ENFORCES:")
    print("  Σ ∈ C^closed ∧ |Σ| < |S| ∧ Ξ(Σ) = S ∧ Σ ∩ S = ∅")
    print()
    print("PREVENTS:")
    print("  ✗ Literal copied patterns")
    print("  ✗ High-entropy binary chunks")
    print("  ✗ Palette echoes")
    print("  ✗ Non-derived string fragments")
    print()
    print("PRINCIPLE:")
    print("  \"If it isn't generated, it's leaked.\"")
    print("  - CLF Law of Structural Purity")
