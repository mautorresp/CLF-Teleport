#!/usr/bin/env python3
"""
CLF Governance Module — Causal Closure, Field Purity, Determinism

Implements:
1. Platform determinism validation
2. Closed-mode enforcement (destructive actions gated by causal proof)
3. Field-pure family validation
4. Seed stamping and vault integration
5. Safe decoder bounds

All boundaries are ontological (derived from causal structure), never heuristic.
"""

import sys
import hashlib
import os
from typing import Dict, Any, Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. FIELD-PURE FAMILIES
# ═══════════════════════════════════════════════════════════════════════════

# Only mathematically pure families permitted in closed mode
VALID_FAMILIES_CLOSED = {
    "D1",  # D1_CONST
    "D2",  # D2_AFFINE_CONSTANT_DELTA
    "D3",  # D3_PERIODIC (if implemented)
    "D9",  # D9_LIMIT_CAUSAL_CLOSURE
    "D9_RADIAL",  # Legacy name for D9_LIMIT_CAUSAL_CLOSURE
}


def validate_family(family: str, mode: str = "closed") -> bool:
    """
    Validate that family is field-pure (permitted in closed mode).
    
    Returns:
        True if family is valid for the given mode
    
    Raises:
        ValueError if family is not permitted in closed mode
    """
    if mode == "closed":
        if family not in VALID_FAMILIES_CLOSED:
            raise ValueError(
                f"Family '{family}' is not permitted in closed mode. "
                f"Only field-pure families allowed: {VALID_FAMILIES_CLOSED}"
            )
    return True


# ═══════════════════════════════════════════════════════════════════════════
# 2. PLATFORM DETERMINISM
# ═══════════════════════════════════════════════════════════════════════════

# Canonical SHA-256 of bytes(range(256))
# This is the universal reference for ℤ₂₅₆ integrity
CANONICAL_Z256_HASH = "40aff2e9d2d8922e47afd4648e6967497158785fbd1da870e7110266bf944880"


def test_platform_determinism() -> bool:
    """
    Verify platform arithmetic is compatible with CLF field closure.
    
    Tests:
    1. Endianness (must be little-endian for compatibility)
    2. Integer overflow (mod 256 must wrap correctly)
    3. Hash determinism (SHA-256 must match canonical)
    
    Returns:
        True if platform is deterministic
        
    Raises:
        RuntimeError if platform determinism fails
    """
    errors = []
    
    # Test 1: Endianness
    if sys.byteorder != "little":
        errors.append(f"Endianness: expected 'little', got '{sys.byteorder}'")
    
    # Test 2: Integer overflow behavior
    overflow_test = ((255 + 1) % 256 == 0)
    if not overflow_test:
        errors.append(f"Integer overflow: (255 + 1) % 256 != 0")
    
    # Test 3: Hash determinism
    test_bytes = bytes(range(256))
    computed_hash = hashlib.sha256(test_bytes).hexdigest()
    if computed_hash != CANONICAL_Z256_HASH:
        errors.append(
            f"Hash determinism: SHA-256(ℤ₂₅₆) mismatch\n"
            f"  Expected: {CANONICAL_Z256_HASH}\n"
            f"  Got:      {computed_hash}"
        )
    
    if errors:
        error_msg = "Platform determinism failed:\n" + "\n".join(f"  - {e}" for e in errors)
        raise RuntimeError(error_msg)
    
    return True


# ═══════════════════════════════════════════════════════════════════════════
# 3. SEED STAMPING AND VAULT
# ═══════════════════════════════════════════════════════════════════════════

def stamp_seed(Sigma: Dict[str, Any]) -> str:
    """
    Compute deterministic cryptographic address for seed Σ.
    
    Address is SHA-256 of normalized wire format.
    This creates content-addressable seed storage.
    
    Args:
        Sigma: Seed structure (causal law representation)
        
    Returns:
        64-character hex string (SHA-256 hash)
    """
    # Normalize to wire format (deterministic serialization)
    # For now, use string representation (TODO: proper wire format)
    import json
    Sigma_wire = json.dumps(Sigma, sort_keys=True).encode('utf-8')
    
    # Compute SHA-256 address
    addr = hashlib.sha256(Sigma_wire).hexdigest()
    return addr


def save_seed_vault(Sigma: Dict[str, Any], vault_path: str) -> str:
    """
    Save seed to immutable vault (content-addressable storage).
    
    Seeds are stored by their cryptographic address.
    Duplicate seeds are automatically deduplicated.
    
    Args:
        Sigma: Seed structure to save
        vault_path: Directory path for seed vault
        
    Returns:
        SHA-256 address of saved seed
    """
    # Ensure vault directory exists
    os.makedirs(vault_path, exist_ok=True)
    
    # Compute address
    addr = stamp_seed(Sigma)
    
    # Save to vault (if not already present)
    seed_file = os.path.join(vault_path, f"{addr}.seed")
    if not os.path.exists(seed_file):
        import json
        Sigma_wire = json.dumps(Sigma, sort_keys=True, indent=2)
        with open(seed_file, 'w') as f:
            f.write(Sigma_wire)
    
    return addr


def load_seed_vault(addr: str, vault_path: str) -> Optional[Dict[str, Any]]:
    """
    Load seed from vault by address.
    
    Args:
        addr: SHA-256 address (64-char hex)
        vault_path: Directory path for seed vault
        
    Returns:
        Seed structure if found, None otherwise
    """
    seed_file = os.path.join(vault_path, f"{addr}.seed")
    if not os.path.exists(seed_file):
        return None
    
    import json
    with open(seed_file, 'r') as f:
        Sigma = json.load(f)
    
    # Verify address matches
    computed_addr = stamp_seed(Sigma)
    if computed_addr != addr:
        raise ValueError(f"Seed address mismatch: expected {addr}, got {computed_addr}")
    
    return Sigma


# ═══════════════════════════════════════════════════════════════════════════
# 4. CLOSED MODE ENFORCEMENT
# ═══════════════════════════════════════════════════════════════════════════

def validate_closed_mode(nu_P: int, nu_CLF: int, sha_match: bool) -> bool:
    """
    Validate that causal equivalence is proven before allowing destructive actions.
    
    Closed mode requires:
    - ν_P = 0 (grid-level bijection)
    - ν_CLF = 0 (field-level equivalence)
    - SHA-256 match (cryptographic confirmation)
    
    Args:
        nu_P: Grid-level hash residual
        nu_CLF: Field-level hash residual
        sha_match: SHA-256 match status
        
    Returns:
        True if all conditions pass
        
    Raises:
        ValueError if any condition fails
    """
    errors = []
    
    if nu_P != 0:
        errors.append(f"Grid-level bijection failed: ν_P = {nu_P} (expected 0)")
    
    if nu_CLF != 0:
        errors.append(f"Field-level equivalence failed: ν_CLF = {nu_CLF} (expected 0)")
    
    if not sha_match:
        errors.append(f"Cryptographic verification failed: SHA-256 mismatch")
    
    if errors:
        error_msg = "Closed mode validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        raise ValueError(error_msg)
    
    return True


# ═══════════════════════════════════════════════════════════════════════════
# 5. SAFE DECODER BOUNDS
# ═══════════════════════════════════════════════════════════════════════════

def safe_varint_decode(stream) -> int:
    """
    Decode variable-length integer with field-ontological bounds.
    
    Bounds are derived from field structure (64-bit domain = 8 bytes max),
    not from arbitrary configuration limits.
    
    Args:
        stream: Iterable of bytes
        
    Returns:
        Decoded integer value
        
    Raises:
        ValueError if varint exceeds causal domain
    """
    val = 0
    shift = 0
    
    for b in stream:
        val |= (b & 0x7F) << shift
        
        # If high bit not set, this is the last byte
        if b < 0x80:
            return val
        
        shift += 7
        
        # Field-ontological bound: 8 bytes = 56 bits of shift
        # Beyond this exceeds ℤ₂⁶⁴ domain
        if shift > 56:
            raise ValueError(
                "Varint exceeds causal domain (>64 bits). "
                "This is a field-ontological bound, not a heuristic limit."
            )
    
    raise ValueError("Varint truncated: no terminating byte")


# ═══════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

def initialize_clf_governance():
    """
    Initialize CLF governance system.
    
    Must be called before any causal operations.
    Validates platform determinism and sets up governance.
    """
    print("CLF Governance: Initializing...")
    
    # Test platform determinism
    try:
        test_platform_determinism()
        print("  ✅ Platform determinism verified")
        print(f"     - Endianness: {sys.byteorder}")
        print(f"     - Integer wrap: ℤ₂₅₆ compatible")
        print(f"     - Hash determinism: SHA-256 canonical")
    except RuntimeError as e:
        print(f"  ❌ Platform determinism failed")
        raise
    
    print("CLF Governance: Ready")
    print()


if __name__ == '__main__':
    # Test governance initialization
    initialize_clf_governance()
    
    # Test family validation
    print("Testing family validation:")
    for family in ["D1", "D2", "D9", "INVALID"]:
        try:
            validate_family(family)
            print(f"  ✅ {family}: valid")
        except ValueError as e:
            print(f"  ❌ {family}: {e}")
    
    print()
    
    # Test seed stamping
    print("Testing seed stamping:")
    test_seed = {"family": "D1", "params": {"c": 42}}
    addr = stamp_seed(test_seed)
    print(f"  Seed address: {addr}")
    
    print()
    
    # Test closed mode validation
    print("Testing closed mode validation:")
    try:
        validate_closed_mode(0, 0, True)
        print("  ✅ All checks pass: closed mode permitted")
    except ValueError as e:
        print(f"  ❌ {e}")
    
    try:
        validate_closed_mode(1, 0, True)
        print("  ✅ Closed mode permitted (should not reach here)")
    except ValueError as e:
        print(f"  ✅ Correctly rejected: {e.args[0].split(':')[0]}")
