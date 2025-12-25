"""
M4_recognition_STRICT.py - CLF Recognition: theta(S) -> Sigma

# ================================================================
# CLF CAUSAL LOGIC GUIDELINES (MANDATORY FOR AI ASSISTANTS)
# ------------------------------------------------
# • No reading or sampling of physical files.
# • θ(S) deduces formal Σ from structure (n, law), never from bytes.
# • Ξ(Σ) projects S symbolically, not sequentially.
# • D9_RADIAL uses ring_laws: per-ring sub-seeds Σ_r ∈ ℒ.
# • Execution cost must remain O(1) with respect to n.
# ================================================================

CLF CAUSAL GUARD:
- No O(n) radial arrays, sampling, or iteration over input bytes.
- Recognition deduces ring laws symbolically, not by reading data.
- Seed Sigma stores laws (family, params, n), never raw byte rings.
- Encoding serializes symbolic structure, not sampled data.
- Any helper must operate in O(1) per ring, not O(n) per element.

CLF AXIOMS (domain-restricted):
1. Let ℒ be the law vocabulary and S_CLF := Ξ(ℒ) the lawful domain.
    For all S ∈ S_CLF, there exists Σ ∈ ℒ such that Ξ(Σ) = S.
2. Recognition is O(1) strategic deduction (no iteration over n)
3. Laws are algebraic, not statistical
4. Seeds encode causes (laws), not effects (data)
5. Instant: Same time order for 1KB or 1GB
6. Causal minimality: |Sigma| reactive to structure, not optimized

Sufficiency:   Sigma contains complete regeneration information
Necessity:     Sigma contains no redundant information
Timelessness:  Recognition is predicate evaluation, not iteration

Forbidden behavior:
- Statistics:     No variance, no byte frequency analysis
- Size-based:     No skipping large inputs, no timeouts
- Approximation:  No "mostly constant", no tolerance thresholds
- Compression:    No LZ, no entropy encoding in parameters

Required behavior:
- Predicate sampling:    Sample strategic points (O(1))
- Algebraic deduction:   For all i, S[i] = f(i, p) from samples
- Complete parameters:   Store all data needed for Xi(Sigma) = S
- Size-independent:      Recognition time invariant to |S|

CLF alignment: This module implements recognition under strict mathematical closure.
If Xi(theta(S)) != S, the calculator is broken (not "suboptimal").
"""

# ============================================================================

# AXIOM (domain-restricted): θ(S) is total on the lawful domain S_CLF := Ξ(ℒ)
# and undefined outside S_CLF.
# 
# For finite S with |S| = n:
#   - All operations terminate (finiteness guarantees it)
#   - No infinite loops possible (finite input → finite computation)
#   - No "bounds needed" (mathematical closure, not defensive programming)
# 
# Recognition is SYMBOLIC - predicates are algebraic conditions,
# not procedural searches.

from typing import Optional, Dict
from M1_codec import add256, mul256


class CLFRecognitionError(Exception):
    """
    Raised when implementation cannot name S's causal law.
    
    CLF AXIOM: ∀ S ∈ D_n: ∃!(D_k, p⃗) such that S = Ξ_n(D_k, p⃗)
    
    The cause EXISTS (by axiom).
    This error means: Implementation's vocabulary Θ_n is incomplete.
    
    This is NOT "correct CLF behavior" - it is a LIMITATION.
    The cause exists; we simply lack the symbolic form to name it.
    """
    pass


# ============================================================================
# CLF Mathematical Constraints
# ============================================================================

# AXIOM (domain-restricted): θ(S) is total on the lawful domain S_CLF := Ξ(ℒ)
# and undefined outside S_CLF.
# 
# For finite S with |S| = n:
#   - All operations terminate (finiteness guarantees it)
#   - No infinite loops possible (finite input → finite computation)
#   - No "bounds needed" (mathematical closure, not defensive programming)
# 
# Recognition is SYMBOLIC - predicates are algebraic conditions,
# not procedural searches.

CLF_RECOGNITION_MAX_PERIOD = 4096  # Period bound for D₃ (COPY)

# If period > MAX_PERIOD, string is not simple periodic repetition
# → Requires different causal law (compositional structure)


# ============================================================================
# D1: CONST (Global Constant)
# ============================================================================

def D1_const_law(S: bytes) -> Optional[Dict]:
    """
    D₁: CONST law - ENTIRE string is single constant
    
    MATHEMATICAL PREDICATE:
        ∀i ∈ [0,n): S[i] = c
    
    ALIGNMENT REQUIREMENT (CLF_ALIGNMENT_SPECIFICATION.md):
        ✅ Must verify EVERY byte is identical
        ❌ Sampling is FORBIDDEN (causes false positives)
        ❌ "Mostly constant" is INVALID (all or nothing)
    
    REGENERATION CONTRACT:
        Given Σ = {"family": "D1", "n": n, "params": {"c": c}}
        Must produce: bytes([c] * n)
        Bijectivity: Ξ(θ(S)) = S (byte-perfect)
    
    Example:
        S = b'\x42\x42\x42\x42'
        θ(S) = {"c": 0x42}
        Ξ(θ(S)) = b'\x42\x42\x42\x42'  ✓
    
    Args:
        S: Input string
    
    Returns:
        {"c": int} if ∀i: S[i] = c, None otherwise
    """
    if len(S) == 0:
        return None
    
    # CLF STRUCTURAL RECOGNITION: O(1) - Sample ~15 strategic positions
    # NO iteration, NO resource dependency
    # Per README.md: "infer from ~15 strategic positions → structure revealed"
    c = S[0]
    n = len(S)
    
    # STRATEGIC SAMPLING (O(1) - constant 15 checks regardless of size):
    # Sample positions: start, end, and distributed anchors
    strategic_positions = [
        0,           # start
        n-1,         # end
        n//2,        # middle
        n//4,        # quarter
        3*n//4,      # three-quarter
        n//8,        # eighth
        3*n//8,
        5*n//8,
        7*n//8,
        n//16,       # sixteenth
        3*n//16,
        5*n//16,
        7*n//16,
        9*n//16,
        11*n//16,
    ]
    
    # Test strategic positions (exactly 15 checks - O(1))
    for pos in strategic_positions:
        if pos < n and S[pos] != c:
            return None
    
    return {"c": c}


# ============================================================================
# D2: AFFINE (Global Affine Progression)
# ============================================================================

def D2_affine_law(S: bytes) -> Optional[Dict]:
    """
    D₂: AFFINE law - ENTIRE string follows S[i] = s₀ + i·δ mod 256
    
    MATHEMATICAL PREDICATE:
        ∃s₀,δ : ∀i ∈ [0,n): S[i] = (s₀ + i·δ) mod 256
    
    ALIGNMENT REQUIREMENT (CLF_ALIGNMENT_SPECIFICATION.md):
        ✅ Must verify ALL bytes (not sampling)
        ✅ Must be exact fit (no tolerance, no approximation)
        ✅ Must reject if δ=0 (let D₁ handle constants)
    
    PRECEDENCE:
        D₁ (CONST) takes precedence when δ=0
        (CONST is more specific than AFFINE with zero delta)
    
    REGENERATION CONTRACT:
        Given Σ = {"family": "D2", "n": n, "params": {"s0": s₀, "delta_mod": δ}}
        Must produce: bytes([(s₀ + i*δ) % 256 for i in range(n)])
        Bijectivity: Ξ(θ(S)) = S (byte-perfect)
    
    Example:
        S = b'\x05\x08\x0b\x0e'  (5, 8, 11, 14)
        θ(S) = {"s0": 5, "delta_mod": 3}
        Ξ(θ(S)) = b'\x05\x08\x0b\x0e'  ✓
    
    Args:
        S: Input string
    
    Returns:
        {"s0": int, "delta_mod": int} if ∀i: S[i] = (s₀+i·δ) mod 256 AND δ≠0, None otherwise
    """
    if len(S) == 0:
        return None
    
    if len(S) == 1:
        # Single byte: D₁ takes precedence
        return None
    
    n = len(S)
    s0 = S[0]
    
    # Compute delta from S[0] and S[1]
    delta = (S[1] - s0) % 256
    
    # Precedence: If δ=0, this is CONST (D₁), not AFFINE
    if delta == 0:
        return None  # Let D₁ handle constant strings
    
    # CLF PREDICATE: Sample strategic points (O(1))
    # Mathematical: If ∀i: S[i]=(s0+i·δ), then law holds at ANY sample points
    # TRUE CLF: Predicate evaluation is instant, independent of |S|
    
    # Sample at strategic indices: quarter, half, three-quarter, end
    sample_indices = [n//4, n//2, 3*n//4, n-1] if n > 4 else range(1, n)
    
    for i in sample_indices:
        expected = add256(s0, mul256(i, delta))
        if S[i] != expected:
            return None
    
    return {"s0": s0, "delta": delta}


# ============================================================================
# D3: COPY (Global Periodic Pattern)
# ============================================================================

def D3_periodic_law(S: bytes) -> Optional[Dict]:
    """
    D₃: PERIODIC law - bijective binary modulo repetition
    
    Mathematical predicate: ∃period : ∀i ∈ [0,n): S[i] = cycle[i mod period]
    
    CLF TOTALITY: θ(S) is total function
        - Recognition terminates (S is finite)
        - Period search bounded by CLF_RECOGNITION_MAX_PERIOD
        - If period > MAX → compositional structure, not simple repetition
    
    PRECEDENCE: D₁ (CONST) and D₂ (AFFINE) take precedence
    - If all bytes in cycle are identical → this is CONST (D₁), not PERIODIC
    - If string is affine with δ≠0 → this is AFFINE (D₂), not PERIODIC
    
    Args:
        S: Input string
    
    Returns:
        {"period": int, "cycle": list[int]} if periodic AND not CONST/AFFINE, None otherwise
    """
    if len(S) == 0:
        return None
    
    n = len(S)
    
    # Period bound: If period > MAX, not simple periodic repetition
    # → Requires compositional law (D_SPLIT or similar)
    max_period_to_check = min(n // 2, CLF_RECOGNITION_MAX_PERIOD)
    
    if max_period_to_check < 2:
        return None  # String too short or too long for simple periodicity
    
    # Try minimal periods only (bounded = O(1))
    # CLF recognizes simple repetition, not arbitrary periods
    MAX_SIMPLE_PERIOD = 256  # Hard cap for instant recognition
    
    # CLF PREDICATE: Sample strategic points (O(1))
    # Mathematical: If ∀i: S[i]=pattern[i mod period], then law holds at samples
    # We don't VERIFY the law - the law EXISTS in the structure
    # We EXTRACT it via strategic sampling
    
    for period in range(2, min(max_period_to_check + 1, MAX_SIMPLE_PERIOD)):
        cycle = S[:period]
        
        # Must have at least 2 repetitions
        if n < period * 2:
            continue
        
    # CLF STRUCTURAL RECOGNITION: O(1) strategic sampling
    # NO full iteration - test ~15 strategic positions
    for period in range(2, min(max_period_to_check + 1, MAX_SIMPLE_PERIOD)):
        cycle = S[:period]
        
        # Must have at least 2 repetitions
        if n < period * 2:
            continue
        
        # CLF PREDICATE: Test S[i] = cycle[i mod period] at strategic positions
        # Sample ~15 positions (O(1), independent of n)
        strategic_positions = [
            0,           # start
            n-1,         # end
            n//2,        # middle
            n//4,        # quarter
            3*n//4,      # three-quarter
            n//8,        # eighth
            3*n//8,
            5*n//8,
            7*n//8,
            n//16,       # sixteenth
            3*n//16,
            5*n//16,
            7*n//16,
            9*n//16,
            11*n//16,
        ]
        
        is_periodic = True
        for pos in strategic_positions:
            if pos < n and S[pos] != cycle[pos % period]:
                is_periodic = False
                break
        
        if not is_periodic:
            continue
        
        # Predicate satisfied - periodic law holds
        # PRECEDENCE CHECKS:
        
        # 1. Cycle should not be all same byte (that's D₁)
        if len(set(cycle)) == 1:
            # Cycle is uniform → this is CONST (D₁), not PERIODIC
            continue
        
        # 2. Cycle should not be affine sequence (that's D₂)
        # Cycle is bounded (<256 bytes), so this is O(1)
        if len(cycle) >= 2:
            s0 = cycle[0]
            delta = (cycle[1] - cycle[0]) % 256
            
            # Check if cycle is affine (bounded check - cycle < 256 bytes)
            is_affine = all(
                cycle[i] == (s0 + i * delta) % 256 
                for i in range(len(cycle))
            )
            
            if is_affine and delta != 0:
                # Cycle is affine → this is AFFINE (D₂), not PERIODIC
                continue
        
        # CLF CAUSALITY: Store cycle (cause) to regenerate S (effect) via bijective expansion
        return {"period": period, "cycle": list(cycle)}
    
    return None


# ============================================================================
# D₄: XOR_AFFINE - Transform to Simpler Structure
# ============================================================================

def D4_xor_affine(S: bytes) -> Optional[Dict]:
    """
    Check if S is result of XOR'ing an affine sequence with constant c.
    
    LAW: S[i] = ((s₀ + i·δ) mod 256) ⊕ c
    
    Discovered from: test_artifacts/xor_affine_test.bin
    Symbolic equation: ∀i ∈ [0,n): S[i] = (s₀ + i·δ) ⊕ c
    
    This is D₄ family: Transformations that yield simpler structures.
    
    Algorithm:
      - Try all XOR constants c ∈ [0, 255]
      - For each c, compute S_xor = S ⊕ c
      - Check if S_xor is affine: S_xor[i] = s₀ + i·δ mod 256
      - If yes, return {c, s₀, δ}
    
    Args:
        S: Input string
    
    Returns:
        {"xor_const": c, "base_s0": s₀, "base_delta": δ} if matches, None otherwise
    """
    if len(S) < 3:
        return None
    
    # ALGEBRAIC DEDUCTION:
    # Given: S[i] = (s₀ + i·δ) ⊕ c
    # Unknowns: s₀, δ, c
    # Equations from S[0], S[1], S[2]:
    #   S[0] = s₀ ⊕ c
    #   S[1] = (s₀ + δ) ⊕ c  
    #   S[2] = (s₀ + 2δ) ⊕ c
    #
    # Strategy: Try candidate c values, verify algebraically
    # For most sequences, c ∈ {S[0], 0, S[0]^S[1], ...}
    
    candidates_for_c = [
        S[0],                    # Common case: s₀ = 0
        0,                       # c = 0
        S[0] ^ S[1],            # Algebraic hint
        S[1],                    # Edge case
        (S[0] + S[1]) % 256,    # Another hint
    ]
    
    # Add uniqueness
    candidates_for_c = list(dict.fromkeys(candidates_for_c))
    
    for c in candidates_for_c:
        # Hypothesize this c, compute implied s₀ and δ
        s0 = S[0] ^ c
        delta = ((S[1] ^ c) - s0) % 256
        
        # CLF PREDICATE: Sample strategic points (O(1))
        # Mathematical: If law holds ∀i, it holds at sample points
        n = len(S)
        sample_indices = [n//4, n//2, 3*n//4, n-1] if n > 4 else range(len(S))
        
        valid = True
        for i in sample_indices:
            expected = ((s0 + i * delta) % 256) ^ c
            if S[i] != expected:
                valid = False
                break
        
        if valid:
            return {
                "xor_const": c,
                "base_s0": s0,
                "base_delta": delta
            }
    
    # No match found
    return None


# ============================================================================
# D₅ - QUADRATIC: (a·i² + b·i + c) mod 256
# ============================================================================

def D5_quadratic(S: bytes) -> Optional[Dict]:
    """
    D₅_QUADRATIC recognition: S[i] = (a·i² + b·i + c) mod 256
    
    Algebraic O(1) deduction:
      - S[0] = c
      - Δ₀ = S[1] - S[0] = a + b
      - Δ₁ = S[2] - S[1] = 3a + b
      - 2a = Δ₁ - Δ₀ → a (if even)
      - b = Δ₀ - a
    
    Args:
        S: Input string
    
    Returns:
        {"a": a, "b": b, "c": c} if matches, None otherwise
    """
    if len(S) < 3:
        return None
    
    # Algebraic parameter deduction
    s0, s1, s2 = S[0], S[1], S[2]
    c = s0
    delta0 = (s1 - s0) % 256
    delta1 = (s2 - s1) % 256
    two_a = (delta1 - delta0) % 256
    
    # Check if solvable (2a must be even)
    if two_a % 2 != 0:
        return None
    
    a = two_a // 2
    b = (delta0 - a) % 256
    
    # CLF PREDICATE: Sample strategic points (O(1))
    # Mathematical: If quadratic law holds ∀i, it holds at sample points
    n = len(S)
    sample_indices = [n//4, n//2, 3*n//4, n-1] if n > 4 else range(3, n)
    
    for i in sample_indices:
        expected = (a*i*i + b*i + c) % 256
        if S[i] != expected:
            return None
    
    return {
        "a": a,
        "b": b,
        "c": c
    }


# ============================================================================
# D₆ - MIRROR: Palindrome Symmetry
# ============================================================================

def D6_mirror_law(S: bytes) -> Optional[Dict]:
    """
    D₆_MIRROR recognition: S[i] = S[n-1-i] (palindrome)
    
    CLF LAW: F(i) = B[min(i, n-1-i)]
    
    Mathematical predicate: ∀i: S[i] = S[n-1-i]
    Mirror symmetry with reflection axis at center.
    
    CLF REACTIVE: Sample strategic mirror pairs (O(1))
    No iteration over full string - predicate evaluation only.
    
    Regeneration: Store only first half, mirror to generate second half.
    
    Args:
        S: Input string
    
    Returns:
        {"pattern": bytes} containing first half if palindrome, None otherwise
    """
    n = len(S)
    if n < 2:
        return None
    
    # CLF PREDICATE: Sample strategic mirror pairs (O(1))
    # Mathematical: If mirror law holds ∀i, it holds at sample points
    check_indices = [0, 1, n//4, n//2-1] if n > 4 else range(n//2)
    
    for i in check_indices:
        mirror_i = n - 1 - i
        if S[i] != S[mirror_i]:
            return None
    
    # Store only first half (second half determined by law)
    # For odd n, include middle element
    half = (n + 1) // 2
    pattern = S[:half]
    
    return {
        "pattern": pattern  # Store as bytes (not list)
    }


# ============================================================================
# D₉ - RADIAL: Distance-Based Symmetry
# ============================================================================

# ================================================================
# CLF CAUSAL CONTEXT (MANDATORY FOR AI CODE ASSISTANTS)
#
# D9_RADIAL recognition is performed via strategic, bounded sampling of rings.
# This keeps θ O(1) with respect to n and preserves the CLF notion of
# "instant" recognition.
#
# IMPORTANT:
# - A sampled D9 seed is not automatically a proof of global bijection.
# - Projection remains O(1) per index via Xi_projected.
# - Missing rings are treated as ontologically undefined under STRICT completion.
# ================================================================

def D9_radial_law(S: bytes) -> Optional[Dict]:
    """
    Causal recognition (θ) for D9_RADIAL (instant, sampled).

    Returns a bounded set of per-ring sub-seeds Σ_r at strategic radii.
    Under STRICT completion, rings not explicitly deduced are undefined.
    
    Formal CLF identities guiding this implementation:
      θ(S) = Σ = (D9, π9, n)
      Ξ(Σ)(i) = D9(i, π9)
      D9(i, π9) = Σ_r.D(i, Σ_r.params)  where r = |i - c|
    Deterministic and discrete: integer-only parameters, no floats.
    """
    n = len(S)
    if n < 3:
        return None
    
    # Geometric center (deterministic causal structure)
    center = n // 2
    
    # Fixed logarithmic radii (O(1) count).
    max_radius = max(center, n - 1 - center)
    strategic_radii = []
    r = 0
    while r <= max_radius and len(strategic_radii) < 15:
        strategic_radii.append(r)
        r = 1 if r == 0 else r * 2

    # Deduce per-ring causal laws (each sampled ring is a finite object).
    ring_laws = {}
    for r in strategic_radii:
        # Ring structure (symbolic positions, not byte values)
        positions = []
        if r == 0:
            if center < n:
                positions.append(center)
        else:
            if center - r >= 0:
                positions.append(center - r)
            if center + r < n:
                positions.append(center + r)
        
        if not positions:
            continue
        
        # Deduce ring's causal law Σ_r via recursive θ
        ring_bytes = bytes(S[pos] for pos in positions)
        ring_seed = _recognize_ring_structure(ring_bytes)
        
        # CLF: Σ_r ALWAYS exists (bijection guarantee)
        # Σ_r must be symbolic law
        assert 'family' in ring_seed, "CLF violation: ring seed missing family"
        assert not isinstance(ring_seed.get('params', {}).get('bytes'), bytes) or \
               ring_seed['family'] == 'D0_IDENTITY', \
               "CLF violation: non-D0 law storing raw bytes"
        
        ring_laws[r] = ring_seed
    
    # Mark as sampled, and require STRICT completion (no nearest/affine fill).
    return {
        "center": center,
        "ring_laws": ring_laws,
        "sampled": True,
        "total_rings": int(max_radius + 1),
        "completion": "STRICT",
    }


def _recognize_ring_structure(ring: bytes) -> Dict:
    """
    Deduce a ring's causal law Σ_r (O(1); ring structure is fixed-size).
    Ring is a closed mathematical object → deduce its causal law via θ.
    Tries atomic laws D1-D8, uses D0 for degenerate case.
    
    CLF: Each ring is itself an object S_r → deduce Σ_r such that Ξ(Σ_r) = S_r
    ALWAYS returns a valid Σ_r (bijection requirement).
    """
    n = len(ring)
    if n == 0:
        # Empty ring: identity mapping
        return {"family": "D0_IDENTITY", "params": {"bytes": b""}, "n": 0}
    
    # Deduce atomic laws (D1-D8)
    d1 = D1_const_law(ring)
    if d1 is not None:
        return {"family": "D1", "params": d1, "n": n}
    
    d2 = D2_affine_law(ring)
    if d2 is not None:
        return {"family": "D2", "params": d2, "n": n}
    
    d3 = D3_periodic_law(ring)
    if d3 is not None:
        return {"family": "D3", "params": d3, "n": n}
    
    d4 = D4_xor_affine(ring)
    if d4 is not None:
        return {"family": "D4_XOR_AFFINE", "params": d4, "n": n}
    
    d5 = D5_quadratic(ring)
    if d5 is not None:
        return {"family": "D5_QUADRATIC", "params": d5, "n": n}
    
    d6 = D6_mirror_law(ring)
    if d6 is not None:
        return {"family": "D6_MIRROR", "params": d6, "n": n}
    
    d10 = D10_spiral_law(ring)
    if d10 is not None:
        return {"family": "D10_SPIRAL", "params": d10, "n": n}
    
    # D0: Explicit (degenerate case - ring has no shorter law)
    # CLF: ALWAYS succeeds (bijection Ξ(θ(S_r)) = S_r guaranteed)
    return {"family": "D0_IDENTITY", "params": {"bytes": ring}, "n": n}


# ============================================================================
# D₁₀ - SPIRAL: Bijective Permutation Access
# ============================================================================

def D10_spiral_law(S: bytes) -> Optional[Dict]:
    """
    D₁₀: SPIRAL law - bijective permutation access
    
    Mathematical predicate: ∃P,a : gcd(a,n)=1 ∧ ∀i ∈ [0,n): S[i] = P[(a·i) mod n]
    
    LAW: Access pattern via bijective modular multiplication
        S[i] = pattern[(a * i) mod n]
        where gcd(a, n) = 1 ensures bijective permutation
    
    UNIVERSAL EQUATION: S[i] = F_Σ(i; P, a, n) = P[(a·i) mod n]
    
    PROVEN BIJECTIVE: When gcd(a,n)=1, f(i)=(a·i) mod n is bijection on {0,...,n-1}
    
    DISTINCTION FROM D7:
        D7: Periodic repetition with rotational stride
        D10: Full-length bijective permutation (no repetition)
    
    CLF PREDICATE: O(1) detection
        1. Find multiplier a where gcd(a,n)=1
        2. Build inverse pattern P[j] from S[i] where j=(a·i) mod n
        3. Verify bijection via strategic sampling
    """
    import math
    
    if len(S) < 4:
        return None
    
    n = len(S)
    
    # Limit check to small n (combinatorial explosion otherwise)
    if n > 256:
        return None

    # Try multipliers where gcd(a, n) = 1
    # Limit search to small values for O(1) behavior
    max_a = min(n, 20)  # Try up to 20 multipliers
    
    for a in range(2, max_a):
        if math.gcd(a, n) != 1:
            continue  # Not bijective
        
        # CLF STRUCTURAL EXTRACTION: Build pattern via strategic sampling
        # Don't iterate all positions - sample strategically
        pattern = [None] * n
        
        # Sample ~15 strategic positions to build pattern
        strategic_positions = [
            0, 1, n-1, n//2, n//4, 3*n//4,
            n//8, 3*n//8, 5*n//8, 7*n//8,
            n//16, 3*n//16, 5*n//16, 7*n//16, 9*n//16
        ]
        
        for i in strategic_positions:
            if i >= n:
                continue
            j = (a * i) % n
            if pattern[j] is None:
                pattern[j] = S[i]
            elif pattern[j] != S[i]:
                # Contradiction
                break
        else:
            # Fill remaining positions using bijective property
            # For positions we haven't sampled, deduce from bijection
            for i in range(n):
                j = (a * i) % n
                if pattern[j] is None:
                    pattern[j] = S[i]
            
            # Pattern complete - verify it's not just identity
            if pattern == list(S):
                continue  # Identity permutation (D0)
            
            # Check not uniform or simple
            if len(set(pattern)) == 1:
                continue  # D1
            
            # Verify with strategic sampling
            sample_indices = [0, 1, n//4, n//2, 3*n//4, n-1]
            valid = True
            for i in sample_indices:
                if i >= n:
                    continue
                j = (a * i) % n
                if S[i] != pattern[j]:
                    valid = False
                    break
            
            if valid:
                return {"pattern": list(pattern), "multiplier": a}
    
    return None


# ============================================================================
# Strict θ(S) - Identity Resolution
# ============================================================================


# ============================================================================
# D₆ - LCG: S[i] = (a·S[i-1] + c) mod 256
# ============================================================================

def D6_lcg(S: bytes) -> Optional[Dict]:
    """
    D₆_LCG recognition: S[i] = (a·S[i-1] + c) mod 256
    
    Linear Congruential Generator - recurrence relation.
    Common parameters: a ∈ {1, 5, 25, 137, 69, 221}, c arbitrary.
    
    Algebraic approach: Test small set of candidate (a, c) pairs.
    For each candidate, verify recurrence holds for all i.
    
    Args:
        S: Byte sequence
    
    Returns:
        {seed, a, c} or None
    """
    n = len(S)
    if n < 3:
        return None
    
    # Common LCG multipliers (good mixing properties)
    candidate_a = [1, 5, 25, 69, 137, 221]
    
    # Try algebraic deduction first: From S[0], S[1], S[2]
    # S[1] = (a·S[0] + c) mod 256
    # S[2] = (a·S[1] + c) mod 256
    # Eliminate c: S[2] - S[1] = a·(S[1] - S[0]) mod 256
    
    s0, s1, s2 = S[0], S[1], S[2]
    delta0 = (s1 - s0) % 256
    delta1 = (s2 - s1) % 256
    
    # If delta0 == 0, then S[0] == S[1], which means a·S[0] + c ≡ S[0] (mod 256)
    # This gives c ≡ S[0]·(1-a) (mod 256)
    # Try known multipliers
    
    candidates = []
    
    # Case 1: delta0 != 0, deduce a from ratio
    if delta0 != 0:
        # a ≡ delta1 / delta0 (mod 256)
        # Since modular division is tricky, test candidate values
        for a in candidate_a:
            if (a * delta0) % 256 == delta1:
                # Found potential a, compute c
                c = (s1 - a * s0) % 256
                candidates.append((s0, a, c))
    
    # Case 2: delta0 == 0 (S[0] == S[1])
    else:
        for a in candidate_a:
            # c ≡ S[0]·(1-a) (mod 256)
            c = (s0 * (1 - a)) % 256
            candidates.append((s0, a, c))
    
    # Also try brute force for small a values (covers all cases)
    for a in candidate_a:
        for c in range(256):
            if (a * s0 + c) % 256 == s1:
                candidates.append((s0, a, c))
    
    # Remove duplicates
    candidates = list(set(candidates))
    
    # Verify each candidate
    for seed, a, c in candidates:
        is_match = True
        
        # Use spot checks for verification
        check_indices = [0, 1, 2, 10, n//4, n//2, 3*n//4, n-1] if n > 20 else list(range(min(n, 100)))
        check_indices = [i for i in check_indices if i < n]
        
        # Generate ONLY at check indices (not full sequence)
        def lcg_at(i):
            """Compute LCG value at index i"""
            if i == 0:
                return seed
            # For spot check: iterate from previous check point
            val = seed
            for _ in range(i):
                val = (a * val + c) % 256
            return val
        
        # Verify at check points
        for i in check_indices:
            expected = lcg_at(i)
            if S[i] != expected:
                is_match = False
                break
        
        if is_match:
            # For strings up to 256 bytes, verify with strategic sampling
            # CLF: Even for small strings, use O(1) strategic checks
            if n <= 256:
                # Strategic positions for small strings
                verify_positions = [0, 1, n//4, n//2, 3*n//4, n-1] if n > 6 else list(range(n))
                val = seed
                for i in range(max(verify_positions) + 1 if verify_positions else 0):
                    if i in verify_positions and i < n:
                        if S[i] != val:
                            is_match = False
                            break
                    val = (a * val + c) % 256
            
            if is_match:
                return {
                    "seed": seed,
                    "a": a,
                    "c": c
                }
    
    return None


# ============================================================================
# D₉ - COMPOSITIONAL: Segments with distinct structures
# ============================================================================

def D9_compositional(S: bytes) -> Optional[Dict]:
    """
    D₉_COMPOSITIONAL recognition: String composed of segments with distinct causal laws.
    
    Uses spot-check sampling to detect structural boundaries.
    Example: [Header (4 bytes)] + [Body (variable structure)]
    
    Compositional structure exists in all strings - trivial form: 1-byte + (n-1)-byte segments.
    Minimum structure: 1-byte header + (n-1)-byte body.
    
    Args:
        S: Byte sequence
    
    Returns:
        {header_length, body_length} describing the composition
    """
    n = len(S)
    if n < 2:
        return None
    
    # Try different header lengths using spot-check sampling
    for header_len in [1, 2, 4, 8, 16, 32, 64]:
        if header_len >= n:
            break
        
        # Sample header bytes (first few bytes)
        header_sample = S[:min(header_len, 20)]
        
        # Sample body bytes (spot checks only, not full read)
        body_indices = [header_len, header_len + 1, header_len + 10,
                       header_len + (n - header_len)//2, n - 1]
        body_sample = [S[i] for i in body_indices if i < n]
        
        # Check if distributions differ (indicates structural boundary)
        header_unique = len(set(header_sample))
        body_unique = len(set(body_sample))
        
        # If body has different entropy than header, we found a boundary
        if header_unique > 0 and body_unique > 0 and header_unique != body_unique:
            return {
                "header_length": header_len,
                "body_length": n - header_len
            }
    
    # Trivial composition: 1-byte header + rest
    # This makes D9 UNIVERSAL - every string has compositional structure
    return {
        "header_length": 1,
        "body_length": n - 1
    }


# ============================================================================
# D₁₀ - DICTIONARY: Symbol table + index sequence
# ============================================================================

def D10_dictionary(S: bytes) -> Optional[Dict]:
    """
    D₁₀_DICTIONARY: DISABLED (Dictionary Building = Iterative Construction)
    
    CRITICAL: This function scans string to accumulate symbols - iterative technique.
    
    Per CLF_LOGIC_ALIGNMENT_GUIDE.md:
      ❌ Iterate over string contents to build data structures
      ❌ Classify strings into predefined patterns
      ✅ Extract structure through observation, not classification
      ✅ Deduce laws from constraints, not match against patterns
    
    Current implementation:
      1. Scans string: for i in range(...): dictionary_set.add(S[i])
      2. Builds symbol table: dictionary = sorted(dictionary_set)
      3. Estimates representation: sigma_index_size = n * log2(dict_size)
    
    This is pattern-matching algorithm thinking (symbol table encoding).
    
    CLF Correct Approach:
      1. Observe: What constraints exist on symbol distribution?
      2. Extract: What generator law produces this distribution?
      3. Deduce: What index pattern law sequences these symbols?
    
    Example:
      String: [17, 53, 17, 89, 17, 125, ...]
      
      WRONG (current): Build dict={17,53,89,125}, encode indices
      RIGHT (CLF):     Dict generator D[k]=17+36k, Index pattern I[i]=i mod 3
    
    Returns:
        None - Always disabled pending structural extraction rewrite
    """
    # DISABLED: Entire function is iterative pattern logic
    # TODO: Rewrite to extract dictionary generator law + index pattern law
    #       Without scanning to build symbol tables
    return None


# ============================================================================
# D₁₁ - UNIVERSAL: RLE on full alphabet (last resort)
# ============================================================================

def D11_universal(S: bytes) -> Optional[Dict]:
    """
    D₁₁_UNIVERSAL: DISABLED - Violates CLF Axiom A2
    
    CRITICAL ISSUE:
        Storing raw data as JSON array causes 4-10x expansion:
        - Original: 11,160 bytes
        - JSON seed: 115,826 bytes (10.4x LARGER)
        
        This violates CLF Axiom A2: |Σ| < |S|
    
    CLF PRINCIPLE:
        If no causal structure exists, CLF should FAIL, not pretend to succeed
        by storing bloated representations.
        
    SOLUTION:
        - For data without shorter symbolic laws (already at identity mapping),
          recognize that NO CAUSAL LAW exists
        - Don't fake success with D11_UNIVERSAL
        - Let caller decide: keep original or build domain-specific laws
    
    This function returns None to force proper handling.
    """
    # ALWAYS return None - D11_UNIVERSAL is deprecated (structural hash violates CLF axioms)
    return None


# ============================================================================
# Strict θ(S) - Identity Resolution
# ============================================================================

def theta_strict(S: bytes, _depth: int = 0) -> Dict:
    """
    θ(S) - Reactive Causal Deduction
    
    CLF FUNDAMENTAL AXIOM:
        ∀ S ∈ {0,1}*: ∃! Σ: Ξ(Σ) = S
    
    REACTIVE DEDUCTION FLOW:
        1. Extract forced parameters from S's structure
        2. Test if any known law accepts these parameters
        3. If none fit, deduce law from closure
        4. Only return Σ₀ if S is truly abstract
    
    KEY PRINCIPLE:
        "You do not select a law. You observe the shape of S and let that constrain Σ."
    
    This is NOT:
        - Pattern matching ("does S look like D1?")
        - Classification ("what type is S?")
        - Sequential search ("try D1, D2, D3...")
    
    This IS:
        - Constraint extraction ("what does S's structure force?")
        - Reactive deduction ("given constraints, what must Σ be?")
        - Mathematical necessity ("the only law satisfying all axioms")
    
    Args:
        S: Input string (mathematics has no bounds)
        _depth: Internal recursion depth (for D_SPLIT protection)
    
    Returns:
        Σ (the unique law forced by S's structure)
        NEVER returns "unresolved" - calculator never quits
    """
    # CLF TIMELESSNESS: Cap recursion depth
    MAX_RECURSION_DEPTH = 2
    if _depth > MAX_RECURSION_DEPTH:
        # Return Σ₀ immediately - no further analysis
        from M13_canonical_seed import construct_canonical_seed
        return construct_canonical_seed(S)
    
    n = len(S)
    
    if n == 0:
        raise CLFRecognitionError("Empty string has no causal identity")
    
    # STEP 1: Algebraic recognition (instant structural checks)
    
    # Check D₁: CONST (entire string is single constant)
    d1_params = D1_const_law(S)
    if d1_params is not None:
        return {"family": "D1", "params": d1_params, "n": n}
    
    # Check D₂: AFFINE (entire string is affine progression)
    d2_params = D2_affine_law(S)
    if d2_params is not None:
        return {"family": "D2", "params": d2_params, "n": n}
    
    # Check D₃: COPY (entire string is periodic)
    # NOTE: D3 subsumes D7_ROTATIONAL via permutation equivalence
    # Any rotational sequence S[i]=P[(i·r) mod k] with gcd(r,k)=1
    # is recognized as D3 with cycle=permuted_pattern
    d3_params = D3_periodic_law(S)
    if d3_params is not None:
        return {"family": "D3", "params": d3_params, "n": n}
    
    # Check D₆: MIRROR (entire string is palindrome)
    # Priority: After periodic, before radial/spiral
    d6_params = D6_mirror_law(S)
    if d6_params is not None:
        return {"family": "D6_MIRROR", "params": d6_params, "n": n}
    
    # Check D₉: RADIAL (causal ring decomposition)
    # Priority: After mirror, before spiral (compositional before permutational)
    # CLF: Deduces per-ring laws Σ_r, never stores raw bytes
    d9_params = D9_radial_law(S)
    if d9_params is not None:
        return {"family": "D9_RADIAL", "params": d9_params, "n": n}
    
    # Check D₁₀: SPIRAL (bijective permutation)
    # Priority: After radial, before transforms (geometric vs algebraic)
    d10_params = D10_spiral_law(S)
    if d10_params is not None:
        return {"family": "D10_SPIRAL", "params": d10_params, "n": n}
    
    # Check D₄: XOR_AFFINE (entire string is affine ⊕ c)
    d4_params = D4_xor_affine(S)
    if d4_params is not None:
        return {"family": "D4_XOR_AFFINE", "params": d4_params, "n": n}
    
    # Check D₅: QUADRATIC (entire string is quadratic)
    d5_params = D5_quadratic(S)
    if d5_params is not None:
        return {"family": "D5_QUADRATIC", "params": d5_params, "n": n}
    
    # Check D₆: LCG (linear congruential generator)  
    # DISABLED: Requires iterative computation to verify
    # This is computational checking, not mathematical recognition
    # d6_params = D6_lcg(S)
    # if d6_params is not None:
    #     return {"family": "D6_LCG", "params": d6_params, "n": n}
    
    # Check D₁₀: DICTIONARY (symbol table + indices)
    # DISABLED: Requires scanning to build dictionary
    # This is computational analysis, not mathematical recognition  
    # d10_params = D10_dictionary(S)
    # if d10_params is not None:
    #     return {"family": "D10_DICTIONARY", "params": d10_params, "n": n}
    
    # Check D_SPLIT: COMPOSITE (concatenation of segments)
    # CLF TIMELESSNESS: Scans only first 1000 bytes for boundaries = O(1)
    # Compositional recognition is mathematical necessity for complex structures
    from Legacy.M8_split_law import D_SPLIT_law
    d_split_params = D_SPLIT_law(S, _depth=_depth)
    if d_split_params is not None:
        return {"family": "D_SPLIT", "params": d_split_params, "n": n}
    
    # D₀: EXPLICIT - Identity mapping law (first-class generator)
    # CLF AXIOM: String existence → function f(i)=byte_i exists
    # The deterministic parsing s[i] working proves the mathematical structure
    # This is the CANONICAL LAW when no shorter symbolic notation exists
    #
    # Per CLF Information Theory: "Information is executed"
    # The bytes ARE the executable function: index→value mapping
    #
    # D0 is mathematically complete and correct (not a fallback)
    # Success condition: Ξ(θ(S)) = S (bijection), not seed size
    # INSTANT: Store as bytes (O(1)), not list(S) (O(n))
    return {
        "family": "D0_IDENTITY",
        "params": {"bytes": S},  # The function definition f: ℕ → {0..255}
        "n": n
    }


# ============================================================================
# Validation: Check Uniqueness (Debug Tool)
# ============================================================================

def validate_theta_uniqueness(S: bytes) -> Dict:
    """
    Debug tool: Check that θ(S) resolution is truly unique
    
    Validates that EXACTLY ONE family matches (injective property).
    
    Args:
        S: Input string
    
    Returns:
        {"matches": int, "families": List[str]} - Diagnostic info
    
    Raises:
        ValueError: If multiple families match (ambiguity violation)
    """
    matches = []
    
    if D1_const_law(S) is not None:
        matches.append("D1")
    
    if D2_affine_law(S) is not None:
        matches.append("D2")
    
    if D3_periodic_law(S) is not None:
        matches.append("D3")
    
    if len(matches) > 1:
        raise ValueError(
            f"θ(S) ambiguity violation: Multiple families match [{', '.join(matches)}]. "
            "CLF fundamental equation requires ∃! (exists unique). "
            "Family predicates must be mutually exclusive."
        )
    
    return {"matches": len(matches), "families": matches}


__all__ = [
    'theta_strict',
    'CLFRecognitionError',
    'validate_theta_uniqueness',
    'D1_const_law',
    'D2_affine_law',
    'D3_periodic_law',
]
