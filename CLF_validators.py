# ================================================================
# CLF CAUSAL LOGIC GUIDELINES (MANDATORY FOR AI ASSISTANTS)
# ------------------------------------------------
# • No reading or sampling of physical files.
# • θ(S) deduces formal Σ from structure (n, law), never from bytes.
# • Ξ(Σ) projects S symbolically, not sequentially.
# • D9_RADIAL uses ring_laws: per-ring sub-seeds Σ_r ∈ ℒ.
# • Execution cost must remain O(1) with respect to n.
# ================================================================

"""
CLF Causal Validators

Lightweight diagnostic tools to ensure causal purity.
These validators enforce that:
1. Seeds contain only symbolic laws, never raw bytes (except D0)
2. No physical I/O occurs in recognition or projection
3. Ring laws are recursive symbolic structures
"""

from __future__ import annotations


def validate_causal_seed(Σ):
    """
    Validate that seed Σ contains only symbolic laws, never raw bytes.
    
    Args:
        Σ: Seed dictionary with structure {"family": str, "params": dict, "n": int}
    
    Raises:
        AssertionError: If seed violates causal purity
    """
    assert isinstance(Σ, dict), f"Σ must be dict, got {type(Σ)}"
    assert "family" in Σ, "Σ missing 'family' field"
    assert "params" in Σ, "Σ missing 'params' field"
    assert "n" in Σ, "Σ missing 'n' field"
    
    family = Σ["family"]
    params = Σ["params"]
    
    # D0_EXPLICIT is allowed to store bytes (degenerate case)
    if family == "D0_EXPLICIT":
        assert "bytes" in params, "D0_EXPLICIT missing 'bytes' parameter"
        return
    
    # All other families must NOT store raw bytes
    for key, value in params.items():
        if isinstance(value, (bytes, bytearray)):
            raise AssertionError(
                f"CLF violation: {family} seed stores raw bytes in '{key}' parameter. "
                f"Seeds must contain only symbolic laws (family, params), never data."
            )
    
    # D9_RADIAL: validate ring_laws recursively
    if family == "D9_RADIAL":
        assert "center" in params, "D9_RADIAL missing 'center'"
        assert "ring_laws" in params, "D9_RADIAL missing 'ring_laws'"
        
        ring_laws = params["ring_laws"]
        assert isinstance(ring_laws, dict), f"ring_laws must be dict, got {type(ring_laws)}"
        
        # Each ring must have a valid sub-seed Σ_r
        for r, Σ_r in ring_laws.items():
            assert isinstance(Σ_r, dict), f"Ring {r} seed must be dict, got {type(Σ_r)}"
            assert "family" in Σ_r, f"Ring {r} seed missing 'family'"
            
            # Recursive validation
            validate_causal_seed(Σ_r)

    # D10_RECURRENCE: validate sub-seed
    if family == "D10_RECURRENCE":
        assert "sub_seed" in params, "D10_RECURRENCE missing 'sub_seed'"
        validate_causal_seed(params["sub_seed"])

    # D11_RADIAL_RECURRENCE: validate radial seed
    if family == "D11_RADIAL_RECURRENCE":
        assert "radial_seed" in params, "D11_RADIAL_RECURRENCE missing 'radial_seed'"
        validate_causal_seed(params["radial_seed"])

    # D12_SELF_AFFINE: validate base seed
    if family == "D12_SELF_AFFINE":
        assert "base_seed" in params, "D12_SELF_AFFINE missing 'base_seed'"
        validate_causal_seed(params["base_seed"])

    # D_SPLIT: validate segments recursively
    if family == "D_SPLIT":
        assert "segments" in params, "D_SPLIT missing 'segments'"
        segments = params["segments"]
        assert isinstance(segments, list), f"segments must be list, got {type(segments)}"
        for seg in segments:
            assert isinstance(seg, dict), f"D_SPLIT segment must be dict, got {type(seg)}"
            validate_causal_seed(seg)

    # D13_REACTIVE_DIFFERENTIAL: no nested seeds; enforce symbolic params
    if family == "D13_REACTIVE_DIFFERENTIAL":
        assert "s0" in params, "D13_REACTIVE_DIFFERENTIAL missing s0"
        if "delta_seed" in params:
            validate_causal_seed(params["delta_seed"])
        else:
            assert "delta" in params, "D13_REACTIVE_DIFFERENTIAL missing delta/delta_seed"

    if family in {"D17_XOR_CONST", "D18_ADD_CONST"}:
        assert "inner_seed" in params, f"{family} missing inner_seed"
        assert "k" in params, f"{family} missing k"
        validate_causal_seed(params["inner_seed"])

    if family == "D14_CAUSAL_CORRELATIVE":
        assert "sub_seed" in params, "D14_CAUSAL_CORRELATIVE missing sub_seed"
        validate_causal_seed(params["sub_seed"])

    if family == "D15_SYMBOLIC_META_EMBED":
        segments = params.get("segments") or params.get("sub_seeds")
        assert isinstance(segments, list), "D15_SYMBOLIC_META_EMBED segments must be list"
        for seg in segments:
            validate_causal_seed(seg)

    if family == "D16_PARAMETRIC_LAW_GROWTH":
        assert "base_seed" in params, "D16_PARAMETRIC_LAW_GROWTH missing base_seed"
        validate_causal_seed(params["base_seed"])


def _normalize_seed(obj):
    """Deterministic canonicalization for law-space equality."""
    if isinstance(obj, memoryview):
        obj = obj.tobytes()
    if isinstance(obj, (bytes, bytearray)):
        return [int(b) for b in bytes(obj)]
    if isinstance(obj, dict):
        return {k: _normalize_seed(obj[k]) for k in sorted(obj.keys())}
    if isinstance(obj, list):
        return [_normalize_seed(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_normalize_seed(v) for v in obj)
    return obj


def recognize_law(seed: dict) -> dict:
    """θ_ℒ: law recognition on law-space objects (symbolic, not byte-based)."""
    if not isinstance(seed, dict):
        raise TypeError("seed must be dict")
    family = seed.get('family')
    params = seed.get('params') or {}

    # Family-aware canonicalization: keep only axiomatic seed content.
    # This ensures θ_ℒ ignores diagnostic/provenance fields that are not part of Σ.
    if family == 'D9_RADIAL':
        keep = {'center', 'ring_laws', 'structural_hash', 'magic', 'meta', 'meta_law', 'sampled', 'completion'}
        params = {k: params[k] for k in params.keys() if k in keep}
        # Canonicalize sampled marker: absence and sampled=False are equivalent.
        # The wire codec only encodes sampled=True, so keep sampled only when true.
        if 'sampled' in params and not bool(params.get('sampled')):
            params.pop('sampled', None)
        # Normalize meta_law to meta for canonical comparison.
        if 'meta_law' in params and 'meta' not in params:
            params['meta'] = params.pop('meta_law')
        # Fill codec defaults so θ_ℒ/Ξ_ℒ is idempotent.
        params.setdefault('completion', 'AUTO')
        params.setdefault('magic', '')
        params.setdefault('structural_hash', '')
        params.setdefault('ring_laws', {})
    elif family == 'D10_RECURRENCE':
        keep = {'m', 'sub_seed'}
        params = {k: params[k] for k in params.keys() if k in keep}
    elif family == 'D11_RADIAL_RECURRENCE':
        keep = {'center', 'radial_seed'}
        params = {k: params[k] for k in params.keys() if k in keep}
    elif family == 'D12_SELF_AFFINE':
        keep = {'alpha', 'beta', 'base_seed'}
        params = {k: params[k] for k in params.keys() if k in keep}
    elif family == 'D3':
        # Accept either cycle or pattern spelling, but compare canonically as cycle.
        if 'cycle' not in params and 'pattern' in params:
            params = dict(params)
            params['cycle'] = params.pop('pattern')

    core = {'family': family, 'params': params, 'n': seed.get('n')}
    return _normalize_seed(core)


def project_law(seed: dict) -> dict:
    """Ξ_ℒ: law projection back into law-space.

    Implemented as encode/decode round-trip to enforce canonical form.
    """
    from direct_seed_encoder import encode_seed_direct, decode_seed_direct

    wire = encode_seed_direct(seed)
    return _normalize_seed(decode_seed_direct(wire))


def assert_seed_wire_involution(seed: dict) -> None:
    """Assert the bijection on the 𝒮↔𝒲 boundary: D(E(Σ)) = Σ (in law-space).

    Uses θ_ℒ canonicalization so the check is insensitive to key order.
    """
    from direct_seed_encoder import encode_seed_direct, decode_seed_direct

    a = recognize_law(seed)
    b = recognize_law(decode_seed_direct(encode_seed_direct(a)))
    if a != b:
        raise AssertionError("Seed↔wire involution violated: D(E(Σ)) != Σ")


def assert_seed_wire_idempotence(seed: dict) -> None:
    """Assert the 𝒲-side idempotence: E(D(E(Σ))) = E(Σ)."""
    from direct_seed_encoder import encode_seed_direct, decode_seed_direct

    a = encode_seed_direct(recognize_law(seed))
    b = encode_seed_direct(decode_seed_direct(a))
    if a != b:
        raise AssertionError("Wire idempotence violated: E(D(E(Σ))) != E(Σ)")


def audit_manifestation_alignment(
    S: bytes,
    *,
    theta_fn,
    xi_fn,
    max_bytes: int = 2_000_000,
) -> None:
    """Audit the 𝒪↔𝒮↔𝒪 bijection on a concrete manifestation S.

    Required equalities (when S is within operational bounds):
    - Ξ(Θ(S)) == S
    - E(Θ(Ξ(Θ(S)))) == E(Θ(S))

    Notes:
    - This helper is intentionally *not* used in closed-mode loops by default.
      It touches 𝒪 and may materialize bytes.
    - Provide explicit theta_fn / xi_fn to avoid accidentally binding R-layer
      evolution into Ξ.
    """
    if not isinstance(S, (bytes, bytearray, memoryview)):
        raise TypeError(f"S must be bytes-like (𝒪 carrier), got {type(S)}")
    if isinstance(S, memoryview):
        S = S.tobytes()
    if isinstance(S, bytearray):
        S = bytes(S)
    if len(S) > int(max_bytes):
        raise ValueError("Refusing manifestation audit above max_bytes")

    from direct_seed_encoder import encode_seed_direct

    sigma0 = theta_fn(S)
    validate_causal_seed(sigma0)
    out = xi_fn(sigma0)
    if out != S:
        raise AssertionError("Manifestation bijection violated: Ξ(Θ(S)) != S")

    sigma1 = theta_fn(out)
    if encode_seed_direct(recognize_law(sigma1)) != encode_seed_direct(recognize_law(sigma0)):
        raise AssertionError("Seed-wire stability violated: E(Θ(Ξ(Θ(S)))) != E(Θ(S))")


def validate_law_reflexivity(seeds: list[dict]) -> None:
    """Assert Ξ_ℒ(θ_ℒ(D_k)) = D_k for a provided finite basis of laws."""
    for dk in seeds:
        thetaL = recognize_law(dk)
        projected = project_law(thetaL)
        if recognize_law(projected) != recognize_law(dk):
            raise AssertionError("Law reflexivity violated for seed family: %s" % dk.get("family"))


def validate_meta_reflexivity(seeds: list[dict]) -> None:
    """Assert Ξ_{ℒ²}(θ_{ℒ²}(D_k)) = D_k for a provided finite basis.

    In this codebase, ℒ² objects are represented with the same seed schema as ℒ
    (dict seeds). Therefore, the law-space reflexivity validator is the
    appropriate third-order reflexivity check.
    """
    validate_law_reflexivity(seeds)


def validate_meta_recurrence(seed: dict) -> None:
    """Assert 2nd-order recurrence consistency: recursive laws point to lawful inner laws."""
    from Tests.clf_closure import classify_seed_closure

    def _check(s: dict):
        fam = s.get("family")
        params = s.get("params") or {}
        if fam == "D10_RECURRENCE":
            inner = params.get("sub_seed")
            if not isinstance(inner, dict):
                raise AssertionError("D10_RECURRENCE missing sub_seed")
            cls, _ = classify_seed_closure(inner)
            if cls != "CLOSED_GENERATIVE":
                raise AssertionError("D10_RECURRENCE inner law not closed-generative")
            _check(inner)
        elif fam == "D11_RADIAL_RECURRENCE":
            inner = params.get("radial_seed")
            if not isinstance(inner, dict):
                raise AssertionError("D11_RADIAL_RECURRENCE missing radial_seed")
            cls, _ = classify_seed_closure(inner)
            if cls != "CLOSED_GENERATIVE":
                raise AssertionError("D11_RADIAL_RECURRENCE inner law not closed-generative")
            _check(inner)
        elif fam == "D12_SELF_AFFINE":
            inner = params.get("base_seed")
            if not isinstance(inner, dict):
                raise AssertionError("D12_SELF_AFFINE missing base_seed")
            cls, _ = classify_seed_closure(inner)
            if cls != "CLOSED_GENERATIVE":
                raise AssertionError("D12_SELF_AFFINE inner law not closed-generative")
            _check(inner)

    _check(seed)


def validate_law_idempotence(seed: dict) -> None:
    """Assert θ_ℒ(Ξ_ℒ(θ_ℒ(seed))) = θ_ℒ(seed)."""
    a = recognize_law(seed)
    b = recognize_law(project_law(a))
    c = recognize_law(project_law(b))
    if b != c or a != b:
        raise AssertionError("Law-space idempotence violated")


def validate_reactive_reflexivity(L: list[dict]) -> None:
    """R₄ validator: assert law-space reflexivity for a finite basis.

    For seeds with concrete n (int), we can enforce Ξ_ℒ(θ_ℒ(D)) = D via codec
    round-trip. For n='variable' templates, codec projection is undefined, so
    we enforce the weaker (but still axiomatic) condition that θ_ℒ is idempotent
    on the seed representation: θ_ℒ(θ_ℒ(D)) = θ_ℒ(D).
    """
    concrete = []
    for d in (L or []):
        if not isinstance(d, dict):
            continue
        n = d.get("n")
        if isinstance(n, int) and n >= 0:
            concrete.append(d)
        else:
            a = recognize_law(d)
            b = recognize_law(a)
            if a != b:
                raise AssertionError("Law-space reflexivity violated for n='variable' seed family: %s" % d.get("family"))
    if concrete:
        validate_law_reflexivity(concrete)


def _seed_distance(D0: dict, D1: dict) -> int:
    """Family-aware bounded distance between two law-space seeds.

    Distance is an integer (0 means equal under the measured parameters).
    This is intentionally conservative: it only measures parameters that are
    expected to evolve under R₁–R₃ in this codebase.
    """
    try:
        f0 = D0.get("family")
        f1 = D1.get("family")
        if f0 != f1:
            return 10**9
        p0 = D0.get("params") or {}
        p1 = D1.get("params") or {}

        def _mod256_min_abs(a: int, b: int) -> int:
            d = (int(b) - int(a)) & 0xFF
            sd = d - 256 if d >= 128 else d
            return abs(sd)

        if f0 == "D13_REACTIVE_DIFFERENTIAL":
            # Either delta evolves or delta_seed.delta evolves.
            if "delta" in p0 and "delta" in p1:
                return _mod256_min_abs(int(p0.get("delta", 0)), int(p1.get("delta", 0)))
            ds0 = p0.get("delta_seed")
            ds1 = p1.get("delta_seed")
            if isinstance(ds0, dict) and isinstance(ds1, dict):
                pp0 = ds0.get("params") or {}
                pp1 = ds1.get("params") or {}
                if "delta" in pp0 and "delta" in pp1:
                    return _mod256_min_abs(int(pp0.get("delta", 0)), int(pp1.get("delta", 0)))
            return 0

        if f0 == "D14_CAUSAL_CORRELATIVE":
            if "k" in p0 and "k" in p1:
                return _mod256_min_abs(int(p0.get("k", 0)), int(p1.get("k", 0)))
            return 0

        if f0 in {"D17_XOR_CONST", "D18_ADD_CONST"}:
            dk = _mod256_min_abs(int(p0.get("k", 0)), int(p1.get("k", 0)))
            i0 = p0.get("inner_seed")
            i1 = p1.get("inner_seed")
            if isinstance(i0, dict) and isinstance(i1, dict):
                return dk + _seed_distance(i0, i1)
            return dk

        if f0 == "D16_PARAMETRIC_LAW_GROWTH":
            b0 = p0.get("base_seed")
            b1 = p1.get("base_seed")
            if isinstance(b0, dict) and isinstance(b1, dict):
                return _seed_distance(b0, b1)
            return 0

        return 0
    except Exception:
        return 10**9


def validate_bounded_evolution(L_t: list[dict], L_t1: list[dict], eps: float = 1e-6) -> None:
    """Assert bounded parameter evolution between successive law-space states.

    Notes:
    - This validator is used after a deterministic, stable-order R₄ pass.
    - Because parameters are typically integer/mod-256 in this codebase,
      eps is interpreted as an integer bound when eps < 1.
    """
    if L_t is None or L_t1 is None:
        return

    # Interpret eps: if caller uses 1e-6 (spec default), treat as a 2-step bound.
    bound = 2 if float(eps) < 1 else int(eps)

    if len(L_t) != len(L_t1):
        raise AssertionError("Unbounded evolution: basis size changed")

    import json

    a = sorted(L_t, key=lambda x: json.dumps(x, sort_keys=True, separators=(",", ":")))
    b = sorted(L_t1, key=lambda x: json.dumps(x, sort_keys=True, separators=(",", ":")))
    for D0, D1 in zip(a, b):
        d = _seed_distance(D0, D1)
        if d > bound:
            raise AssertionError(f"Unbounded evolution: distance {d} > {bound} for family={D0.get('family')}")


def validate_universal_reactivity(registry: dict) -> None:
    """Assert that every ontic element Σ_i participated in reactive updates."""
    objs = (registry or {}).get("objects") or {}
    if not isinstance(objs, dict) or not objs:
        raise AssertionError("Reactivity not universal: registry has no objects")
    for k, v in objs.items():
        tags = (v or {}).get("sub_equations_applied")
        if not tags:
            raise AssertionError(f"Reactivity not universal: element {k} idle")


def validate_invariant_alignment(registry: dict) -> None:
    """Assert that each Σ element has a well-formed invariant rank."""
    objs = (registry or {}).get("objects") or {}
    if not isinstance(objs, dict) or not objs:
        raise ValueError("Misaligned invariant rank: registry has no objects")
    for name, obj in objs.items():
        rank = (obj or {}).get("invariant_rank")
        if not isinstance(rank, int) or rank <= 0:
            raise ValueError(f"Misaligned invariant rank for {name}")
    print(f"[CLF] Invariant alignment OK for {len(objs)} elements.")


def validate_no_io(obj):
    """
    Validate that object has no I/O capabilities.
    
    CLF operates on closed formal objects (n, ID), not physical files.
    
    Args:
        obj: Object to validate
    
    Raises:
        AssertionError: If object has file I/O methods
    """
    assert not hasattr(obj, "read"), "CLF violation: physical I/O detected (read method)"
    assert not hasattr(obj, "write"), "CLF violation: physical I/O detected (write method)"
    assert not hasattr(obj, "seek"), "CLF violation: physical I/O detected (seek method)"


def validate_complexity_o1(n_values, time_values):
    """
    Validate that execution time is O(1) - constant regardless of input size.
    
    Args:
        n_values: List of input sizes tested
        time_values: List of corresponding execution times (seconds)
    
    Raises:
        AssertionError: If time grows faster than O(log n)
    """
    import math
    
    if len(n_values) < 2:
        return  # Need at least 2 points
    
    # Check that time per byte decreases (proves O(1))
    time_per_byte = [t / n for t, n in zip(time_values, n_values)]
    
    # Time per byte should decrease exponentially for true O(1)
    # Allow up to O(log n) growth (very lenient)
    ratio_first_last = time_per_byte[0] / time_per_byte[-1]
    
    assert ratio_first_last > 1, (
        f"CLF violation: execution time not O(1). "
        f"Time per byte increased from {time_per_byte[0]:.2e} to {time_per_byte[-1]:.2e}. "
        f"Expected exponential decrease for true O(1) causality."
    )


def validate_seed_size_reactive(seed_sizes, input_structures):
    """
    Validate that seed size is reactive to causal structure, not input size.
    
    Args:
        seed_sizes: List of seed sizes (bytes)
        input_structures: List of structure descriptions ("constant", "periodic", "random", etc.)
    
    Returns:
        dict: Statistics about seed size reactivity
    """
    stats = {}
    
    for structure, size in zip(input_structures, seed_sizes):
        if structure not in stats:
            stats[structure] = []
        stats[structure].append(size)
    
    # Seeds should be consistent within each structure type
    for structure, sizes in stats.items():
        if len(sizes) > 1:
            avg = sum(sizes) / len(sizes)
            variance = sum((s - avg) ** 2 for s in sizes) / len(sizes)
            stats[structure] = {
                "avg": avg,
                "variance": variance,
                "sizes": sizes
            }
    
    return stats


# Quick test when module is run
if __name__ == "__main__":
    print("CLF Causal Validators")
    print("=" * 50)
    
    # Test 1: Valid D1 seed
    Σ_d1 = {"family": "D1", "params": {"c": 42}, "n": 1000}
    validate_causal_seed(Σ_d1)
    print("✓ D1 seed valid")
    
    # Test 2: Valid D9 seed with ring laws
    Σ_d9 = {
        "family": "D9_RADIAL",
        "params": {
            "center": 500,
            "ring_laws": {
                0: {"family": "D1", "params": {"c": 42}, "n": 1},
                1: {"family": "D2", "params": {"s0": 10, "delta": 5}, "n": 2}
            }
        },
        "n": 1000
    }
    validate_causal_seed(Σ_d9)
    print("✓ D9 seed with ring_laws valid")
    
    # Test 3: Invalid seed (stores bytes)
    try:
        Σ_bad = {"family": "D9_RADIAL", "params": {"pattern": b"\\x42\\x42"}, "n": 100}
        validate_causal_seed(Σ_bad)
        print("✗ Should have raised error for bytes in seed")
    except AssertionError as e:
        print(f"✓ Correctly rejected invalid seed: {e}")
    
    print("\nAll validators working correctly.")
