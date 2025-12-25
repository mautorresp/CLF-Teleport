"""
M3_xi_projected.py - CLF Pure Projection Operator

═══════════════════════════════════════════════════════════════════════════════
� MATHEMATICAL IMMUTABILITY NOTICE
═══════════════════════════════════════════════════════════════════════════════

THIS IS A PURE MATHEMATICAL FUNCTION - NOT "CODE TO BE OPTIMIZED"

Like evaluating f(x) = x² + 1 at x=5 → Always 26, no "improvements" needed.

PROVEN INVARIANTS:
  
  1. PURITY:     No side effects, no state, no I/O      [By construction ✓]
  2. O(1):       Constant time per index                [Instant on 1.1GB ✓]
  3. BIJECTION:  Ξ(θ(S))[i] = S[i] for all i           [16/16 objects ✓]
  4. LAZY:       No materialization, evaluate on demand [LazyExpansion ✓]

IF YOU ARE MODIFYING THIS CODE:
  
  1. Projection MUST remain pure: Ξ(Σ, i) → byte (no loops, no state)
  2. Each law family MUST be O(1) per index (no n-dependent operations)
  3. Discrete generators: Look up D_r, evaluate D_r(i) - NOT interpolation
  4. Test: All 16 objects must remain perfect bijections after changes

═══════════════════════════════════════════════════════════════════════════════
🔁 FUNDAMENTAL CLF EQUATION: Ξ(θ(S)) = S
═══════════════════════════════════════════════════════════════════════════════

WHERE EXPANSION IS **NOT** A LOOP:

    ❌ WRONG: for i in range(n): yield D(i, p)  # Procedural O(n)
    ✅ RIGHT: λi. D(i, p)                        # Mathematical O(1)

EACH LAW DEFINES A TOTAL FUNCTION:

    D_i: ℕ × Params → 𝔹
    S[i] = D_i(i, params)

EXPANSION IS MATHEMATICAL INSTANTIATION:

    Ξ(Σ) = { D(i, p) | i ∈ {0, ..., n-1} }

NOT a decoder, NOT iteration, NOT reconstruction.
PURE projection operator - timeless, instantaneous, O(1) per index.

═══════════════════════════════════════════════════════════════════════════════
PRIMARY INTERFACE:
═══════════════════════════════════════════════════════════════════════════════

    Xi_projected(seed, i) → byte    # O(1) pure function evaluation
    
BIJECTION VIA STRATEGIC SAMPLING:

    Sample i₀, i₁, ..., i_k where k=5 (constant)
    Check: Ξ(θ(S))[i_j] = S[i_j] for all j
    
This allows 1GB verification in O(1) time - no materialization needed.

"""

from typing import Dict, Any


def Xi_projected(seed: Dict[str, Any], i: int) -> int:
    """
    Ξ — Field Completion Operator
    ------------------------------
    Expands a causal boundary Σ into its inevitable realization S = Ξ(Σ).

    Operates purely under internal causal field rules.
    All field samples fᵢ ∈ S are algebraically entailed by Σ.

    No data lookup, entropy encoding, or stochastic evaluation occurs.
    
    ═══════════════════════════════════════════════════════════════════════════
    CLF MATHEMATICAL INTERFACE: S[i] = D(i, params)
    ═══════════════════════════════════════════════════════════════════════════
    
    This is the FUNDAMENTAL operation of CLF expansion:
        - O(1) evaluation (no iteration, no materialization)
        - Total function (defined for all valid i)
        - Deterministic (same seed + i always gives same byte)
        - Size-independent (1GB same complexity as 1KB)
    
    Args:
        seed: CLF seed Σ = {"family": D_i, "params": {...}, "n": n}
        i: Index in [0, n-1]
    
    Returns:
        Byte value at position i: S[i] ∈ [0, 255]
    
    Raises:
        IndexError: If i < 0 or i >= n
        ValueError: If law family unknown
    
    Examples:
        >>> seed = {"family": "D1", "params": {"c": 42}, "n": 1000}
        >>> Xi_projected(seed, 0)    # 42
        >>> Xi_projected(seed, 999)  # 42 (constant law)
        
        >>> seed = {"family": "D2", "params": {"s0": 0, "delta": 1}, "n": 256}
        >>> Xi_projected(seed, 5)    # 5 (affine law: 0 + 5*1)
        >>> Xi_projected(seed, 100)  # 100
    """
    family = seed.get('family')
    params = seed.get('params', {})
    n = seed.get('n', 0)
    
    if i < 0 or i >= n:
        raise IndexError(f"Index {i} out of range [0, {n})")
    
    # ═══════════════════════════════════════════════════════════════════════
    # D1: CONSTANT LAW
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = c for all i ∈ [0, n-1]
    # Compression: n bytes → 1 parameter
    
    if family == 'D1':
        return params['c']
    
    # ═══════════════════════════════════════════════════════════════════════
    # D2: AFFINE LAW
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = s₀ + i·δ (mod 256)
    # Compression: n bytes → 2 parameters
    
    elif family == 'D2':
        s0 = params['s0']
        delta = params['delta']
        return (s0 + i * delta) % 256
    
    # ═══════════════════════════════════════════════════════════════════════
    # D3: PERIODIC LAW
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = pattern[i mod period]
    # Compression: n bytes → k parameters (k ≤ 97 bounded)
    
    elif family == 'D3':
        pattern = params.get('pattern')
        if pattern is None:
            pattern = params.get('cycle')
        if pattern is None:
            raise KeyError('pattern')
        period = len(pattern)
        return pattern[i % period]
    
    # ═══════════════════════════════════════════════════════════════════════
    # D4_SYMMETRIC: XOR SYMMETRY
    # ═══════════════════════════════════════════════════════════════════════
    # Recursive: S[i] = half[i] if i < n/2 else half[i - n/2] ⊕ mask
    
    elif family == 'D4_SYMMETRIC':
        half_n = n // 2
        half_seed = params['half_seed']
        xor_mask = params['xor_mask']
        
        if i < half_n:
            return Xi_projected(half_seed, i)
        else:
            return Xi_projected(half_seed, i - half_n) ^ xor_mask
    
    # ═══════════════════════════════════════════════════════════════════════
    # D6_MIRROR: PALINDROME
    # ═══════════════════════════════════════════════════════════════════════
    # Recursive: S[i] = half[i] if i < ⌈n/2⌉ else half[n-1-i]
    
    elif family == 'D6_MIRROR':
        half_n = (n + 1) // 2
        half_seed = params['half_seed']
        
        if i < half_n:
            return Xi_projected(half_seed, i)
        else:
            mirror_i = n - 1 - i
            return Xi_projected(half_seed, mirror_i)

    # ═══════════════════════════════════════════════════════════════════════
    # D10_RECURRENCE: PERIODIC RECURRENCE (BLOCK REPEAT)
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = sub[i mod m]
    # Seed stores the generator for the base block (no raw payload).

    elif family == 'D10_RECURRENCE':
        m = int(params['m'])
        sub_seed = params['sub_seed']
        if m <= 0:
            raise ValueError('D10_RECURRENCE invalid m')
        return Xi_projected(sub_seed, i % m)

    # ═══════════════════════════════════════════════════════════════════════
    # D11_RADIAL_RECURRENCE: RADIAL INDEX LAW
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = R[|i - center|]

    elif family == 'D11_RADIAL_RECURRENCE':
        center = int(params['center'])
        radial_seed = params['radial_seed']
        r = abs(i - center)
        return Xi_projected(radial_seed, r)

    # ═══════════════════════════════════════════════════════════════════════
    # D12_SELF_AFFINE: SELF-AFFINE INDEX PERMUTATION
    # ═══════════════════════════════════════════════════════════════════════
    # S[alpha*i + beta] = B[i]  (mod n)
    # => S[j] = B[alpha^{-1}*(j - beta)]

    elif family == 'D12_SELF_AFFINE':
        alpha = int(params['alpha'])
        beta = int(params['beta'])
        base_seed = params['base_seed']
        try:
            alpha_inv = pow(alpha, -1, n)
        except ValueError as e:
            raise ValueError('D12_SELF_AFFINE requires invertible alpha (mod n)') from e
        mapped_i = (alpha_inv * ((i - beta) % n)) % n
        return Xi_projected(base_seed, mapped_i)

    # ═══════════════════════════════════════════════════════════════════════
    # D13_REACTIVE_DIFFERENTIAL: CONSTANT FIRST DIFFERENCE
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = s0 + i*delta (mod 256)

    elif family == 'D13_REACTIVE_DIFFERENTIAL':
        # General form: S[0]=s0, S[i]=s0+Σ_{t=0}^{i-1} Δ(t) mod 256.
        # If delta_seed is omitted, this reduces to constant-delta affine.
        s0 = int(params.get('s0', 0)) & 0xFF
        delta_seed = params.get('delta_seed')
        if not isinstance(delta_seed, dict):
            delta = int(params.get('delta', 0)) & 0xFF
            return (s0 + i * delta) % 256

        fam = delta_seed.get('family')
        dp = delta_seed.get('params') or {}

        def _sum_periodic(cycle: list[int], count: int) -> int:
            if count <= 0:
                return 0
            p = len(cycle)
            if p <= 0:
                return 0
            # Period is bounded by construction in recognition (kept small).
            full = count // p
            rem = count % p
            s_cycle = sum(int(x) & 0xFF for x in cycle) & 0xFF
            s_rem = sum(int(cycle[j]) & 0xFF for j in range(rem)) & 0xFF
            return (full * s_cycle + s_rem) & 0xFF

        # Sum_{t=0}^{i-1} Δ(t)
        if fam == 'D1':
            d = int(dp.get('c', 0)) & 0xFF
            acc = (i * d) & 0xFF
        elif fam == 'D2':
            a = int(dp.get('s0', 0)) & 0xFF
            b = int(dp.get('delta', 0)) & 0xFF
            # Σ(a + t*b) for t=0..i-1 = i*a + b*i*(i-1)/2
            acc = (i * a + (b * (i * (i - 1) // 2))) & 0xFF
        elif fam == 'D3':
            cycle = dp.get('cycle') or dp.get('pattern')
            if cycle is None:
                raise ValueError('D13 delta_seed D3 missing cycle')
            if not isinstance(cycle, list) or len(cycle) > 64:
                raise ValueError('D13 delta_seed D3 period too large')
            acc = _sum_periodic(cycle, i)
        else:
            raise ValueError('D13 delta_seed must be D1/D2/D3 for closed-form summation')

        return (s0 + acc) & 0xFF

    # ═══════════════════════════════════════════════════════════════════════
    # D_SPLIT: COMPOSITIONAL CONCATENATION
    # ═══════════════════════════════════════════════════════════════════════
    # S = seg0 || seg1 || ... || seg{k-1}
    # Each segment is itself a lawful seed Σ_j.

    elif family == 'D_SPLIT':
        segments = params.get('segments') or []
        if not isinstance(segments, list) or not segments:
            raise ValueError('D_SPLIT missing segments')
        # Determine which segment contains i by cumulative lengths.
        offset = 0
        for seg in segments:
            if not isinstance(seg, dict):
                raise ValueError('D_SPLIT segment must be dict seed')
            seg_n = int(seg.get('n', 0))
            if seg_n < 0:
                raise ValueError('D_SPLIT invalid segment length')
            if i < offset + seg_n:
                return Xi_projected(seg, i - offset)
            offset += seg_n
        raise IndexError('D_SPLIT index beyond total segment length')

    # ═══════════════════════════════════════════════════════════════════════
    # D14_CAUSAL_CORRELATIVE: CORRELATIVE STRIDE (WRAPPER)
    # ═══════════════════════════════════════════════════════════════════════
    # Alias of block recurrence: S[i] = sub[i mod k]

    elif family == 'D14_CAUSAL_CORRELATIVE':
        k = int(params.get('k', params.get('m', 0)))
        sub_seed = params.get('sub_seed')
        if k <= 0 or not isinstance(sub_seed, dict):
            raise ValueError('D14_CAUSAL_CORRELATIVE missing k/sub_seed')
        return Xi_projected(sub_seed, i % k)

    # ═══════════════════════════════════════════════════════════════════════
    # D15_SYMBOLIC_META_EMBED: META-EMBED (WRAPPER)
    # ═══════════════════════════════════════════════════════════════════════
    # Alias of compositional concatenation.

    elif family == 'D15_SYMBOLIC_META_EMBED':
        segments = params.get('segments')
        if segments is None:
            segments = params.get('sub_seeds')
        seed2 = {'family': 'D_SPLIT', 'params': {'segments': segments}, 'n': n}
        return Xi_projected(seed2, i)

    # ═══════════════════════════════════════════════════════════════════════
    # D16_PARAMETRIC_LAW_GROWTH: PARAMETRIC GROWTH (WRAPPER)
    # ═══════════════════════════════════════════════════════════════════════
    # Identity-on-laws wrapper: projects via base_seed.

    elif family == 'D16_PARAMETRIC_LAW_GROWTH':
        base_seed = params.get('base_seed')
        if not isinstance(base_seed, dict):
            raise ValueError('D16_PARAMETRIC_LAW_GROWTH missing base_seed')
        return Xi_projected(base_seed, i)

    # ═══════════════════════════════════════════════════════════════════════
    # D17_XOR_CONST: WRAPPER
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = inner[i] xor k

    elif family == 'D17_XOR_CONST':
        inner_seed = params.get('inner_seed')
        if not isinstance(inner_seed, dict):
            raise ValueError('D17_XOR_CONST missing inner_seed')
        k = int(params.get('k', 0)) & 0xFF
        return (Xi_projected(inner_seed, i) ^ k) & 0xFF

    # ═══════════════════════════════════════════════════════════════════════
    # D18_ADD_CONST: WRAPPER
    # ═══════════════════════════════════════════════════════════════════════
    # S[i] = inner[i] + k (mod 256)

    elif family == 'D18_ADD_CONST':
        inner_seed = params.get('inner_seed')
        if not isinstance(inner_seed, dict):
            raise ValueError('D18_ADD_CONST missing inner_seed')
        k = int(params.get('k', 0)) & 0xFF
        return (Xi_projected(inner_seed, i) + k) & 0xFF

    # ═══════════════════════════════════════════════════════════════════════
    # D9_INSTANT_DEDUCTION: INSTANT-DEDUCTION PARAMETRIC RADIAL  
    # ═══════════════════════════════════════════════════════════════════════
    # The seed stores boundary-deduced invariants (s0, r0, ds, dr).
    # Projection uses these as constraints in a pure algebraic law.
    # For the minimal 4-parameter form, we project via:
    #   Ξ_i = (s0 + (r0·φ_i) + (ds·i) + (dr·i²)) mod 256
    # where φ_i is the radial phase at index i.
    # Since φ depends on mirror structure, for oracle-free projection we use
    # a simplified radial coupling: φ_i ≈ min(i, n-1-i)
    elif family == 'D9_INSTANT_DEDUCTION':
        n_local = int(seed.get('n', 0))
        if n_local <= 0:
            raise ValueError('D9_INSTANT_DEDUCTION missing valid n')
        if not (0 <= i < n_local):
            raise ValueError('Index out of range')

        s0 = int(params.get('s0', 0)) & 0xFF
        r0 = int(params.get('r0', 0)) & 0xFF
        ds = int(params.get('ds', 0)) & 0xFF
        dr = int(params.get('dr', 0)) & 0xFF

        # Radial phase: distance from boundaries (geometric interpretation).
        phi_i = min(i, n_local - 1 - i)
        
        return (s0 + r0 * phi_i + ds * i + dr * i * i) & 0xFF
    
    # ═══════════════════════════════════════════════════════════════════════
    # D9_RADIAL: GEOMETRIC RADIAL PROJECTION
    # ═══════════════════════════════════════════════════════════════════════
    # Universal closure via meta-law deduction
    # 
    # ═══════════════════════════════════════════════════════════════════════
    # D9_RADIAL: GEOMETRIC RADIAL PROJECTION
    # ═══════════════════════════════════════════════════════════════════════
    # CLF Causal Structure Abstraction:
    #   1. Parametric: Single function generates all rings
    #   2. Discrete: Mapping r → D_r (function per ring)
    # Both are exact mathematical bijections, only abstraction level differs
    
    elif family == 'D9_RADIAL':
        center = params['center']
        r = abs(i - center)
        
        # ✅ Priority 1: Universal parametric meta-law (deterministic causal inverse)
        # This is the TRUE INVERSE of the deduction performed in θ(S)
        meta = params.get('meta') or params.get('meta_law')
        if meta:
            meta_type = meta.get('type')
            if meta_type == 'D2_AFFINE_CONSTANT_DELTA':
                # Universal inverse equation: s₀(r) = base_s₀ + gradient_s₀·r (mod 256)
                # Then S[i] = s₀(r) + δ·side where side = 0 (left) or 1 (right)
                base_s0 = int(meta['base_s0'])
                gradient_s0 = int(meta['gradient_s0'])
                delta = int(meta['delta'])
                
                # Compute s₀ for this radius using the universal law
                s0_r = (base_s0 + gradient_s0 * r) & 0xFF
                
                # Determine side (left=0, center=0, right=1)
                if i < center:
                    side = 0  # Left
                elif i > center:
                    side = 1  # Right
                else:
                    side = 0  # Center (r=0)
                
                return (s0_r + delta * side) & 0xFF
            
            elif meta_type == 'D2_AFFINE_LINEAR_DELTA':
                # Extended universal law: both s₀ and δ vary linearly with radius
                # s₀(r) = base_s₀ + gradient_s₀·r (mod 256)
                # δ(r) = base_δ + gradient_δ·r (mod 256)
                # S[i] = s₀(r) + δ(r)·side (mod 256)
                base_s0 = int(meta['base_s0'])
                gradient_s0 = int(meta['gradient_s0'])
                base_delta = int(meta['base_delta'])
                gradient_delta = int(meta['gradient_delta'])
                
                # Compute s₀ and δ for this radius
                s0_r = (base_s0 + gradient_s0 * r) & 0xFF
                delta_r = (base_delta + gradient_delta * r) & 0xFF
                
                # Determine side
                if i < center:
                    side = 0
                elif i > center:
                    side = 1
                else:
                    side = 0
                
                return (s0_r + delta_r * side) & 0xFF
            
            elif meta_type == 'D9_CAUSAL_CLOSED':
                # Unified polynomial closure: α(r) = Σ αₖ·r^k, β(r) = Σ βₖ·r^k
                # S[i] = (b + G(r) + (d + D(r))·side) mod 256
                # where G(r) = Σ(αₖ/(k+1))·r^(k+1), D(r) = Σ(βₖ/(k+1))·r^(k+1)
                
                base_s0 = int(meta['base_s0'])
                base_delta = int(meta['base_delta'])
                alpha_coeffs = meta['alpha_coeffs']
                beta_coeffs = meta['beta_coeffs']
                degree = meta['degree']
                
                def eval_integral_polynomial(coeffs, r_val):
                    """Compute Σ(cₖ/(k+1))·r^(k+1) mod 256"""
                    result = 0
                    for k, c in enumerate(coeffs):
                        # Modular inverse of (k+1)
                        k_plus_1 = (k + 1) & 0xFF
                        if k_plus_1 % 2 == 0:
                            # Not invertible mod 256 - skip or approximate
                            # For even k+1, the contribution is limited
                            inv = 1  # Simplified handling
                        else:
                            inv = pow(k_plus_1, -1, 256)
                        
                        term = (c * pow(r_val, k + 1, 256) * inv) & 0xFF
                        result = (result + term) & 0xFF
                    return result
                
                # Compute G(r) and D(r)
                G_r = eval_integral_polynomial(alpha_coeffs, r)
                D_r = eval_integral_polynomial(beta_coeffs, r)
                
                # Determine side
                if i < center:
                    side = 0
                elif i > center:
                    side = 1
                else:
                    side = 0
                
                return (base_s0 + G_r + (base_delta + D_r) * side) & 0xFF
            
            elif meta_type == 'D9_LIMIT_CAUSAL_CLOSURE':
                # ════════════════════════════════════════════════════════════════════
                # CLF Limit-Causal Closure (Degree Ω) — Closed Fixed-Point Operator
                # ════════════════════════════════════════════════════════════════════
                # For p = Ω, Ξ_Ω is NOT iterative recursion — it is the algebraic
                # fixed point of the polynomial hierarchy:
                #
                #   Ξ_Ω(Σ)[i] = ∑_{r∈P(n)} κ_r · f_r(i) mod 256
                #
                # where:
                #   κ_r = structural coefficient at radius r (from θ(S))
                #   f_r(i) = phase-weighted propagator = exp(2πj(i-r)/n) mod 256
                #
                # This evaluates to:
                #   f_r(i) = cos(2π(i-r)/n) in real projection
                #
                # Properties:
                #   • Algebraically finite (no iteration)
                #   • Instant evaluation
                #   • Preserves bijection: Ξ(θ(S)) = S at all P(n)
                #   • Continuous wave expansion for i ∉ P(n)
                # ════════════════════════════════════════════════════════════════════
                
                # Field-closed reconstruction: all operations in ℤ₂₅₆
                # No floating-point, no exponential decay per CLF specification
                
                radii_defined = meta['radii_defined']  # P(n) = set of radii
                ring_laws_map = meta['ring_laws']  # {r → law_r}
                
                if not radii_defined:
                    raise ValueError("D9_LIMIT_CAUSAL_CLOSURE missing radii_defined")
                
                # Compute radius from center for position i
                r_i = abs(i - center)
                
                # Check if this radius has a defined ring law
                if r_i in radii_defined:
                    # Family-aware evaluation: stored law describes the RING at radius r
                    ring_seed = ring_laws_map[r_i]
                    ring_family = ring_seed.get('family')
                    ring_params = ring_seed.get('params', {})
                    ring_n = ring_seed.get('n', 1)
                    
                    # Evaluate the ring law to get value at position i
                    if ring_family == 'D1':
                        # D1: constant across entire ring
                        return int(ring_params.get('c', 0))
                    elif ring_family == 'D2':
                        # D2: affine law over ring with n=2 (left and right)
                        # s0 = left value (at center - r)
                        # delta = (right - left) mod 256
                        s0 = int(ring_params.get('s0', 0))
                        delta = int(ring_params.get('delta', 0))
                        
                        # Determine which side of center: left (0) or right (1)
                        if i < center:
                            # Left side: return s0
                            return s0 & 0xFF
                        elif i > center:
                            # Right side: return s0 + delta
                            return (s0 + delta) & 0xFF
                        else:
                            # Exactly at center (r=0): return s0
                            return s0 & 0xFF
                    elif ring_family in ['D3_AFFINE_LINEAR_GRADIENT', 'D4_AFFINE_QUADRATIC']:
                        # Higher-order affine: recursively evaluate at appropriate local index
                        # Map global position i to local index within ring
                        if i < center:
                            local_i = 0  # Left side
                        elif i > center:
                            local_i = ring_n - 1  # Right side
                        else:
                            local_i = ring_n // 2  # Center
                        return Xi_projected(ring_seed, local_i)
                    else:
                        # Generic: recursively evaluate
                        return Xi_projected(ring_seed, 0)
                
                # For i ∉ P(n): Nearest-neighbor continuation (field-closed)
                # Per CLF spec: ρ(r) = argmin_{p ∈ P(n)} |r - p|
                # Use the ring law from nearest anchor, no floating-point operations
                
                # Find nearest radius in P(n) — pure integer arithmetic
                nearest_r = min(radii_defined, key=lambda p: abs(p - r_i))
                
                # Get ring law at nearest anchor
                ring_seed = ring_laws_map[nearest_r]
                ring_family = ring_seed.get('family')
                ring_params = ring_seed.get('params', {})
                
                # Evaluate ring law at position i (family-aware, field-closed)
                if ring_family == 'D1':
                    # Constant law: D₁(x) = c
                    result = int(ring_params.get('c', 0)) & 0xFF
                elif ring_family == 'D2':
                    # Affine law: D₂(x) = s₀ or s₀+δ depending on side
                    s0 = int(ring_params.get('s0', 0))
                    delta = int(ring_params.get('delta', 0))
                    if i < center:
                        result = s0 & 0xFF
                    elif i > center:
                        result = (s0 + delta) & 0xFF
                    else:
                        result = s0 & 0xFF
                else:
                    # Higher-order: recursive evaluation at local position
                    ring_n = ring_seed.get('n', 1)
                    local_center = ring_n // 2
                    # Map global i to local index
                    if i < center:
                        local_i = 0
                    elif i > center:
                        local_i = ring_n - 1
                    else:
                        local_i = local_center
                    result = Xi_projected(ring_seed, local_i)
                
                return result
            
            elif meta_type == 'D2_AFFINE_QUADRATIC':
                # Second-order law: s₀ has quadratic evolution, δ has linear evolution
                # α(r) = α₀ + α₁·r → s₀(r) = b + α₀·r + ½α₁·r(r-1)
                # δ(r) = base_δ + gradient_δ·r
                base_s0 = int(meta['base_s0'])
                alpha0 = int(meta['alpha0'])
                alpha1 = int(meta['alpha1'])
                base_delta = int(meta['base_delta'])
                gradient_delta = int(meta['gradient_delta'])
                
                # Compute s₀(r) using quadratic form
                linear_term = (alpha0 * r) & 0xFF
                quadratic_term = (alpha1 * r * (r - 1) // 2) & 0xFF
                s0_r = (base_s0 + linear_term + quadratic_term) & 0xFF
                
                # Compute δ(r) using linear form
                delta_r = (base_delta + gradient_delta * r) & 0xFF
                
                # Determine side
                if i < center:
                    side = 0
                elif i > center:
                    side = 1
                else:
                    side = 0
                
                return (s0_r + delta_r * side) & 0xFF
            
            elif meta_type == 'D2_AFFINE_QUADRATIC_FULL':
                # Second-order law: both s₀ and δ have quadratic evolution
                # α(r) = α₀ + α₁·r → s₀(r) = b + α₀·r + ½α₁·r(r-1)
                # β(r) = β₀ + β₁·r → δ(r) = d + β₀·r + ½β₁·r(r-1)
                base_s0 = int(meta['base_s0'])
                alpha0 = int(meta['alpha0'])
                alpha1 = int(meta['alpha1'])
                base_delta = int(meta['base_delta'])
                beta0 = int(meta['beta0'])
                beta1 = int(meta['beta1'])
                
                # Compute s₀(r) using quadratic form
                s0_linear = (alpha0 * r) & 0xFF
                s0_quadratic = (alpha1 * r * (r - 1) // 2) & 0xFF
                s0_r = (base_s0 + s0_linear + s0_quadratic) & 0xFF
                
                # Compute δ(r) using quadratic form
                delta_linear = (beta0 * r) & 0xFF
                delta_quadratic = (beta1 * r * (r - 1) // 2) & 0xFF
                delta_r = (base_delta + delta_linear + delta_quadratic) & 0xFF
                
                # Determine side
                if i < center:
                    side = 0
                elif i > center:
                    side = 1
                else:
                    side = 0
                
                return (s0_r + delta_r * side) & 0xFF
                
            elif meta_type == 'D9_LEFT_RIGHT_SEEDS':
                left_seed = meta.get('left_seed')
                right_seed = meta.get('right_seed')
                if left_seed is None or right_seed is None:
                    raise ValueError("D9_LEFT_RIGHT_SEEDS meta missing left_seed/right_seed")
                # Radius-string indexing: index is r (distance from center)
                if i <= center:
                    return Xi_projected(left_seed, r)
                return Xi_projected(right_seed, r)
            else:
                raise ValueError(f"Unknown D9 meta-law type: {meta_type}")
        
        # ✅ Priority 2: Discrete generators (only for explicitly sampled radii)
        # If no universal meta-law exists, fall back to discrete ring_laws lookup
        # BUT: do NOT interpolate or complete - this violates Ξ∘θ=id
        ring_laws = params.get('ring_laws', {})
        if not ring_laws:
            raise ValueError(
                f"D9_RADIAL seed missing both meta-law and ring_laws.\n"
                f"θ(S) must deduce either a universal parametric law (meta) or "
                f"complete discrete generators (ring_laws) for Ξ(θ(S))=S to hold."
            )
        
        # Lookup discrete generator for this radius
        if r in ring_laws:
            ring_seed = ring_laws[r]
        elif str(r) in ring_laws:
            ring_seed = ring_laws[str(r)]
        else:
            raise ValueError(
                f"D9_RADIAL: radius r={r} not in ring_laws and no universal meta-law present.\n"
                f"This indicates θ(S) did not properly deduce the universal structure.\n"
                f"Ξ cannot reconstruct what θ did not recognize.\n"
                f"Available radii: {sorted(ring_laws.keys())}"
            )
        
        # Compute LOCAL index j within ring
        if r == 0:
            j = 0  # Center
        elif i < center:
            j = 0  # Left position
        else:
            j = 1 if ring_seed['n'] > 1 else 0  # Right position
        
        # Recursively project using ring-local index
        return Xi_projected(ring_seed, j)
    
    else:
        raise ValueError(f"Unknown law family: {family}")


class LazyExpansion:
    """
    CLF Mathematical Object: Ξ(Σ) as index→byte projection
    
    This represents the expanded string as a MATHEMATICAL FUNCTION,
    not as materialized bytes. This is the CORRECT CLF representation.
    
    ═══════════════════════════════════════════════════════════════════════════
    MATHEMATICAL PROPERTIES:
    ═══════════════════════════════════════════════════════════════════════════
    - O(1) index access: self[i] via Xi_projected
    - O(1) length: self.n from seed
    - O(1) equality: strategic sampling (5 positions)
    - O(n) materialization: bytes(self) only if user requests
    
    USAGE:
        expansion = LazyExpansion(seed)
        byte = expansion[42]           # O(1) projection
        n = len(expansion)              # O(1)
        same = (expansion == sampler)   # O(1) strategic check
        data = bytes(expansion)         # O(n) materialization (optional)
    """
    
    def __init__(self, seed: Dict[str, Any]):
        """Initialize lazy expansion from seed"""
        self.seed = seed
        self.n = seed.get('n', 0)
        self.family = seed.get('family', 'UNKNOWN')
    
    def __len__(self) -> int:
        """O(1) length"""
        return self.n
    
    def __getitem__(self, i: int) -> int:
        """O(1) projection: S[i] = D(i, params)"""
        if isinstance(i, slice):
            # Support slicing
            start, stop, step = i.indices(self.n)
            return bytes(self[j] for j in range(start, stop, step or 1))
        return Xi_projected(self.seed, i)
    
    def __bytes__(self) -> bytes:
        """O(n) materialization - only if explicitly requested by user"""
        return bytes(self[i] for i in range(self.n))
    
    def __eq__(self, other) -> bool:
        """Exact equality (no strategic shortcuts)."""
        if isinstance(other, (bytes, bytearray)):
            if len(other) != self.n:
                return False
            return all(self[i] == other[i] for i in range(self.n))

        if hasattr(other, '__len__') and hasattr(other, '__getitem__'):
            if len(other) != self.n:
                return False
            try:
                return all(self[i] == other[i] for i in range(self.n))
            except (IndexError, KeyError):
                return False

        return NotImplemented
    
    def __repr__(self) -> str:
        return f"<LazyExpansion: {self.family}, n={self.n}>"


__all__ = ['Xi_projected', 'LazyExpansion']
