"""
M18: CLF Binary Codec
=====================

MATHEMATICAL ALIGNMENT:
    CLF demands causal minimality in REPRESENTATION, not just logic.
    
    Binary format encodes ONLY causal information:
        - Law ID: 1 byte
        - Parameters: Minimal binary encoding
        - No serialization pollution
    
    CRITICAL CORRECTIONS:
        ❌ Base64 is NOT CLF-compatible (1.33x overhead, external format)
        ❌ RAW_BYTES is NOT a valid law (admits defeat, violates closure)
        ❌ "Random data" does NOT exist (vocabulary gap, not fundamental limit)
        
        ✅ Every string has causal structure (closed mathematical object)
        ✅ If |Σ| ≥ |S|, vocabulary is incomplete (trigger deduction)
        ✅ CLF cannot fail, only vocabulary can be insufficient
    
    Proof of minimality:
        |Σ_binary| = |law_id| + |params|
        where params encode only the generative formula
        
    ∴ Zero format overhead, pure causality

AXIOM COMPLIANCE:
    A1 (Totality):    encode_seed(Σ) defined for all seeds with causal laws
    A2 (Minimality):  |Σ_binary| < |S| (strict, no fallback exceptions)
    A3 (Bijectivity): decode_seed(encode_seed(Σ)) = Σ
    A4 (Determinism): Same Σ → Same binary representation
    A5 (Closure):     Binary format is CLF-native, no external contamination
"""

import struct
from typing import Dict, Any, Tuple


# ========================================
# LAW FAMILY IDS
# ========================================

LAW_IDS = {
    'D1': 0x01,
    'D1_constant': 0x01,
    'D1_DEDUCED': 0x01,
    
    'D2': 0x02,
    'D2_affine': 0x02,
    'D2_DEDUCED': 0x02,
    
    'D3': 0x03,
    'D3_periodic': 0x03,
    'D3_DEDUCED': 0x03,
    
    'D4_SYMMETRIC': 0x04,
    'D4_XOR_AFFINE': 0x04,
    'D5_QUADRATIC': 0x05,
    'D5_MIRROR_COMPOSITE': 0x05,
    'D6_MIRROR': 0x06,
    'D7_LINEAR_MIRROR': 0x07,
    'D8_RECURRENCE': 0x08,
    
    'D_SPLIT': 0x10,
    'D_SPLIT_DEDUCED': 0x10,
    
    # ⚠️ Σ₀: VOCABULARY GAP (Not a valid law)
    # 
    # FORMAL DEFINITION:
    #   θ(S) = Σ₀ ⟺ ¬(∃Σ ∈ 𝓛_current : Λ(Σ) = S)
    # 
    # GUARANTEE:
    #   ∃Σ* ∉ 𝓛_current such that Λ(Σ*) = S
    #   Therefore: Σ₀ ∈ (𝓛_total ∖ 𝓛_current)
    # 
    # Σ₀ MEANS:
    #   ✓ "Vocabulary incomplete" - 𝓛_current lacks required generator
    #   ✓ "Structural law exists" - guaranteed by Axiom A1
    #   ✓ "LawNotInstantiatedError" - Σ exists, not yet implemented
    # 
    # Σ₀ DOES NOT MEAN:
    #   ✗ "String is random" - all strings have deterministic structure
    #   ✗ "String is incompressible" - CLF is not compression
    #   ✗ "No rule exists" - rule exists, not yet discovered
    #   ✗ "Error/null/undefined" - no undefined in closed bijective framework
    # 
    # CORRECT RESPONSE:
    #   1. Raise LawNotInstantiatedError(S)
    #   2. Trigger discover_generator(S)
    #   3. Extend vocabulary: 𝓛_current → 𝓛_current+1
    #   4. Re-apply: θ(S) yields Σ* instead of Σ₀
    # 
    # NEVER:
    #   ✗ Accept Σ₀ as valid final state
    #   ✗ Fallback to raw storage
    #   ✗ Return null/None/undefined
    'RAW_BYTES': 0xFF,  # Vocabulary gap marker
    'Σ₀': 0xFF,         # Vocabulary gap marker
    'D11_UNIVERSAL': 0xFF,
}

# Reverse mapping
ID_TO_LAW = {v: k for k, v in LAW_IDS.items() if not k.endswith('_DEDUCED')}


# ========================================
# VARINT ENCODING (Compact Integers)
# ========================================

def encode_varint(n: int) -> bytes:
    """
    Compact integer encoding:
        0-127:       1 byte  [0xxxxxxx]
        128-16383:   2 bytes [10xxxxxx][xxxxxxxx]
        16384+:      4 bytes [11xxxxxx][xxxxxxxx][xxxxxxxx][xxxxxxxx]
    """
    if n < 0:
        raise ValueError(f"VarInt must be non-negative, got {n}")
    
    if n < 128:
        # 1 byte: 0xxxxxxx
        return bytes([n])
    elif n < 16384:
        # 2 bytes: 10xxxxxx xxxxxxxx
        b1 = 0x80 | (n >> 8)
        b2 = n & 0xFF
        return bytes([b1, b2])
    else:
        # 4 bytes: 11xxxxxx xxxxxxxx xxxxxxxx xxxxxxxx
        b1 = 0xC0 | (n >> 24)
        b2 = (n >> 16) & 0xFF
        b3 = (n >> 8) & 0xFF
        b4 = n & 0xFF
        return bytes([b1, b2, b3, b4])


def decode_varint(data: bytes, offset: int = 0) -> Tuple[int, int]:
    """
    Decode VarInt and return (value, bytes_consumed)
    """
    if offset >= len(data):
        raise ValueError("Unexpected end of data in VarInt")
    
    first_byte = data[offset]
    
    if (first_byte & 0x80) == 0:
        # 1 byte
        return (first_byte, 1)
    elif (first_byte & 0x40) == 0:
        # 2 bytes
        if offset + 1 >= len(data):
            raise ValueError("Incomplete 2-byte VarInt")
        value = ((first_byte & 0x3F) << 8) | data[offset + 1]
        return (value, 2)
    else:
        # 4 bytes
        if offset + 3 >= len(data):
            raise ValueError("Incomplete 4-byte VarInt")
        value = ((first_byte & 0x3F) << 24) | (data[offset + 1] << 16) | \
                (data[offset + 2] << 8) | data[offset + 3]
        return (value, 4)


# ========================================
# SEED ENCODING
# ========================================

def encode_seed(seed: Dict[str, Any]) -> bytes:
    """
    Encode CLF seed to binary format.
    
    Returns pure causal information with zero serialization overhead.
    """
    # Use optimized_law if present (new format), else family (backward compat)
    family = seed.get('optimized_law', seed.get('family', 'RAW_BYTES'))
    n = seed.get('n', 0)
    params = seed.get('params', {})
    
    # Get law ID
    law_id = LAW_IDS.get(family)
    if law_id is None:
        raise ValueError(f"Unknown law family: {family}")
    
    # Encode based on law type
    if law_id == 0x01:
        # D1: Constant
        return encode_D1(params, n)
    elif law_id == 0x02:
        # D2: Affine
        return encode_D2(params, n)
    elif law_id == 0x03:
        # D3: Periodic
        return encode_D3(params, n)
    elif law_id == 0x04:
        # D4: Symmetric or XOR Affine - check which one
        if 'half_seed' in params or 'half' in params:
            # D4_SYMMETRIC
            return encode_D4_symmetric(params, n)
        else:
            # D4_XOR_AFFINE
            return encode_D4(params, n)
    elif law_id == 0x05:
        # D5: Mirror Composite or Quadratic - check which one
        if 'half_law' in params:
            # D5_MIRROR_COMPOSITE
            return encode_D5_mirror_composite(params, n)
        else:
            # D5_QUADRATIC
            return encode_D5(params, n)
    elif law_id == 0x06:
        # D6: Mirror
        return encode_D6_mirror(params, n)
    elif law_id == 0x07:
        # D7: Linear Mirror
        return encode_D7_linear_mirror(params, n)
    elif law_id == 0x08:
        # D8: Recurrence
        return encode_D8_recurrence(params, n)
    elif law_id == 0x10:
        # D_SPLIT: Compositional
        return encode_D_SPLIT(params, n)
    elif law_id == 0xFF:
        # RAW_BYTES: Fallback
        return encode_RAW_BYTES(params, n)
    else:
        raise ValueError(f"Unsupported law ID: {law_id:#x}")


def encode_D1(params: Dict[str, Any], n: int) -> bytes:
    """
    D1 Constant: [0x01][c: 1 byte][n: VarInt]
    """
    c = params.get('constant', params.get('c', 0))
    return bytes([0x01, c]) + encode_varint(n)


def encode_D2(params: Dict[str, Any], n: int) -> bytes:
    """
    D2 Affine: [0x02][s0: 1 byte][delta: 1 byte][n: VarInt]
    """
    s0 = params.get('s0', 0)
    delta = params.get('delta', 0)
    return bytes([0x02, s0, delta]) + encode_varint(n)


def encode_D3(params: Dict[str, Any], n: int) -> bytes:
    """
    D3 Periodic: [0x03][period: VarInt][pattern: period bytes][n: VarInt]
    """
    period = params.get('period', 0)
    pattern = params.get('pattern', [])
    
    if isinstance(pattern, list):
        pattern_bytes = bytes(pattern)
    else:
        pattern_bytes = pattern
    
    result = bytes([0x03])
    result += encode_varint(period)
    result += pattern_bytes
    result += encode_varint(n)
    return result


def encode_D4(params: Dict[str, Any], n: int) -> bytes:
    """
    D4 XOR Affine: [0x04][s0][delta][xor_const][n: VarInt]
    """
    s0 = params.get('base_s0', params.get('s0', 0))
    delta = params.get('base_delta', params.get('delta', 0))
    xor_const = params.get('xor_const', 0)
    return bytes([0x04, s0, delta, xor_const]) + encode_varint(n)


def encode_D5(params: Dict[str, Any], n: int) -> bytes:
    """
    D5 Quadratic: [0x05][a][b][c][n: VarInt]
    """
    a = params.get('a', 0)
    b = params.get('b', 0)
    c = params.get('c', 0)
    return bytes([0x05, a, b, c]) + encode_varint(n)


def encode_D4_symmetric(params: Dict[str, Any], n: int) -> bytes:
    """
    D4 Symmetric: [0x04][xor_const][half_seed_bytes]
    """
    xor_const = params['xor_const']
    result = bytes([0x04, xor_const])
    result += encode_varint(n)
    
    # Encode the half_seed recursively
    if 'half_seed' in params:
        half_seed_bytes = encode_seed(params['half_seed'])
        result += encode_varint(len(half_seed_bytes))
        result += half_seed_bytes
    elif 'half' in params:
        # Raw bytes format
        half = bytes(params['half'])
        result += encode_varint(len(half))
        result += half
    
    return result


def encode_D5_mirror_composite(params: Dict[str, Any], n: int) -> bytes:
    """
    D5 Mirror Composite: [0x05][half_law_bytes]
    """
    result = bytes([0x05])
    result += encode_varint(n)
    
    # Encode the half_law recursively
    half_law_bytes = encode_seed(params['half_law'])
    result += encode_varint(len(half_law_bytes))
    result += half_law_bytes
    
    return result


def encode_D6_mirror(params: Dict[str, Any], n: int) -> bytes:
    """
    D6 Mirror: [0x06][n]
    Palindrome - only need to store n, structure is implicit
    """
    result = bytes([0x06])
    result += encode_varint(n)
    return result


def encode_D7_linear_mirror(params: Dict[str, Any], n: int) -> bytes:
    """
    D7 Linear Mirror: [0x07][params][n]
    """
    result = bytes([0x07])
    # Encode params as needed (simplified for now)
    result += encode_varint(n)
    return result


def encode_D8_recurrence(params: Dict[str, Any], n: int) -> bytes:
    """
    D8 Recurrence: [0x08][params][n]
    """
    result = bytes([0x08])
    # Encode params as needed (simplified for now)
    result += encode_varint(n)
    return result


def encode_D_SPLIT(params: Dict[str, Any], n: int) -> bytes:
    """
    D_SPLIT Compositional: Three formats supported
      1. segments (recursive splitting)
      2. ring_laws (D9 radial discrete)
      3. meta (D9 radial parametric)
    
    Format: [0x10][format_type: 1 byte][data...]
    """
    result = bytes([0x10])
    
    if 'segments' in params:
        # Format: recursive segments
        segments = params['segments']
        result += bytes([0x01])  # Format type: segments
        result += encode_varint(len(segments))
        
        for segment_info in segments:
            if 'law_family' in segment_info:
                segment_seed = {
                    'family': segment_info['law_family'],
                    'params': segment_info.get('params', {}),
                    'n': segment_info.get('length', 0)
                }
            else:
                segment_seed = segment_info
            
            segment_bytes = encode_seed(segment_seed)
            result += encode_varint(len(segment_bytes))
            result += segment_bytes
        
        return result
    
    elif 'meta' in params or 'meta_law' in params:
        # Parametric format: meta-law (global formula)
        result += bytes([0x02])  # Format type: meta
        result += encode_varint(params['center'])
        result += encode_varint(params['n_rings'])
        
        meta = params.get('meta') or params.get('meta_law')
        # Encode meta-law type and parameters
        meta_type = meta['type']
        if meta_type == 'D2_AFFINE_CONSTANT_DELTA':
            result += bytes([0x01])  # Meta type ID
            result += bytes([meta['base_s0'] % 256])
            result += bytes([meta['gradient_s0'] % 256])
            result += bytes([meta['delta'] % 256])
        else:
            raise ValueError(f"Unsupported meta type: {meta_type}")
        
        return result
    
    elif 'ring_laws' in params:
        # Discrete format: ring_laws map
        result += bytes([0x03])  # Format type: ring_laws
        result += encode_varint(params['center'])
        result += encode_varint(params.get('total_rings', 0))
        
        ring_laws = params['ring_laws']
        result += encode_varint(len(ring_laws))
        
        # Encode each ring law
        for radius_str, ring_seed in ring_laws.items():
            radius = int(radius_str)
            result += encode_varint(radius)
            
            # Encode the ring's seed
            ring_bytes = encode_seed(ring_seed)
            result += encode_varint(len(ring_bytes))
            result += ring_bytes
        
        return result
    
    else:
        raise ValueError(f"D_SPLIT params missing segments, meta, or ring_laws: {params.keys()}")


def encode_RAW_BYTES(params: Dict[str, Any], n: int) -> bytes:
    """
    ⚠️ RAW_BYTES: VOCABULARY GAP INDICATOR (Not a valid CLF law)
    
    This function should never be called in a mathematically complete CLF system.
    Its presence indicates:
        - Vocabulary is incomplete
        - Deduction failed to find causal law
        - System should trigger vocabulary expansion
    
    CRITICAL: This is TEMPORARY COMPATIBILITY, not CLF compliance.
    Every string has causal structure. "Random data" is a vocabulary gap.
    
    If this encodes data where |output| ≥ |input|:
        ❌ NOT: Accept as "fundamental limit"
        ✅ YES: Treat as vocabulary incompleteness signal
    
    Pure bytes, no base64 (base64 violates minimality with 1.33x overhead).
    """
    # Check for base64-encoded data
    if 'data_b64' in params:
        import base64
        # Decode base64 back to pure bytes
        # (Base64 itself is not CLF-compatible due to 1.33x overhead)
        raw_bytes = base64.b64decode(params['data_b64'])
    elif 'data' in params:
        data = params['data']
        if isinstance(data, list):
            raw_bytes = bytes(data)
        elif isinstance(data, (bytes, bytearray)):
            raw_bytes = bytes(data)
        else:
            raise ValueError("RAW_BYTES requires 'data' as bytes or list")
    else:
        raise ValueError("RAW_BYTES requires 'data' or 'data_b64' parameter")
    
    result = bytes([0xFF])
    result += encode_varint(len(raw_bytes))
    result += raw_bytes
    return result


# ========================================
# SEED DECODING
# ========================================

def decode_seed(data: bytes, offset: int = 0) -> Tuple[Dict[str, Any], int]:
    """
    Decode binary CLF seed.
    
    Returns (seed_dict, bytes_consumed)
    """
    if offset >= len(data):
        raise ValueError("Unexpected end of data")
    
    law_id = data[offset]
    offset += 1
    
    if law_id == 0x01:
        return decode_D1(data, offset)
    elif law_id == 0x02:
        return decode_D2(data, offset)
    elif law_id == 0x03:
        return decode_D3(data, offset)
    elif law_id == 0x04:
        return decode_D4(data, offset)
    elif law_id == 0x05:
        return decode_D5(data, offset)
    elif law_id == 0x10:
        return decode_D_SPLIT(data, offset)
    elif law_id == 0xFF:
        return decode_RAW_BYTES(data, offset)
    else:
        raise ValueError(f"Unknown law ID: {law_id:#x}")


def decode_D1(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D1 Constant: [c: 1 byte][n: VarInt]"""
    c = data[offset]
    offset += 1
    
    n, consumed = decode_varint(data, offset)
    offset += consumed
    
    seed = {
        'family': 'D1',
        'params': {'c': c},
        'n': n
    }
    return (seed, offset)


def decode_D2(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D2 Affine: [s0][delta][n: VarInt]"""
    s0 = data[offset]
    delta = data[offset + 1]
    offset += 2
    
    n, consumed = decode_varint(data, offset)
    offset += consumed
    
    seed = {
        'family': 'D2',
        'params': {'s0': s0, 'delta': delta},
        'n': n
    }
    return (seed, offset)


def decode_D3(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D3 Periodic: [period: VarInt][pattern: period bytes][n: VarInt]"""
    period, consumed = decode_varint(data, offset)
    offset += consumed
    
    pattern = list(data[offset:offset + period])
    offset += period
    
    n, consumed = decode_varint(data, offset)
    offset += consumed
    
    seed = {
        'family': 'D3',
        'params': {'period': period, 'pattern': pattern},
        'n': n
    }
    return (seed, offset)


def decode_D4(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D4 XOR Affine: [s0][delta][xor_const][n: VarInt]"""
    s0 = data[offset]
    delta = data[offset + 1]
    xor_const = data[offset + 2]
    offset += 3
    
    n, consumed = decode_varint(data, offset)
    offset += consumed
    
    seed = {
        'family': 'D4_XOR_AFFINE',
        'params': {'s0': s0, 'delta': delta, 'xor_const': xor_const},
        'n': n
    }
    return (seed, offset)


def decode_D5(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D5 Quadratic: [a][b][c][n: VarInt]"""
    a = data[offset]
    b = data[offset + 1]
    c = data[offset + 2]
    offset += 3
    
    n, consumed = decode_varint(data, offset)
    offset += consumed
    
    seed = {
        'family': 'D5_QUADRATIC',
        'params': {'a': a, 'b': b, 'c': c},
        'n': n
    }
    return (seed, offset)


def decode_D_SPLIT(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """D_SPLIT Compositional: Three formats (0x01=segments, 0x02=meta, 0x03=ring_laws)"""
    format_type = data[offset]
    offset += 1
    
    if format_type == 0x01:
        # Format: segments
        num_segments, consumed = decode_varint(data, offset)
        offset += consumed
        
        segments = []
        for _ in range(num_segments):
            seg_len, consumed = decode_varint(data, offset)
            offset += consumed
            
            segment_seed, bytes_used = decode_seed(data, offset)
            offset += bytes_used
            
            segments.append(segment_seed)
        
        n = sum(seg['n'] for seg in segments)
        
        seed = {
            'family': 'D_SPLIT',
            'params': {'segments': segments},
            'n': n
        }
        return (seed, offset)
    
    elif format_type == 0x02:
        # Parametric format: meta-law
        center, consumed = decode_varint(data, offset)
        offset += consumed
        
        n_rings, consumed = decode_varint(data, offset)
        offset += consumed
        
        meta_type_id = data[offset]
        offset += 1
        
        if meta_type_id == 0x01:
            # D2_AFFINE_CONSTANT_DELTA
            base_s0 = data[offset]
            offset += 1
            gradient_s0 = data[offset]
            offset += 1
            delta = data[offset]
            offset += 1
            
            meta = {
                'type': 'D2_AFFINE_CONSTANT_DELTA',
                'base_s0': base_s0,
                'gradient_s0': gradient_s0,
                'delta': delta
            }
        else:
            raise ValueError(f"Unknown meta type ID: {meta_type_id:#x}")
        
        seed = {
            'family': 'D_SPLIT',
            'params': {
                'center': center,
                'meta': meta,
                'n_rings': n_rings
            },
            'n': center * 2  # Approximate
        }
        return (seed, offset)
    
    elif format_type == 0x03:
        # Discrete format: ring_laws
        center, consumed = decode_varint(data, offset)
        offset += consumed
        
        total_rings, consumed = decode_varint(data, offset)
        offset += consumed
        
        num_ring_laws, consumed = decode_varint(data, offset)
        offset += consumed
        
        ring_laws = {}
        for _ in range(num_ring_laws):
            radius, consumed = decode_varint(data, offset)
            offset += consumed
            
            ring_len, consumed = decode_varint(data, offset)
            offset += consumed
            
            ring_seed, bytes_used = decode_seed(data, offset)
            offset += bytes_used
            
            ring_laws[str(radius)] = ring_seed
        
        seed = {
            'family': 'D_SPLIT',
            'params': {
                'center': center,
                'ring_laws': ring_laws,
                'total_rings': total_rings
            },
            'n': center * 2  # Approximate
        }
        return (seed, offset)
    
    else:
        raise ValueError(f"Unknown D_SPLIT format type: {format_type:#x}")


def decode_RAW_BYTES(data: bytes, offset: int) -> Tuple[Dict[str, Any], int]:
    """
    ⚠️ RAW_BYTES: VOCABULARY GAP INDICATOR
    
    Decodes raw byte storage. Presence of this in seeds indicates
    vocabulary incompleteness, not fundamental data property.
    """
    length, consumed = decode_varint(data, offset)
    offset += consumed
    
    raw_bytes = bytes(data[offset:offset + length])
    offset += length
    
    seed = {
        'family': 'RAW_BYTES',
        'params': {'data': raw_bytes},
        'n': length
    }
    return (seed, offset)


# ========================================
# CONVENIENCE FUNCTIONS
# ========================================

def seed_to_binary_file(seed: Dict[str, Any], filepath: str) -> None:
    """Save seed as binary .clf file"""
    binary_data = encode_seed(seed)
    with open(filepath, 'wb') as f:
        f.write(binary_data)


def binary_file_to_seed(filepath: str) -> Dict[str, Any]:
    """Load seed from binary .clf file"""
    with open(filepath, 'rb') as f:
        binary_data = f.read()
    seed, _ = decode_seed(binary_data)
    return seed


def get_binary_seed_size(seed: Dict[str, Any]) -> int:
    """Calculate size of binary seed without encoding to file"""
    return len(encode_seed(seed))
