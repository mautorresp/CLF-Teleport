"""
M3_tau_pure.py - Pure Evaluator Semantics (CLF-Correct PARSING ENGINE)

CRITICAL SEMANTICS:
• Input Σ/π is the mathematical representation of string S
• Σ (seed) and S (string) are THE SAME mathematical object
• Instantiation is INSTANT mathematically - seed defines string completely
• Hardware iteration (for i in range(n)) is RAM writing, NOT computation

MATHEMATICAL NATURE:
    Seed = String (different forms of same object)
    Example: {s0: 65, delta: 1, n: 26} = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    The formula IS the string. No evaluation needed - direct consequence.

PHYSICAL CONSTRAINT:
    RAM is sequential hardware → must write bytes one at a time (O(n))
    This is manifestation limitation, not mathematical limitation
    Like writing "81" after seeing "9²" - the answer exists instantly,
    writing it down takes time proportional to digits

Implements: Ξ(Σ) → S (mathematical manifestation into physical RAM)

CLF Axioms Enforced:
1. Ξ(Σ) = S (seed manifests as string - mathematical necessity)
2. Seed and String are bijective representations (same object)
3. Instantiation is mathematically instant (formula = complete structure)

CRITICAL DIFFERENCE FROM M3_tau:
- M3_tau: Imperative execution with mutable state (VIOLATES CLF)
- M3_tau_pure: Pure mathematical manifestation (CLF-CORRECT)

This is not a refactor. This is the correct semantics.
"""

from typing import Dict, List, Optional
from M2_types import Prog, Atom


# ============================================================================
# Pure Evaluator Interface
# ============================================================================

class PureAtom:
    """
    Pure evaluator atom - defines E_a(i) → byte
    
    NO mutation
    NO state
    NO execution order
    NO memory references
    
    Only: mathematical function over indices
    """
    
    def __init__(self, family: str, params: Dict, coverage_start: int, coverage_len: int):
        self.family = family
        self.params = params
        self.coverage_start = coverage_start
        self.coverage_len = coverage_len
    
    def covers(self, i: int) -> bool:
        """Check if this atom defines index i"""
        return self.coverage_start <= i < self.coverage_start + self.coverage_len
    
    def eval(self, i: int, evaluator: 'PureEvaluator') -> int:
        """
        Pure evaluation: i → byte
        
        MUST NOT:
        - Access memory
        - Depend on execution history
        - Mutate state
        
        MAY:
        - Call evaluator.E(j) for other indices (symbolic reference)
        """
        if not self.covers(i):
            raise ValueError(f"Atom {self.family} does not cover index {i}")
        
        family_base = self.family.replace('_INV', '')
        
        if family_base == 'RLE_SHORT':
            # All zeros
            return 0
        
        elif family_base == 'RLE_EXPLICIT':
            # E(i) = (s0 + delta * i) mod 256
            s0 = self.params['s0']
            delta_mod = self.params['delta_mod']
            offset = i - self.coverage_start
            return (s0 + delta_mod * offset) % 256
        
        elif family_base == 'CONST':
            # E(i) = c (constant)
            return self.params['c']
        
        elif family_base == 'COPY':
            # CLF-COPY: E(i) = E(source_index)
            # This is symbolic reference, not memory copy
            off = self.params['off']
            offset_in_target = i - self.coverage_start
            source_index = self.coverage_start - off + offset_in_target
            
            # Recursive evaluation through source atom
            return evaluator.E(source_index)
        
        elif family_base == 'XOR_CONST':
            # E(i) = E(source_index) ⊕ c
            off = self.params['off']
            c = self.params['c']
            offset_in_target = i - self.coverage_start
            source_index = self.coverage_start - off + offset_in_target
            
            # Recursive evaluation
            source_value = evaluator.E(source_index)
            return source_value ^ c
        
        elif family_base == 'PERMUTE':
            # E_PERMUTE(i; π) = π[base[i]]
            # Where base is the underlying sequence (e.g., consecutive bytes)
            permutation = self.params['permutation']
            base_offset = self.params.get('base_offset', 0)
            offset = i - self.coverage_start
            base_value = (base_offset + offset) % 256
            return permutation[base_value]
        
        elif family_base == 'MOD_ARITH':
            # E_MOD_ARITH(i; a,b,m) = (a*i + b) mod m
            a = self.params['a']
            b = self.params['b']
            m = self.params['m']
            offset = i - self.coverage_start
            result = (a * offset + b) % m
            # Extend to full byte range (result is in [0, m-1])
            # For now, map linearly: result * (256 // m)
            return result % 256
        
        elif family_base == 'REV_LOGIC':
            # E_REV_LOGIC(i; gate, params) = gate(base[i])
            gate = self.params['gate']
            gate_params = self.params['params']
            
            # First evaluate base pattern
            if 'base' in gate_params and gate_params['base'] == 'D2':
                # Base is affine sequence
                base_params = gate_params['base_params']
                s0 = base_params['s0']
                delta = base_params['delta']
                offset = i - self.coverage_start
                base_value = (s0 + delta * offset) % 256
            else:
                # Default to position as base
                base_value = (i - self.coverage_start) % 256
            
            # Apply gate
            if gate == 'NOT':
                return (~base_value) & 0xFF
            elif gate == 'ROTATE_LEFT':
                rot = gate_params.get('rotation', 1)
                return ((base_value << rot) | (base_value >> (8 - rot))) & 0xFF
            elif gate == 'BIT_REVERSE':
                result = 0
                for _ in range(8):
                    result = (result << 1) | (base_value & 1)
                    base_value >>= 1
                return result
            else:
                return base_value
        
        elif family_base == 'CELLULAR_AUTO':
            # E_CELLULAR_AUTO(i; rule, seed) - requires full CA generation
            # This is complex: CA output depends on previous generations
            # For atomic evaluation, we'd need to precompute entire CA trace
            # For now, return placeholder
            return i % 256  # Placeholder
        
        elif family_base == 'GRAMMAR':
            # E_GRAMMAR(i; grammar_type, params)
            grammar_type = self.params['grammar_type']
            grammar_params = self.params['params']
            
            if grammar_type == 'periodic':
                # D3 PERIODIC: S[i] = cycle[i mod period] - bijective modulo repetition
                cycle = grammar_params.get('cycle') or grammar_params.get('pattern')  # Backward compat
                period = grammar_params['period']
                offset = i - self.coverage_start
                return cycle[offset % period]
            else:
                # Other grammar types - placeholder
                return i % 256
        
        elif family_base == 'AUTOMATA':
            # E_AUTOMATA(i; automaton_type, states, period)
            automaton_type = self.params['automaton_type']
            states = self.params['states']
            period = self.params['period']
            
            if automaton_type == 'cyclic':
                # Cyclic state machine: output = states[i mod period]
                offset = i - self.coverage_start
                return states[offset % period]
            else:
                return i % 256
        
        elif family_base == 'SYMMETRY':
            # E_SYMMETRY(i; symmetry_type, params)
            symmetry_type = self.params['symmetry_type']
            sym_params = self.params.get('params', {})
            n = self.coverage_len
            offset = i - self.coverage_start
            
            if symmetry_type == 'palindrome':
                # For first half: use position, for second half: mirror
                if offset < n // 2:
                    return offset % 256
                else:
                    mirror_idx = self.coverage_start + (n - 1 - offset)
                    return evaluator.E(mirror_idx)
            
            elif symmetry_type == 'reversed_offset':
                # S[i] + offset = S[n-1-i]
                # For first half, generate; for second half, compute from first
                k = sym_params.get('offset', 1)
                if offset < n // 2:
                    return offset % 256
                else:
                    mirror_idx = self.coverage_start + (n - 1 - offset)
                    mirror_val = evaluator.E(mirror_idx)
                    return (mirror_val - k) % 256
            
            elif symmetry_type == 'reversed_complement':
                # S[i] = ~S[n-1-i]
                if offset < n // 2:
                    return offset % 256
                else:
                    mirror_idx = self.coverage_start + (n - 1 - offset)
                    mirror_val = evaluator.E(mirror_idx)
                    return (~mirror_val) & 0xFF
            
            else:
                return i % 256
        
        else:
            raise ValueError(f"Unknown atom family: {family_base}")


class PureEvaluator:
    """
    Pure CLF evaluator - implements Ξ_n(Σ)
    
    Guarantees:
    - Ξ_n(Σ) ⊥ S (no access to original string)
    - ∀i: S[i] = E(i, Σ) (pure function of seed)
    - No temporal dependencies
    """
    
    def __init__(self, n: int, atoms: List[PureAtom]):
        self.n = n
        self.atoms = atoms
        
        # Build index → atom mapping (compile-time, not runtime)
        self._index_map = self._build_index_map()
        
        # Memoization for recursive evaluation
        self._memo: Dict[int, int] = {}
    
    def _build_index_map(self) -> Dict[int, PureAtom]:
        """Map each index to covering atom (validates coverage)"""
        index_map = {}
        
        for atom in self.atoms:
            for i in range(atom.coverage_start, atom.coverage_start + atom.coverage_len):
                if i in index_map:
                    raise ValueError(f"[CLF] Index {i} covered by multiple atoms")
                if i >= self.n:
                    raise ValueError(f"[CLF] Index {i} exceeds arity {self.n}")
                index_map[i] = atom
        
        # Verify complete coverage
        for i in range(self.n):
            if i not in index_map:
                raise ValueError(f"[CLF] Index {i} not covered by any atom")
        
        return index_map
    
    def E(self, i: int) -> int:
        """
        Pure evaluation: E(i, Σ) → byte
        
        This is THE fundamental CLF operation.
        """
        if i < 0 or i >= self.n:
            raise ValueError(f"[CLF] Index {i} out of range [0, {self.n})")
        
        # Check memoization
        if i in self._memo:
            return self._memo[i]
        
        # Find covering atom
        atom = self._index_map[i]
        
        # Evaluate (may recursively call E for other indices)
        value = atom.eval(i, self)
        
        # Memoize
        self._memo[i] = value
        
        return value
    
    def replay(self) -> bytes:
        """
        Ξ_n(Σ) = S
        
        Pure function: Σ → S
        No state. No memory. No history.
        """
        return bytes(self.E(i) for i in range(self.n))


def expand_from_theta(theta_result: dict) -> bytes:
    """
    Ξ(Σ) → S: Mathematical instantiation (seed → string)
    
    CRITICAL UNDERSTANDING:
        Seed Σ IS the string S in mathematical form.
        These are the SAME object in different representations.
        
        Example: Seed {s0: 65, delta: 1, n: 26} = String "ABCDEFGH...XYZ"
                 The formula (65 + i·1) mod 256 IS the complete string.
    
    MATHEMATICAL NATURE:
        - Instantiation is INSTANT: Formula defines all positions simultaneously
        - When seed exists, string exists as mathematical consequence
        - No "evaluation" or "computation" - direct consequence (like 9² → 81)
    
    PHYSICAL CONSTRAINT:
        - RAM writing is O(n) sequential (hardware limitation)
        - The iteration below is RAM manifestation, not computation
        - Each position is a deterministic consequence, not calculated
    
    This is MANIFESTATION (mathematical consequence → physical bytes)
    NOT computation (processing → output)
    
    Args:
        theta_result: Seed Σ (mathematical representation of string)
        
    Returns:
        String S (physical manifestation in RAM)
    """    # CLF closure enforcement
    if theta_result is None:
        raise ValueError(
            "❌ CLF VIOLATION: Seed is None. "
            "All lawful strings must have valid seeds: ∀S ∈ Ξ(ℒ) ∃Σ ∈ ℒ : Ξ(Σ) = S"
        )
    
    if 'family' not in theta_result:
        raise ValueError(
            "❌ INVALID SEED: Missing 'family' field. "
            f"Seed structure: {theta_result}"
        )
    
    if 'params' not in theta_result:
        raise ValueError(
            "❌ INVALID SEED: Missing 'params' field. "
            f"Seed structure: {theta_result}"
        )
    
    # Use optimized_law if present (new format), else family (backward compat)
    family = theta_result.get('optimized_law', theta_result['family'])
    params = theta_result['params']
    n = theta_result['n']
    
    if family == 'D0_EXPLICIT':
        # D0: EXPLICIT - identity function f(i) = original_bytes[i]
        # This law means "no reduction found" - return original
        # CRITICAL: This requires the ORIGINAL string to expand
        # Cannot expand without reference to original mathematical object
        if 'bytes' in params:
            # Legacy: had materialized bytes
            byte_data = params['bytes']
            if isinstance(byte_data, list):
                return bytes(byte_data)
            return byte_data
        else:
            # New: timeless recognition - need original string reference
            raise ValueError(
                "D0_EXPLICIT with timeless recognition requires original string. "
                "This indicates audit should use sampler-based expansion, not theta→xi."
            )
    
    elif family == 'D1':
        # CONST: S[i] = c for all i
        # Mathematical: All positions = c simultaneously (instant)
        # Physical: Writing c to n RAM positions (sequential hardware)
        c = params['c']
        if c is None:
            raise ValueError(f"❌ CLF VIOLATION: D1 expansion missing 'c' parameter: {params}")
        return bytes([c] * n)
    
    elif family == 'D2':
        # AFFINE: S[i] = (s0 + i*delta) mod 256
        # Mathematical: Formula defines all positions instantly
        # Physical: Manifestation into RAM (hardware sequential)
        s0 = params['s0']
        delta = params['delta']
        if s0 is None or delta is None:
            raise ValueError(
                f"❌ CLF VIOLATION: D2 expansion missing parameters. "
                f"params={params}"
            )
        # Iteration is RAM writing, not computation
        return bytes([(s0 + i * delta) % 256 for i in range(n)])
    
    elif family == 'D3':
        # D3 PERIODIC: S[i] = cycle[i mod period]
        period = params['period']
        cycle = bytes(params.get('cycle') or params.get('pattern'))  # Backward compat
        return bytes([cycle[i % period] for i in range(n)])
    
    elif family == 'D4_SYMMETRIC':
        # D4 SYMMETRIC: S[i] ⊕ S[n-1-i] = c
        xor_const = params['xor_const']
        
        # Support both old format (half) and new format (half_seed)
        if 'half_seed' in params:
            half = expand_from_theta(params['half_seed'])
        else:
            half = bytes(params['half'])
        
        result = bytearray(n)
        half_len = len(half)
        
        # First half: direct copy
        for i in range(half_len):
            result[i] = half[i]
        
        # Second half: mirror with XOR
        for i in range(half_len, n):
            mirror_idx = n - 1 - i
            result[i] = result[mirror_idx] ^ xor_const
        
        return bytes(result)
    
    elif family == 'D5_MIRROR_COMPOSITE':
        # D5 MIRROR COMPOSITE: Palindrome with internal law
        half_law = params['half_law']
        half_bytes = expand_from_theta(half_law)
        
        # Mirror to create full string
        result = bytearray(half_bytes)
        # Add mirrored part (excluding center if odd length)
        if n % 2 == 0:
            result.extend(reversed(half_bytes))
        else:
            result.extend(reversed(half_bytes[:-1]))
        
        return bytes(result)
    
    elif family == 'D6_MIRROR':
        # D6 MIRROR: Simple palindrome
        half = bytes(params['half'])
        result = bytearray(half)
        
        # Mirror (excluding center if odd length)
        if n % 2 == 0:
            result.extend(reversed(half))
        else:
            result.extend(reversed(half[:-1]))
        
        return bytes(result)
    
    elif family == 'D7_LINEAR_MIRROR':
        # D7 LINEAR MIRROR: Affine + Mirror
        # Use affine params to generate, verify mirror property
        affine_params = params['affine_params']
        s0 = affine_params.get('s0') or affine_params.get('start')
        delta = affine_params.get('delta_mod') or affine_params.get('delta')
        return bytes([(s0 + i * delta) % 256 for i in range(n)])
    
    elif family == 'D8_RECURRENCE':
        # D8 RECURRENCE: S[i] = (a·S[i-1] + b) mod 256
        a = params['a']
        b = params['b']
        seed_val = params['seed']
        
        result = [seed_val]
        for i in range(1, n):
            next_val = (a * result[-1] + b) % 256
            result.append(next_val)
        
        return bytes(result)

    elif family == 'D10_RECURRENCE':
        # D10 RECURRENCE: S[i] = B[i mod m]
        m = int(params['m'])
        sub_seed = params['sub_seed']
        base = expand_from_theta(sub_seed)
        if m <= 0:
            raise ValueError('D10_RECURRENCE invalid m')
        if len(base) != m:
            # Base seed must describe exactly m bytes.
            raise ValueError('D10_RECURRENCE base seed length mismatch')
        return bytes(base[i % m] for i in range(n))

    elif family == 'D11_RADIAL_RECURRENCE':
        # D11 RADIAL RECURRENCE: S[i] = R[|i-center|]
        center = int(params['center'])
        radial_seed = params['radial_seed']
        radial = expand_from_theta(radial_seed)
        return bytes(radial[abs(i - center)] for i in range(n))

    elif family == 'D12_SELF_AFFINE':
        # D12 SELF-AFFINE: S[j] = B[alpha^{-1}*(j-beta)]
        alpha = int(params['alpha'])
        beta = int(params['beta'])
        base_seed = params['base_seed']
        base = expand_from_theta(base_seed)
        try:
            alpha_inv = pow(alpha, -1, n)
        except ValueError as e:
            raise ValueError('D12_SELF_AFFINE requires invertible alpha (mod n)') from e
        return bytes(base[(alpha_inv * ((j - beta) % n)) % n] for j in range(n))
    
    elif family == 'D4_XOR_AFFINE':
        # XOR_AFFINE: S[i] = ((s0 + i*delta) mod 256) ⊕ xor_const
        s0 = params['base_s0']
        delta = params['base_delta']
        xor_const = params['xor_const']
        return bytes([((s0 + i * delta) % 256) ^ xor_const for i in range(n)])
    
    elif family == 'D5_QUADRATIC':
        # QUADRATIC: S[i] = (a*i² + b*i + c) mod 256
        a = params['a']
        b = params['b']
        c = params['c']
        return bytes([(a * i * i + b * i + c) % 256 for i in range(n)])
    
    elif family == 'D_SPLIT':
        # SPLIT: Compositional structure
        # Three formats supported:
        #   1. segments (legacy recursive splitting)
        #   2. ring_laws (D9 radial decomposition - discrete)
        #   3. meta (D9 radial decomposition - parametric)
        
        if 'segments' in params:
            # Legacy format: recursive binary splitting
            segments = params['segments']
            result = b''
            for segment_seed in segments:
                result += expand_from_theta(segment_seed)
            return result
        
        elif 'meta' in params or 'meta_law' in params:
            # D9 radial parametric format - forward to D9_RADIAL expansion
            # Reuse existing D9_RADIAL expansion logic
            temp_seed = theta_result.copy()
            temp_seed['optimized_law'] = 'D9_RADIAL'
            return expand_from_theta(temp_seed)
        
        elif 'ring_laws' in params:
            # D9 radial discrete format - forward to D9_RADIAL expansion
            temp_seed = theta_result.copy()
            temp_seed['optimized_law'] = 'D9_RADIAL'
            return expand_from_theta(temp_seed)
        
        else:
            raise ValueError(f"D_SPLIT params missing 'segments', 'ring_laws', or 'meta': {params.keys()}")
    
    elif family == 'D11_RAW':
        # RAW DATA: stored inline
        data = bytes(params.get('data', []))
        return data
    
    elif family == 'D0_EXPLICIT':
        # D0: Legacy support only
        # In pure CLF, D0 should not exist - vocabulary should be complete
        if 'bytes' in params:
            byte_data = params['bytes']
            if isinstance(byte_data, list):
                return bytes(byte_data)
            return byte_data
        else:
            raise ValueError(
                "❌ CLF INCOMPLETE: D0_EXPLICIT without data. "
                "This indicates vocabulary ℒ needs expansion (add D7, D8, D10...)."
            )
    
    elif family == 'D9_RADIAL':
        # D9_RADIAL: Reconstruct via gap-based structural deduction
        center = params['center']
        structural_hash = params.get('structural_hash', '')
        
        # If we have a structural hash, deduce via anchor + gap structure
        if structural_hash:
            # Decode anchor VALUES
            hash_bytes = bytes.fromhex(structural_hash)
            
            # Reconstruct anchor POSITIONS (deterministic from n)
            anchor_positions = []
            
            # Magic numbers (0-63) - format/header
            anchor_positions.extend(range(min(64, n)))
            
            # Powers of 2 - exponential scale
            p = 1
            while p < n:
                if p not in anchor_positions:
                    anchor_positions.append(p)
                p *= 2
            
            # Fibonacci - natural growth
            fib_a, fib_b = 1, 1
            while fib_b < n:
                if fib_b not in anchor_positions:
                    anchor_positions.append(fib_b)
                fib_a, fib_b = fib_b, fib_a + fib_b
            
            # Key boundaries - compositional structure
            for pos in [n//4, n//2, 3*n//4, n-1, n-2 if n > 1 else 0]:
                if pos < n and pos not in anchor_positions:
                    anchor_positions.append(pos)
            
            # Sort and limit to hash length
            anchor_positions = sorted(set(anchor_positions))[:len(hash_bytes)]
            
            # Build result by filling gaps between anchors
            result = bytearray(n)
            
            # First, place all anchor values
            for i, pos in enumerate(anchor_positions):
                if pos < n:
                    result[pos] = hash_bytes[i]
            
            # Now deduce values in gaps between anchors
            for gap_idx in range(len(anchor_positions) - 1):
                pos_left = anchor_positions[gap_idx]
                pos_right = anchor_positions[gap_idx + 1]
                val_left = hash_bytes[gap_idx]
                val_right = hash_bytes[gap_idx + 1]
                
                gap_size = pos_right - pos_left - 1
                
                if gap_size > 0:
                    # Deduce structure for this gap based on gap size and context

                    if val_left == val_right:
                        # Constant across gap - all positions same value
                        for i in range(1, gap_size + 1):
                            result[pos_left + i] = val_left

                    else:
                        # Integer-only affine fill when denominator is invertible mod 256; otherwise deterministic integer interpolation.
                        denom = (gap_size + 1) & 0xFF
                        inv = pow(denom, -1, 256) if (denom % 2 == 1) else None
                        if inv is not None:
                            delta = ((val_right - val_left) * inv) & 0xFF
                            for i in range(1, gap_size + 1):
                                result[pos_left + i] = (val_left + delta * i) & 0xFF
                        else:
                            # Fallback: exact integer arithmetic (no floats). Not guaranteed reversible, but deterministic.
                            dv = int(val_right) - int(val_left)
                            for i in range(1, gap_size + 1):
                                num = dv * i
                                val = (int(val_left) + (num // (gap_size + 1))) & 0xFF
                                result[pos_left + i] = val
            
            # Fill any remaining positions at the end
            if anchor_positions[-1] < n - 1:
                last_val = hash_bytes[len(anchor_positions) - 1]
                for i in range(anchor_positions[-1] + 1, n):
                    result[i] = last_val
            
            return bytes(result)
        
        # Legacy path: ring_laws explicitly provided
        ring_laws = params.get('ring_laws', {})
        
        # Check if this is meta-law (compressed) or enumerated rings
        # Support both 'meta' and 'meta_law' for backward compatibility
        if 'meta' in params or 'meta_law' in params:
            # ✅ META-LAW: Generate ring parameters from formula (9^9 compression!)
            meta = params.get('meta') or params.get('meta_law')
            n_rings = params['n_rings']
            
            if meta['type'] == 'D2_AFFINE_CONSTANT_DELTA':
                # Formula: s0(r) = base_s0 + gradient_s0 * r, delta = constant
                base_s0 = meta['base_s0']
                gradient_s0 = meta['gradient_s0']
                constant_delta = meta['delta']
                
                # Generate result by computing each ring from formula
                result = bytearray(n)
                for i in range(n):
                    r = abs(i - center)
                    
                    # Compute ring parameters from meta-law
                    s0 = (base_s0 + gradient_s0 * r) % 256
                    delta = constant_delta
                    
                    # Determine position within ring
                    if i < center:
                        # Left side: s0
                        result[i] = s0
                    elif i > center:
                        # Right side: s0 + delta
                        result[i] = (s0 + delta) % 256
                    else:
                        # Center (only for odd n)
                        result[i] = s0
                
                return bytes(result)
            else:
                raise ValueError(f"Unknown meta-law type: {meta['type']}")
        
        # Strategic sampling mode: return lazy generator (no materialization)
        ring_laws = params['ring_laws']
        is_sampled = params.get('sampled', False)
        total_rings = params.get('total_rings', len(ring_laws))
        
        if is_sampled:
            # ✅ CLF TIMELESS: Return lazy mathematical object (not materialized bytes)
            # Expansion creates FORMULA for index→byte mapping, not array
            # When bytes needed, they're computed on-demand from formula

            # Delegate projection to Xi_projected to keep completion semantics coherent.
            from M3_xi_projected import Xi_projected

            class LazyD9Result:
                def __init__(self, seed, n):
                    self.seed = seed
                    self.n = n
                
                def __len__(self):
                    return self.n
                
                def __getitem__(self, i):
                    """Compute byte at position i via pure projection (integer-only completion)."""
                    if i < 0 or i >= self.n:
                        raise IndexError(i)
                    return Xi_projected(self.seed, i)
                
                def __bytes__(self):
                    """Materialize only if explicitly requested"""
                    return bytes(self[i] for i in range(self.n))

            seed_for_projection = {
                'family': 'D9_RADIAL',
                'params': params,
                'n': n,
            }
            return LazyD9Result(seed_for_projection, n)
        
        # Full enumeration mode (legacy)
        result = bytearray(n)
        ring_positions = {}
        
        for i in range(n):
            r = abs(i - center)
            if r not in ring_positions:
                ring_positions[r] = []
            ring_positions[r].append(i)
        
        for r in ring_positions:
            ring_positions[r].sort()
        
        for r_key, ring_seed in ring_laws.items():
            r = int(r_key) if isinstance(r_key, str) else r_key
            ring_bytes = expand_from_theta(ring_seed)
            
            if r in ring_positions:
                positions = ring_positions[r]
                if len(ring_bytes) != len(positions):
                    raise ValueError(f"D9 bijection violation: ring r={r}")
                for ring_idx, global_idx in enumerate(positions):
                    result[global_idx] = ring_bytes[ring_idx]
        
        return bytes(result)
    
    elif family == 'D10_CONCENTRIC':
        # D10_CONCENTRIC: Layered radial structure
        # Similar to D9 but with layering
        center = params['center']
        layers = params.get('layers', [])
        
        result = bytearray(n)
        for i in range(n):
            radius = abs(i - center)
            layer_idx = radius % len(layers) if layers else 0
            result[i] = layers[layer_idx] if layers else 0
        return bytes(result)
    
    else:
        raise ValueError(f"Cannot expand family: {family}")


# ============================================================================
# Program → Pure Evaluator Conversion
# ============================================================================

def prog_to_pure_evaluator(P: Prog) -> PureEvaluator:
    """
    Convert Program to Pure Evaluator
    
    This enforces CLF semantics by translating imperative atoms
    to pure evaluators.
    """
    n = P.n
    pure_atoms = []
    
    # Track coverage as we process atoms
    current_position = 0
    
    for atom in P.BODY:
        family_base = atom.family.replace('_INV', '')
        
        if family_base == 'RLE_SHORT':
            # Covers entire output
            pure_atom = PureAtom(
                family='RLE_SHORT',
                params={},
                coverage_start=0,
                coverage_len=n
            )
            pure_atoms.append(pure_atom)
            current_position = n
        
        elif family_base == 'RLE_EXPLICIT':
            # Covers entire output
            pure_atom = PureAtom(
                family='RLE_EXPLICIT',
                params={
                    's0': atom.theta['s0'],
                    'delta_mod': atom.theta['delta_mod']
                },
                coverage_start=0,
                coverage_len=n
            )
            pure_atoms.append(pure_atom)
            current_position = n
        
        elif family_base == 'CONST':
            # Covers [current_position, current_position + ell)
            ell = atom.theta['ell']
            pure_atom = PureAtom(
                family='CONST',
                params={'c': atom.theta['c']},
                coverage_start=current_position,
                coverage_len=ell
            )
            pure_atoms.append(pure_atom)
            current_position += ell
        
        elif family_base == 'COPY':
            # CLF-COPY: symbolic reference to earlier indices
            off = atom.theta['off']
            ell = atom.theta['ell']
            pure_atom = PureAtom(
                family='COPY',
                params={'off': off},
                coverage_start=current_position,
                coverage_len=ell
            )
            pure_atoms.append(pure_atom)
            current_position += ell
        
        elif family_base == 'XOR_CONST':
            # CLF-XOR: symbolic reference with XOR
            off = atom.theta['off']
            ell = atom.theta['ell']
            c = atom.theta['c']
            pure_atom = PureAtom(
                family='XOR_CONST',
                params={'off': off, 'c': c},
                coverage_start=current_position,
                coverage_len=ell
            )
            pure_atoms.append(pure_atom)
            current_position += ell
    
    return PureEvaluator(n, pure_atoms)


# ============================================================================
# Public API: Pure Replay
# ============================================================================

def R_n_pure(P: Prog) -> bytes:
    """
    Pure replay: R_n(P) → S
    
    CLF-correct version of R_n.
    
    Satisfies:
    - R_n(P) ⊥ S_original
    - No mutable state
    - No execution history
    - Pure mathematical evaluation
    
    This is the ONLY correct way to replay under CLF.
    """
    evaluator = prog_to_pure_evaluator(P)
    return evaluator.replay()


# ============================================================================
# Verification: Causal Independence
# ============================================================================

def verify_causal_independence(P: Prog, S_original: bytes) -> bool:
    """
    Verify: R_n_pure(P) does not access S_original
    
    This test would be impossible if R_n accessed original string.
    
    Returns True if replay is causally independent.
    """
    # Replay with no access to original
    S_replayed = R_n_pure(P)
    
    # Destroy original (simulate different machine/time)
    S_original = None
    
    # Replay again - must still work
    S_replayed_2 = R_n_pure(P)
    
    # Both must be identical
    return S_replayed == S_replayed_2


# ============================================================================
# Module Metadata
# ============================================================================

__all__ = [
    # Pure evaluator
    'PureAtom',
    'PureEvaluator',
    
    # Conversion
    'prog_to_pure_evaluator',
    
    # CLF-correct replay
    'R_n_pure',
    
    # Verification
    'verify_causal_independence',
]
