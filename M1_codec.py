"""
M1_codec.py - Wire Format Bijection Layer
CLF 2.txt Section 5: Codec, canonical seeds, replay

Implements SDL_ω encoding/decoding (bijective, prefix-free)
Pure mathematical bijection: bytes ↔ wire tokens

Key principle: Both directions (encode/decode) are equally fundamental.
This is not "compression/decompression" but bijective coordinate transformation.
"""

from typing import Tuple, Optional
import hashlib

# ============================================================================
# SDL Primitives: Γ̃ (Gamma Plus One) Encoding
# ============================================================================

def encode_gamma(y: int) -> bytes:
    """
    Encode y as Γ̃(y) - byte-aligned Elias gamma.
    
    CLF 2.txt Section 5: SDL_ω is bijective & prefix-free
    
    Args:
        y: Integer >= 1
    
    Returns:
        Byte-aligned gamma encoding
    
    Mathematical definition:
        k = ⌊log₂(y)⌋
        bits = '0'*k + bin(y)[2:]  # k zeros + binary representation
        Pad to byte boundary with trailing zeros
    """
    if y < 1:
        raise ValueError(f"gamma encoding requires y >= 1, got {y}")
    
    k = y.bit_length() - 1
    bits = '0' * k + format(y, f'0{k+1}b')
    
    # Pad to byte boundary
    pad = (8 - (len(bits) % 8)) % 8
    bits += '0' * pad
    
    return int(bits, 2).to_bytes(len(bits) // 8, 'big')


def decode_gamma(stream: bytes, pos: int) -> Tuple[int, int]:
    """
    Recognize Γ̃(y) from wire stream at position pos.
    
    CLF 2.txt Section 0: "decoders total, locally decidable"
    
    Args:
        stream: Wire format bytes
        pos: Starting position
    
    Returns:
        (y, bytes_consumed)
    
    Mathematical recognition (not sequential scan):
        Count leading zeros → k
        Read k+1 bits → y
        Verify padding zeros
    """
    if pos >= len(stream):
        raise ValueError("decode_gamma: insufficient bytes")
    
    # Count leading zeros (determines k)
    z = 0
    bit_pos = 0
    
    while True:
        byte_idx = pos + (bit_pos // 8)
        if byte_idx >= len(stream):
            raise ValueError("decode_gamma: malformed stream")
        
        b = stream[byte_idx]
        bit = (b >> (7 - (bit_pos % 8))) & 1
        bit_pos += 1
        
        if bit == 0:
            z += 1
        else:
            break
    
    # Read remaining z bits
    y = 1
    for _ in range(z):
        byte_idx = pos + (bit_pos // 8)
        if byte_idx >= len(stream):
            raise ValueError("decode_gamma: malformed stream")
        
        b = stream[byte_idx]
        bit = (b >> (7 - (bit_pos % 8))) & 1
        bit_pos += 1
        y = (y << 1) | bit
    
    # Verify padding
    pad = (8 - (bit_pos % 8)) % 8
    for _ in range(pad):
        byte_idx = pos + (bit_pos // 8)
        if byte_idx >= len(stream):
            raise ValueError("decode_gamma: malformed stream")
        
        b = stream[byte_idx]
        bit = (b >> (7 - (bit_pos % 8))) & 1
        bit_pos += 1
        
        if bit != 0:
            raise ValueError("decode_gamma: invalid padding")
    
    bytes_used = bit_pos // 8
    return (y, bytes_used)


def Lgamma(y: int) -> int:
    """
    Compute 𝓁̃_γ(y): byte-aligned gamma length in bits.
    
    CLF 2.txt Section 6.1: 𝓁̃_γ(y) = 8·⌈ℓ_γ(y)/8⌉
    where ℓ_γ(y) = 2⌊log₂y⌋ + 1
    
    Args:
        y: Integer >= 1
    
    Returns:
        Length in bits (multiple of 8)
    """
    if y < 1:
        raise ValueError(f"Lgamma requires y >= 1, got {y}")
    
    k = y.bit_length() - 1
    ell_gamma = 2 * k + 1
    return 8 * ((ell_gamma + 7) // 8)


# ============================================================================
# Wire Structure: HEAD, COMMIT
# ============================================================================

# Sentinel bytes
OMEGA_SENTINEL = 0x14  # HEAD marker
COMMIT_SENTINEL = 0x15  # COMMIT marker

# Family identifiers
OMEGA_RAW = 0x00       # RAW family (direct byte storage)
OMEGA_RLE = 0x01
OMEGA_COMPOSE = 0x03
OMEGA_D4_XOR_AFFINE = 0x04
OMEGA_D5_QUADRATIC = 0x05
OMEGA_D6_LCG = 0x06
OMEGA_D9_COMPOSITIONAL = 0x09
OMEGA_D10_DICTIONARY = 0x0A


def encode_HEAD(omega: int) -> bytes:
    """
    Encode HEAD: [0x14][ω]
    
    CLF 2.txt Section 5: "HEAD carries edition/codec IDs"
    
    Args:
        omega: Family selector (0x01=RLE, 0x03=COMPOSE, 0x04=D4_XOR_AFFINE)
    
    Returns:
        2-byte HEAD
    """
    return bytes([OMEGA_SENTINEL, omega])


def decode_HEAD(stream: bytes, pos: int) -> Tuple[int, int]:
    """
    Recognize HEAD structure from wire.
    
    Returns:
        (omega, new_position)
    """
    if pos + 1 >= len(stream):
        raise ValueError("decode_HEAD: insufficient bytes")
    
    if stream[pos] != OMEGA_SENTINEL:
        raise ValueError(f"decode_HEAD: expected 0x14, got 0x{stream[pos]:02x}")
    
    omega = stream[pos + 1]
    
    if omega not in [OMEGA_RAW, OMEGA_RLE, OMEGA_COMPOSE, OMEGA_D4_XOR_AFFINE, OMEGA_D5_QUADRATIC, OMEGA_D6_LCG]:
        raise ValueError(f"decode_HEAD: unknown family 0x{omega:02x}")
    
    return (omega, pos + 2)


def encode_COMMIT(digest: bytes) -> bytes:
    """
    Encode COMMIT: [0x15][SHA-256(S)]
    
    CLF 2.txt Section 5: Optional witness
    
    Args:
        digest: 32-byte SHA-256 hash
    
    Returns:
        33-byte COMMIT structure
    """
    if len(digest) != 32:
        raise ValueError(f"COMMIT requires 32-byte digest, got {len(digest)}")
    
    return bytes([COMMIT_SENTINEL]) + digest


def decode_COMMIT(stream: bytes, pos: int) -> Tuple[bool, Optional[bytes], int]:
    """
    Recognize optional COMMIT structure.
    
    Returns:
        (has_commit, digest, new_position)
    """
    if pos >= len(stream):
        return (False, None, pos)
    
    if stream[pos] != COMMIT_SENTINEL:
        return (False, None, pos)
    
    if pos + 33 > len(stream):
        raise ValueError("decode_COMMIT: insufficient bytes for digest")
    
    digest = stream[pos + 1:pos + 33]
    return (True, digest, pos + 33)


def sha256(data: bytes) -> bytes:
    """Compute SHA-256 digest (32 bytes)"""
    return hashlib.sha256(data).digest()


# ============================================================================
# Modular Arithmetic Primitives (ℤ₂₅₆)
# ============================================================================

def add256(a: int, b: int) -> int:
    """Addition modulo 256"""
    return (a + b) % 256


def mul256(a: int, b: int) -> int:
    """Multiplication modulo 256"""
    return (a * b) % 256


def xor8(a: int, b: int) -> int:
    """Bitwise XOR on 8-bit bytes"""
    return a ^ b


# ============================================================================
# Full Codec: Enc_n / Dec_n
# (Will be completed after M2_types defines Prog)
# ============================================================================

def encode_body_prefix(n: int) -> bytes:
    """
    Encode BODY prefix: Γ̃(n+1)
    
    Every program begins with arity declaration.
    
    Args:
        n: Arity (string length)
    
    Returns:
        Encoded prefix
    """
    return encode_gamma(n + 1)


def decode_body_prefix(stream: bytes, pos: int) -> Tuple[int, int]:
    """
    Recognize BODY prefix: Γ̃(n+1)
    
    Returns:
        (n, new_position)
    """
    y, consumed = decode_gamma(stream, pos)
    
    if y < 1:
        raise ValueError("decode_body_prefix: invalid arity")
    
    n = y - 1
    return (n, pos + consumed)


# ============================================================================
# Wire Format Verification
# ============================================================================

def verify_canonical_end(stream: bytes, pos: int):
    """
    Verify no trailing bytes (canonical end).
    
    CLF 2.txt Section 5: "canonical end forbids trailers"
    """
    if pos != len(stream):
        raise ValueError(f"verify_canonical_end: {len(stream) - pos} trailing bytes")


def verify_commit_witness(S: bytes, digest: bytes):
    """
    Verify COMMIT witness matches string.
    
    Args:
        S: Original string
        digest: Claimed SHA-256 hash
    """
    computed = sha256(S)
    if computed != digest:
        raise ValueError("verify_commit_witness: digest mismatch")


# ============================================================================
# Cost Calculations
# ============================================================================

def cost_HEAD() -> int:
    """Cost of HEAD in bits (always 16)"""
    return 16


def cost_COMMIT() -> int:
    """Cost of COMMIT in bits (always 8 + 256 = 264)"""
    return 8 + 256


def wire_length_overhead() -> int:
    """Fixed overhead: HEAD only (COMMIT optional)"""
    return cost_HEAD()


# ============================================================================
# Module Metadata
# ============================================================================

__all__ = [
    # Gamma encoding
    'encode_gamma',
    'decode_gamma',
    'Lgamma',
    
    # Wire structure
    'encode_HEAD',
    'decode_HEAD',
    'encode_COMMIT',
    'decode_COMMIT',
    'encode_body_prefix',
    'decode_body_prefix',
    
    # Verification
    'verify_canonical_end',
    'verify_commit_witness',
    'sha256',
    
    # Arithmetic
    'add256',
    'mul256',
    'xor8',
    
    # Cost
    'Lgamma',
    'cost_HEAD',
    'cost_COMMIT',
    'wire_length_overhead',
    
    # Constants
    'OMEGA_SENTINEL',
    'COMMIT_SENTINEL',
    'OMEGA_RAW',
    'OMEGA_RLE',
    'OMEGA_COMPOSE',
]
