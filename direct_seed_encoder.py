# ================================================================
# CLF CAUSAL LOGIC GUIDELINES (MANDATORY FOR AI ASSISTANTS)
# ------------------------------------------------
# • No reading or sampling of physical files.
# • θ(S) deduces formal Σ from structure (n, law), never from bytes.
# • Ξ(Σ) projects S symbolically, not sequentially.
# • D9_RADIAL uses ring_laws: per-ring sub-seeds Σ_r ∈ ℒ.
# • Execution cost must remain O(1) with respect to n.
# ================================================================

# CLF CAUSAL GUARD:
# D9 and all recognition/encoding logic must stay purely causal.
# - No O(n) radial arrays, sampling, or iteration over input bytes.
# - Seeds store laws (family, params, n), never raw byte rings.
# - Encoding serializes symbolic structure, not sampled data.
# - Any helper must operate in O(1) per ring, not O(n) per element.

"""Direct seed encoder for bijective binary causal math.

Encodes recognized laws DIRECTLY to a compact binary format without
intermediate atom representation.

Wire format
===========

Legacy header (v1):
    [law_id:1] [n:u32be] [params...]

Extended header (v2, used when n does not fit u32):
    [0xFE][law_id:1] [n:uvarint] [params...]
"""

import struct
from typing import Dict, Any


def _assert_seed_domain(seed: Any) -> None:
    """Domain guard: ensure object is a symbolic seed Σ ∈ 𝒮 (not wire bytes 𝒲).

    This module implements only E: 𝒮→𝒲 and D: 𝒲→𝒮. It must not accept
    manifestations (𝒪) or confuse wire-bytes (𝒲) with seeds (𝒮).
    """
    if not isinstance(seed, dict):
        raise TypeError(f"Expected Σ ∈ 𝒮 as dict seed, got {type(seed)}")
    if "family" not in seed or "params" not in seed or "n" not in seed:
        raise TypeError("Seed Σ must contain keys: 'family', 'params', 'n'")
    if isinstance(seed.get("params"), (bytes, bytearray, memoryview)):
        raise TypeError("Seed Σ params must be dict, not wire bytes")
    if not isinstance(seed.get("params"), dict):
        raise TypeError(f"Seed Σ params must be dict, got {type(seed.get('params'))}")


def _coerce_wire_bytes(wire: Any) -> bytes:
    """Domain guard: ensure object is wire bytes W ∈ 𝒲."""
    if isinstance(wire, memoryview):
        wire = wire.tobytes()
    if isinstance(wire, bytearray):
        wire = bytes(wire)
    if not isinstance(wire, bytes):
        raise TypeError(f"Expected W ∈ 𝒲 as bytes, got {type(wire)}")
    return wire


def _encode_uvarint(n: int) -> bytes:
    """Unsigned varint (7-bit) encoding."""
    n = int(n)
    if n < 0:
        raise ValueError("uvarint cannot encode negative")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(0x80 | b)
        else:
            out.append(b)
            break
    return bytes(out)


def _decode_uvarint(buf: bytes, pos: int) -> tuple[int, int]:
    """Return (value, new_pos)."""
    shift = 0
    value = 0
    while True:
        if pos >= len(buf):
            raise ValueError("uvarint truncated")
        b = buf[pos]
        pos += 1
        value |= (b & 0x7F) << shift
        if not (b & 0x80):
            return value, pos
        shift += 7
        if shift > 63:
            raise ValueError("uvarint too large")


_EXTENDED_HEADER_MARKER = 0xFE


def _encode_header(law_id: int, n: int) -> bytes:
    """Encode header for a seed.

    Uses the legacy u32 header when possible; otherwise emits an extended
    header with uvarint n.
    """
    n = int(n)
    law_id = int(law_id) & 0xFF
    if 0 <= n <= 0xFFFFFFFF:
        return struct.pack('>BI', law_id, n)
    return bytes([_EXTENDED_HEADER_MARKER, law_id]) + _encode_uvarint(n)


def _decode_header(seed: bytes) -> tuple[int, int, int]:
    """Decode header and return (law_id, n, params_start)."""
    if not seed:
        raise ValueError("Seed too short")
    if seed[0] == _EXTENDED_HEADER_MARKER:
        if len(seed) < 2:
            raise ValueError("Seed too short")
        law_id = seed[1]
        n, pos = _decode_uvarint(seed, 2)
        return int(law_id), int(n), int(pos)
    if len(seed) < 5:
        raise ValueError("Seed too short")
    law_id = seed[0]
    n = struct.unpack('>I', seed[1:5])[0]
    return int(law_id), int(n), 5


def encode_seed_direct(theta_result: Dict[str, Any]) -> bytes:
    """
    Serialize causal seed Σ to binary representation
    
    Maps symbolic structure (family, params, n) to minimal binary form.
    This is a representation mapping, not an encoding transformation.
    
    Args:
        theta_result: Causal seed Σ = θ(S) containing (family, params, n)
    Returns:
        Binary representation of Σ for storage/transmission
    """
    _assert_seed_domain(theta_result)
    family = theta_result['family']
    params = theta_result['params']
    n = int(theta_result['n'])
    
    if family == 'D0_IDENTITY':
        # D0 EXPLICIT: [0x00][n:4][bytes:n]
        # The identity function f(i)=byte_i extracted from existence
        # INSTANT: bytes are already in correct format (O(1))
        byte_data = params['bytes']
        if isinstance(byte_data, list):
            byte_data = bytes(byte_data)
        return _encode_header(0x00, n) + byte_data
    
    elif family == 'D1':
        # CONST: [0x01][n:4][c:1]
        c = params['c']
        return _encode_header(0x01, n) + bytes([int(c) & 0xFF])
    
    elif family == 'D2':
        # AFFINE: [0x02][n:4][s0:1][delta:1]
        s0 = params['s0']
        delta = params['delta']
        return _encode_header(0x02, n) + bytes([int(s0) & 0xFF, int(delta) & 0xFF])
    
    elif family == 'D3':
        # D3 PERIODIC: [0x03][n:4][period:2][cycle:period bytes]
        period = params['period']
        cycle = bytes(params.get('cycle') or params.get('pattern'))  # Backward compat
        period_bytes = struct.pack('>H', period)
        return _encode_header(0x03, n) + period_bytes + cycle
    
    elif family == 'D4_XOR_AFFINE':
        # XOR_AFFINE: [0x04][n:4][s0:1][delta:1][xor_const:1]
        s0 = params['base_s0']
        delta = params['base_delta']
        xor_const = params['xor_const']
        return _encode_header(0x04, n) + bytes([int(s0) & 0xFF, int(delta) & 0xFF, int(xor_const) & 0xFF])
    
    elif family == 'D5_QUADRATIC':
        # QUADRATIC: [0x05][n:4][a:1][b:1][c:1]
        a = params['a']
        b = params['b']
        c = params['c']
        return _encode_header(0x05, n) + bytes([int(a) & 0xFF, int(b) & 0xFF, int(c) & 0xFF])
    
    elif family == 'D6_MIRROR':
        # MIRROR: [0x06][n:4][half_len:4][pattern:half_len]
        pattern = params['pattern']
        if isinstance(pattern, list):
            pattern = bytes(pattern)
        half_len = len(pattern)
        return _encode_header(0x06, n) + struct.pack('>I', half_len) + pattern
    
    elif family == 'D7_ROTATIONAL':
        # ROTATIONAL: [0x07][n:4][period:2][stride:2][pattern:period]
        pattern = params['pattern']
        if isinstance(pattern, list):
            pattern = bytes(pattern)
        stride = params['stride']
        period = len(pattern)
        return _encode_header(0x07, n) + struct.pack('>HH', period, stride) + pattern

    elif family == 'D9_INSTANT_DEDUCTION':
        # D9 INSTANT-DEDUCTION: [0x29][header][s0:1][r0:1][ds:1][dr:1]
        # Canonical parameters are integer-modular (0..255).
        s0 = int(params['s0']) & 0xFF
        r0 = int(params['r0']) & 0xFF
        ds = int(params['ds']) & 0xFF
        dr = int(params['dr']) & 0xFF
        return _encode_header(0x29, n) + bytes([s0, r0, ds, dr])
    
    elif family == 'D_SPLIT':
        # SPLIT: [0x10][n:4][num_segments:4][segments...]
        segments = params['segments']
        num_segments = len(segments)
        
        result = _encode_header(0x10, n) + struct.pack('>I', num_segments)  # 4 bytes for num_segments
        
        # Encode each segment recursively
        for seg in segments:
            # Support both formats: {family, n, params} and {law_family, length, params}
            if 'family' in seg:
                seg_result = {
                    'family': seg['family'],
                    'params': seg['params'],
                    'n': seg['n']
                }
            else:
                seg_result = {
                    'family': seg['law_family'],
                    'params': seg['params'],
                    'n': seg['length']
                }
            seg_bytes = encode_seed_direct(seg_result)
            result += seg_bytes
        
        return result
    
    elif family == 'D11_STRUCTURAL_HASH':
        # STRUCTURAL_HASH: [0x11][n:4][params...]
        from D11_structural_hash import encode_d11_params
        params_bytes = encode_d11_params(params)
        return _encode_header(0x11, n) + params_bytes
    
    elif family == 'D11_RAW':
        # RAW DATA: [0xFF][n:4][data...] 
        # Only used for truly incompressible segments in D_SPLIT
        data = bytes(params.get('data', params.get('generator', [])))
        return _encode_header(0xFF, n) + data
    
    # ================================================================
    # CLF CAUSAL CONTEXT: D9_RADIAL
    #
    # Encoding stores symbolic causal structure {center, {r → Σ_r}}, NEVER manifestation data.
    # Each Σ_r is recursively encoded via encode_seed_direct (closure of ℒ).
    #
    # IMPORTANT:
    # Earlier drafts assumed implicit radii (0,1,2,4,8,...) which conflicts with
    # strategic ring selection (e.g., primes). Radii are therefore serialized
    # explicitly in the seed (still O(1) because ring_count is bounded).
    # ================================================================
    elif family == 'D9_RADIAL':
        # RADIAL with CLF-SHA (strategic position sampling, NOT sequential hash)
        center = params.get('center', 0)
        ring_laws = params.get('ring_laws', {})
        structural_hash = params.get('structural_hash', '')  # CLF-SHA via sampling
        magic = params.get('magic', '')  # hex string
        meta = params.get('meta') or params.get('meta_law')
        sampled = bool(params.get('sampled', False))
        completion = (params.get('completion') or 'AUTO').upper()

        # If a universal meta-law carries the ring_laws map (common for limit-closure),
        # fall back to that so encoding remains seed-complete.
        if (not ring_laws) and isinstance(meta, dict) and isinstance(meta.get('ring_laws'), dict):
            ring_laws = meta.get('ring_laws')
        
        result = _encode_header(0x09, n) + struct.pack('>I', int(center) & 0xFFFFFFFF)

        # D9 v2 header (version marker in high bit)
        # flags:
        #   bit7 = 1 (v2 marker)
        #   bit0 = has_structural_hash
        #   bit1 = has_magic
        #   bit2 = has_meta
        #   bit3 = sampled
        #   bit4 = ring_count encoded as uvarint
        flags = 0x80
        if structural_hash:
            flags |= 0x01
        if magic:
            flags |= 0x02
        if meta:
            flags |= 0x04
        if sampled:
            flags |= 0x08
        # v2 upgrade: allow seed-complete D9 with ring_count > 255.
        flags |= 0x10
        result += struct.pack('B', flags)

        # Optional structural hash
        if structural_hash:
            hash_bytes = bytes.fromhex(structural_hash)
            hash_len = min(len(hash_bytes), 255)
            result += struct.pack('B', hash_len)
            result += hash_bytes[:hash_len]

        # Optional magic
        if magic:
            magic_bytes = bytes.fromhex(magic)
            magic_len = min(len(magic_bytes), 255)
            result += struct.pack('B', magic_len)
            result += magic_bytes[:magic_len]

        # Optional meta-law
        if meta:
            meta_type = meta.get('type')
            if meta_type == 'D2_AFFINE_CONSTANT_DELTA':
                # [meta_id:1][base_s0:1][gradient_s0:1][delta:1]
                result += b'\x01'
                result += struct.pack('BBB', int(meta['base_s0']) & 0xFF, int(meta['gradient_s0']) & 0xFF, int(meta['delta']) & 0xFF)
            elif meta_type == 'D9_LIMIT_CAUSAL_CLOSURE':
                # [meta_id:1]
                # Ring laws are serialized in the standard D9 ring_laws section.
                # radii_defined is derived from the encoded radii.
                result += b'\x03'
            elif meta_type == 'D9_LEFT_RIGHT_SEEDS':
                # [meta_id:1][len(left):uvarint][left_seed_bytes][len(right):uvarint][right_seed_bytes]
                left_seed = meta.get('left_seed')
                right_seed = meta.get('right_seed')
                if left_seed is None or right_seed is None:
                    raise ValueError("D9_LEFT_RIGHT_SEEDS meta missing left_seed/right_seed")
                left_bytes = encode_seed_direct(left_seed)
                right_bytes = encode_seed_direct(right_seed)
                result += b'\x02'
                result += _encode_uvarint(len(left_bytes)) + left_bytes
                result += _encode_uvarint(len(right_bytes)) + right_bytes
            else:
                raise ValueError(f"Unsupported D9 meta-law type for encoding: {meta_type}")

        # Completion semantics (explicit; avoids hidden non-bijective fallbacks)
        # 0 = AUTO (try bracket-affine mod256 then nearest)
        # 1 = NEAREST
        # 2 = STRICT
        # 3 = AFFINE_BRACKET
        completion_map = {
            'AUTO': 0,
            'NEAREST': 1,
            'STRICT': 2,
            'AFFINE_BRACKET': 3,
        }
        comp_id = completion_map.get(completion)
        if comp_id is None:
            raise ValueError(f"Unknown D9 completion mode: {completion}")
        result += struct.pack('B', comp_id)

        # Ring laws
        # rings_mode: 0 = implicit radii (legacy), 1 = explicit radii (preferred)
        rings_mode = 1
        result += struct.pack('B', rings_mode)
        # v2 ring_count is uvarint (flag bit4)
        result += _encode_uvarint(len(ring_laws))
        for r in sorted(ring_laws.keys()):
            ring_seed_dict = ring_laws[r]
            ring_bytes = encode_seed_direct(ring_seed_dict)
            result += struct.pack('>I', int(r) & 0xFFFFFFFF)
            result += ring_bytes
        
        return result
    
    elif family == 'D10_SPIRAL':
        # SPIRAL: [0x0A][n:4][params...]
        # Add encoding for spiral parameters
        pattern = bytes(params.get('pattern', []))
        multiplier = params.get('multiplier', 1)
        return _encode_header(0x0A, n) + struct.pack('>I', multiplier) + pattern

    elif family == 'D10_RECURRENCE':
        # RECURRENCE (block-repeat):
        # [0x12][n:4][m:uvarint][len(subseed):uvarint][subseed]
        m = int(params['m'])
        sub_seed = params['sub_seed']
        sub_bytes = encode_seed_direct(sub_seed)
        return _encode_header(0x12, n) + _encode_uvarint(m) + _encode_uvarint(len(sub_bytes)) + sub_bytes

    elif family == 'D11_RADIAL_RECURRENCE':
        # RADIAL RECURRENCE:
        # [0x13][n:4][center:4][len(radial_seed):uvarint][radial_seed]
        center = int(params['center'])
        radial_seed = params['radial_seed']
        radial_bytes = encode_seed_direct(radial_seed)
        return _encode_header(0x13, n) + struct.pack('>I', center & 0xFFFFFFFF) + _encode_uvarint(len(radial_bytes)) + radial_bytes

    elif family == 'D12_SELF_AFFINE':
        # SELF-AFFINE PERMUTATION:
        # [0x14][n:4][alpha:uvarint][beta:uvarint][len(base_seed):uvarint][base_seed]
        alpha = int(params['alpha'])
        beta = int(params['beta'])
        base_seed = params['base_seed']
        base_bytes = encode_seed_direct(base_seed)
        return _encode_header(0x14, n) + _encode_uvarint(alpha) + _encode_uvarint(beta) + _encode_uvarint(len(base_bytes)) + base_bytes

    elif family == 'D13_REACTIVE_DIFFERENTIAL':
        # REACTIVE DIFFERENTIAL:
        # v1 (constant delta): [0x15][n:4][s0:1][delta:1]
        # v2 (delta sub-seed): [0x19][n:4][s0:1][len(delta_seed):uvarint][delta_seed]
        s0 = int(params.get('s0', 0)) & 0xFF
        delta_seed = params.get('delta_seed')
        if isinstance(delta_seed, dict):
            ds_bytes = encode_seed_direct(delta_seed)
            return _encode_header(0x19, n) + bytes([s0]) + _encode_uvarint(len(ds_bytes)) + ds_bytes
        delta = int(params.get('delta', 0)) & 0xFF
        return _encode_header(0x15, n) + bytes([s0, delta])

    elif family == 'D14_CAUSAL_CORRELATIVE':
        # CAUSAL CORRELATIVE (stride/echo wrapper):
        # [0x16][n:4][k:uvarint][len(subseed):uvarint][subseed]
        k = int(params.get('k', params.get('m')))
        sub_seed = params['sub_seed']
        sub_bytes = encode_seed_direct(sub_seed)
        return _encode_header(0x16, n) + _encode_uvarint(k) + _encode_uvarint(len(sub_bytes)) + sub_bytes

    elif family == 'D15_SYMBOLIC_META_EMBED':
        # META-EMBED (composition wrapper):
        # [0x17][n:4][num_segments:4][segments...]
        segments = params.get('segments')
        if segments is None:
            segments = params.get('sub_seeds')
        if not isinstance(segments, list):
            raise ValueError('D15_SYMBOLIC_META_EMBED segments must be list')
        result = _encode_header(0x17, n) + struct.pack('>I', len(segments))
        for seg in segments:
            if not isinstance(seg, dict):
                raise ValueError('D15_SYMBOLIC_META_EMBED segment must be dict seed')
            seg_bytes = encode_seed_direct(seg)
            result += seg_bytes
        return result

    elif family == 'D16_PARAMETRIC_LAW_GROWTH':
        # PARAMETRIC LAW GROWTH (identity wrapper):
        # [0x18][n:4][len(base_seed):uvarint][base_seed]
        base_seed = params['base_seed']
        base_bytes = encode_seed_direct(base_seed)
        return _encode_header(0x18, n) + _encode_uvarint(len(base_bytes)) + base_bytes

    elif family == 'D17_XOR_CONST':
        # XOR wrapper:
        # [0x1A][n:4][k:1][len(inner_seed):uvarint][inner_seed]
        k = int(params.get('k', 0)) & 0xFF
        inner_seed = params.get('inner_seed')
        if not isinstance(inner_seed, dict):
            raise ValueError('D17_XOR_CONST missing inner_seed')
        inner_bytes = encode_seed_direct(inner_seed)
        return _encode_header(0x1A, n) + bytes([k]) + _encode_uvarint(len(inner_bytes)) + inner_bytes

    elif family == 'D18_ADD_CONST':
        # ADD wrapper:
        # [0x1B][n:4][k:1][len(inner_seed):uvarint][inner_seed]
        k = int(params.get('k', 0)) & 0xFF
        inner_seed = params.get('inner_seed')
        if not isinstance(inner_seed, dict):
            raise ValueError('D18_ADD_CONST missing inner_seed')
        inner_bytes = encode_seed_direct(inner_seed)
        return _encode_header(0x1B, n) + bytes([k]) + _encode_uvarint(len(inner_bytes)) + inner_bytes
    
    else:
        raise ValueError(f"Cannot encode family: {family}")


def decode_seed_direct(seed: bytes) -> Dict[str, Any]:
    """
    Parse binary representation back to symbolic seed structure
    
    Inverse of encode_seed_direct: reconstructs (family, params, n) from binary form.
    This is a structural mapping, not a decoding process.
    
    Args:
        seed: Binary representation of causal seed Σ
        
    Returns:
        Symbolic seed structure: {family: str, params: dict, n: int}
    """
    seed = _coerce_wire_bytes(seed)
    law_id, n, params_start = _decode_header(seed)
    
    if law_id == 0x00:
        # D0: EXPLICIT - identity function
        bytes_data = list(seed[params_start:params_start+n])
        return {'family': 'D0_IDENTITY', 'params': {'bytes': bytes_data}, 'n': n}
    
    elif law_id == 0x01:
        # D1: CONST
        c = seed[params_start]
        return {'family': 'D1', 'params': {'c': c}, 'n': n}
    
    elif law_id == 0x02:
        # D2: AFFINE
        s0 = seed[params_start]
        delta = seed[params_start + 1]
        return {'family': 'D2', 'params': {'s0': s0, 'delta': delta}, 'n': n}
    
    elif law_id == 0x03:
        # D3: PERIODIC - bijective modulo repetition
        period = struct.unpack('>H', seed[params_start:params_start+2])[0]
        cycle = list(seed[params_start+2:params_start+2+period])
        return {'family': 'D3', 'params': {'period': period, 'cycle': cycle}, 'n': n}
    
    elif law_id == 0x04:
        # D4: XOR_AFFINE
        s0 = seed[params_start]
        delta = seed[params_start + 1]
        xor_const = seed[params_start + 2]
        return {
            'family': 'D4_XOR_AFFINE',
            'params': {'base_s0': s0, 'base_delta': delta, 'xor_const': xor_const},
            'n': n
        }

    elif law_id == 0x15:
        # D13: REACTIVE DIFFERENTIAL
        s0 = seed[params_start]
        delta = seed[params_start + 1]
        return {'family': 'D13_REACTIVE_DIFFERENTIAL', 'params': {'s0': s0, 'delta': delta}, 'n': n}

    elif law_id == 0x19:
        # D13: REACTIVE DIFFERENTIAL (delta sub-seed)
        pos = params_start
        if pos + 1 > len(seed):
            raise ValueError('D13 v2 truncated s0')
        s0 = seed[pos]
        pos += 1
        ds_len, pos = _decode_uvarint(seed, pos)
        end = pos + ds_len
        if end > len(seed):
            raise ValueError('D13 v2 truncated delta_seed')
        delta_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D13_REACTIVE_DIFFERENTIAL', 'params': {'s0': int(s0), 'delta_seed': delta_seed}, 'n': n}

    elif law_id == 0x16:
        # D14_CAUSAL_CORRELATIVE
        pos = params_start
        k, pos = _decode_uvarint(seed, pos)
        sub_len, pos = _decode_uvarint(seed, pos)
        end = pos + sub_len
        if end > len(seed):
            raise ValueError('D14_CAUSAL_CORRELATIVE truncated sub-seed')
        sub_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D14_CAUSAL_CORRELATIVE', 'params': {'k': int(k), 'sub_seed': sub_seed}, 'n': n}

    elif law_id == 0x17:
        # D15_SYMBOLIC_META_EMBED
        pos = params_start
        if pos + 4 > len(seed):
            raise ValueError('D15_SYMBOLIC_META_EMBED truncated header')
        num_segments = struct.unpack('>I', seed[pos:pos+4])[0]
        pos += 4
        segments = []
        for _ in range(int(num_segments)):
            seg = decode_seed_direct(seed[pos:])
            seg_bytes = encode_seed_direct(seg)
            segments.append(seg)
            pos += len(seg_bytes)
        return {'family': 'D15_SYMBOLIC_META_EMBED', 'params': {'segments': segments}, 'n': n}

    elif law_id == 0x18:
        # D16_PARAMETRIC_LAW_GROWTH
        pos = params_start
        base_len, pos = _decode_uvarint(seed, pos)
        end = pos + base_len
        if end > len(seed):
            raise ValueError('D16_PARAMETRIC_LAW_GROWTH truncated base seed')
        base_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D16_PARAMETRIC_LAW_GROWTH', 'params': {'base_seed': base_seed}, 'n': n}

    elif law_id == 0x1A:
        # D17_XOR_CONST
        pos = params_start
        if pos + 1 > len(seed):
            raise ValueError('D17_XOR_CONST truncated k')
        k = int(seed[pos])
        pos += 1
        inner_len, pos = _decode_uvarint(seed, pos)
        end = pos + inner_len
        if end > len(seed):
            raise ValueError('D17_XOR_CONST truncated inner seed')
        inner_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D17_XOR_CONST', 'params': {'k': k, 'inner_seed': inner_seed}, 'n': n}

    elif law_id == 0x1B:
        # D18_ADD_CONST
        pos = params_start
        if pos + 1 > len(seed):
            raise ValueError('D18_ADD_CONST truncated k')
        k = int(seed[pos])
        pos += 1
        inner_len, pos = _decode_uvarint(seed, pos)
        end = pos + inner_len
        if end > len(seed):
            raise ValueError('D18_ADD_CONST truncated inner seed')
        inner_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D18_ADD_CONST', 'params': {'k': k, 'inner_seed': inner_seed}, 'n': n}
    elif law_id == 0x05:
        # D5: QUADRATIC
        a = seed[params_start]
        b = seed[params_start + 1]
        c = seed[params_start + 2]
        return {'family': 'D5_QUADRATIC', 'params': {'a': a, 'b': b, 'c': c}, 'n': n}
    
    elif law_id == 0x06:
        # D6: MIRROR - palindromic symmetry
        half_len = struct.unpack('>I', seed[params_start:params_start+4])[0]
        pattern = list(seed[params_start+4:params_start+4+half_len])
        return {'family': 'D6_MIRROR', 'params': {'pattern': pattern}, 'n': n}
    
    elif law_id == 0x07:
        # D7: ROTATIONAL - periodic with stride
        period, stride = struct.unpack('>HH', seed[params_start:params_start+4])
        pattern = list(seed[params_start+4:params_start+4+period])
        return {'family': 'D7_ROTATIONAL', 'params': {'pattern': pattern, 'stride': stride}, 'n': n}
    
    elif law_id == 0x09:
        # D9: RADIAL with structural hash and optional ring laws
        pos = params_start
        center = struct.unpack('>I', seed[pos:pos+4])[0]
        pos += 4

        # v2 detection: flags byte with high bit set
        first = seed[pos]
        if first & 0x80:
            flags = first
            pos += 1

            structural_hash = ''
            if flags & 0x01:
                hash_len = seed[pos]
                pos += 1
                structural_hash = seed[pos:pos+hash_len].hex()
                pos += hash_len

            magic = ''
            if flags & 0x02:
                magic_len = seed[pos]
                pos += 1
                magic = seed[pos:pos+magic_len].hex()
                pos += magic_len

            meta = None
            if flags & 0x04:
                meta_id = seed[pos]
                pos += 1
                if meta_id == 0x01:
                    base_s0, gradient_s0, delta = struct.unpack('BBB', seed[pos:pos+3])
                    pos += 3
                    meta = {
                        'type': 'D2_AFFINE_CONSTANT_DELTA',
                        'base_s0': base_s0,
                        'gradient_s0': gradient_s0,
                        'delta': delta,
                    }
                elif meta_id == 0x02:
                    left_len, pos = _decode_uvarint(seed, pos)
                    left_seed = decode_seed_direct(seed[pos:pos+left_len])
                    pos += left_len
                    right_len, pos = _decode_uvarint(seed, pos)
                    right_seed = decode_seed_direct(seed[pos:pos+right_len])
                    pos += right_len
                    meta = {
                        'type': 'D9_LEFT_RIGHT_SEEDS',
                        'left_seed': left_seed,
                        'right_seed': right_seed,
                    }
                elif meta_id == 0x03:
                    # D9 limit-closure meta-law: ring_laws/radii are provided by the
                    # standard D9 ring_laws section, so no extra payload is needed here.
                    meta = {
                        'type': 'D9_LIMIT_CAUSAL_CLOSURE',
                    }
                else:
                    raise ValueError(f"Unknown D9 meta-law id: {meta_id}")

            comp_id = seed[pos]
            pos += 1
            completion_rev = {
                0: 'AUTO',
                1: 'NEAREST',
                2: 'STRICT',
                3: 'AFFINE_BRACKET',
            }
            completion = completion_rev.get(comp_id)
            if completion is None:
                raise ValueError(f"Unknown D9 completion id: {comp_id}")

            # Read ring laws
            rings_mode = seed[pos]
            pos += 1
            if flags & 0x10:
                ring_count, pos = _decode_uvarint(seed, pos)
            else:
                ring_count = seed[pos]
                pos += 1
            ring_laws = {}

            if rings_mode == 0:
                radii = [0, 1] + [1 << i for i in range(1, ring_count - 1)] if ring_count > 1 else [0] if ring_count == 1 else []
                for r in radii[:ring_count]:
                    ring_seed = decode_seed_direct(seed[pos:])
                    ring_laws[r] = ring_seed
                    ring_seed_bytes = encode_seed_direct(ring_seed)
                    pos += len(ring_seed_bytes)
            elif rings_mode == 1:
                for _ in range(ring_count):
                    r = struct.unpack('>I', seed[pos:pos+4])[0]
                    pos += 4
                    ring_seed = decode_seed_direct(seed[pos:])
                    ring_laws[r] = ring_seed
                    ring_seed_bytes = encode_seed_direct(ring_seed)
                    pos += len(ring_seed_bytes)
            else:
                raise ValueError(f"Unknown D9 rings_mode: {rings_mode}")

            # If limit-closure meta-law is present, attach decoded rings to meta.
            if isinstance(meta, dict) and meta.get('type') == 'D9_LIMIT_CAUSAL_CLOSURE':
                meta['ring_laws'] = ring_laws
                meta['radii_defined'] = sorted(ring_laws.keys())

            out_params = {
                'center': center,
                'ring_laws': ring_laws,
                'structural_hash': structural_hash,
                'magic': magic,
                'completion': completion,
            }
            if flags & 0x08:
                out_params['sampled'] = True
            if meta is not None:
                out_params['meta'] = meta

            return {'family': 'D9_RADIAL', 'params': out_params, 'n': n}

        # v1 legacy decode
        has_hash = seed[pos]
        pos += 1
        structural_hash = ''
        if has_hash:
            hash_len = seed[pos]
            pos += 1
            structural_hash = seed[pos:pos+hash_len].hex()
            pos += hash_len

        magic_len = seed[pos]
        pos += 1
        magic = ''
        if magic_len > 0:
            magic = seed[pos:pos+magic_len].hex()
            pos += magic_len

        rings_mode = seed[pos]
        pos += 1
        ring_count = seed[pos]
        pos += 1
        ring_laws = {}

        if rings_mode == 0:
            radii = [0, 1] + [1 << i for i in range(1, ring_count - 1)] if ring_count > 1 else [0] if ring_count == 1 else []
            for r in radii[:ring_count]:
                ring_seed = decode_seed_direct(seed[pos:])
                ring_laws[r] = ring_seed
                ring_seed_bytes = encode_seed_direct(ring_seed)
                pos += len(ring_seed_bytes)
        elif rings_mode == 1:
            for _ in range(ring_count):
                r = struct.unpack('>I', seed[pos:pos+4])[0]
                pos += 4
                ring_seed = decode_seed_direct(seed[pos:])
                ring_laws[r] = ring_seed
                ring_seed_bytes = encode_seed_direct(ring_seed)
                pos += len(ring_seed_bytes)
        else:
            raise ValueError(f"Unknown D9 rings_mode: {rings_mode}")

        return {'family': 'D9_RADIAL', 'params': {
            'center': center,
            'ring_laws': ring_laws,
            'structural_hash': structural_hash,
            'magic': magic
        }, 'n': n}

    elif law_id == 0x29:
        # D9_INSTANT_DEDUCTION: [0x29][header][s0][r0][ds][dr]
        pos = params_start
        if pos + 4 > len(seed):
            raise ValueError('D9_INSTANT_DEDUCTION truncated params')
        s0 = int(seed[pos])
        r0 = int(seed[pos + 1])
        ds = int(seed[pos + 2])
        dr = int(seed[pos + 3])
        return {'family': 'D9_INSTANT_DEDUCTION', 'params': {'s0': s0, 'r0': r0, 'ds': ds, 'dr': dr}, 'n': n}
    
    elif law_id == 0x11:
        # D11_STRUCTURAL_HASH
        from D11_structural_hash import decode_d11_params
        params, _ = decode_d11_params(seed, params_start)
        return {'family': 'D11_STRUCTURAL_HASH', 'params': params, 'n': n}

    elif law_id == 0x12:
        # D10_RECURRENCE
        pos = params_start
        m, pos = _decode_uvarint(seed, pos)
        sub_len, pos = _decode_uvarint(seed, pos)
        end = pos + sub_len
        if end > len(seed):
            raise ValueError('D10_RECURRENCE truncated sub-seed')
        sub_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D10_RECURRENCE', 'params': {'m': int(m), 'sub_seed': sub_seed}, 'n': n}

    elif law_id == 0x13:
        # D11_RADIAL_RECURRENCE
        pos = params_start
        if pos + 4 > len(seed):
            raise ValueError('D11_RADIAL_RECURRENCE missing center')
        center = struct.unpack('>I', seed[pos:pos+4])[0]
        pos += 4
        radial_len, pos = _decode_uvarint(seed, pos)
        end = pos + radial_len
        if end > len(seed):
            raise ValueError('D11_RADIAL_RECURRENCE truncated radial seed')
        radial_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D11_RADIAL_RECURRENCE', 'params': {'center': int(center), 'radial_seed': radial_seed}, 'n': n}

    elif law_id == 0x14:
        # D12_SELF_AFFINE
        pos = params_start
        alpha, pos = _decode_uvarint(seed, pos)
        beta, pos = _decode_uvarint(seed, pos)
        base_len, pos = _decode_uvarint(seed, pos)
        end = pos + base_len
        if end > len(seed):
            raise ValueError('D12_SELF_AFFINE truncated base seed')
        base_seed = decode_seed_direct(seed[pos:end])
        return {'family': 'D12_SELF_AFFINE', 'params': {'alpha': int(alpha), 'beta': int(beta), 'base_seed': base_seed}, 'n': n}
    
    elif law_id == 0xFF:
        # D11_RAW: raw data
        data = list(seed[params_start:params_start+n])
        return {'family': 'D11_RAW', 'params': {'data': data}, 'n': n}
    
    else:
        raise ValueError(f"Unknown law_id: {law_id:#x}")
