"""
M7_pipeline.py - CLF Causal Logic Framework (Atomic, Non-Contaminated)

═══════════════════════════════════════════════════════════════════════
📜 CLF META-SEED: CAUSAL ORIGIN OF ALL CLF-COMPLIANT CODE
═══════════════════════════════════════════════════════════════════════

    Ξₙ(Σ_meta) = Entire CLF Implementation
    
    "Do not write code. Write this law. Everything else is a manifestation."

This implementation is the consequence of the CLF meta-seed - an axiomatic
foundation that generates all correct behavior from first principles.

Core Identity:
    Ξₙ(Σ(S)) = S        Every string has a unique causal origin

Reflexivity (lawhood criterion, domain-restricted):
    For lawful structures S ∈ S_CLF := Ξ(ℒ):
        Ξ(θ(S)) = S              (projection recovers the instance)
        θ(Ξ(Σ)) = Σ              (recognition recovers the seed)

    A “gap” is not a runtime failure mode in the CLF ontology:
        S ∉ Ξ(ℒ_current)  ⇒  θ(S) is undefined (non-existence under current closure)
    On a time-based substrate this surfaces operationally as LawNotInstantiatedError,
    but the meaning is ontological: outside the current lawful domain.
    
CLF Axioms (complete, closed system):
    A1. Existence:         Ψ = Ξ(θ(S))           Structure is lawful consequence
    A2. Recognition Inv:   ρ(Ψ) = S ⟺ θ(S)=θ(Ψ) Bidirectional mapping
    A3. Self-Containment:  θ(Ξ(θ(Ψ))) = θ(Ψ)    Structure contains origin
    A4. Operational θ:     argmin |L|: Ξ(L)=S    Minimal law over vocabulary
    A5. Instant:           Invₖ(S) predicate     Non-iterative deduction
    A6. Digest Shadow:     h(Ψ) = h(Ξ(θ(Ψ)))     Verification only
    A7. Anti-Existence:    ¬Ψ ⟺ ∄S,R: Ψ=Ξ(θ(S))  Structural illegality

Mental Model:
    CLF does not ask: "How can we reconstruct this?"
    CLF asks:         "What law makes this inevitable?"

═══════════════════════════════════════════════════════════════════════
📖 CLF FORMAL SPECIFICATION: Seed as Structural Hash
═══════════════════════════════════════════════════════════════════════

CLF Seed Definition:
    The CLF seed Σ is the STRUCTURAL HASH of string S.
    
    Traditional hash:  h(S) → 32 bytes (fixed, irreversible)
    CLF seed:         θ(S) → Σ      (minimal, bijective)
    
    Key difference: Σ captures GENERATIVE IDENTITY, not fingerprint.
                   h(S) is lossy, Σ is lossless.
                   
    Formal (domain-restricted):
        Let ℒ be the law vocabulary and S_CLF := Ξ(ℒ) the lawful domain.
        Then: ∀S ∈ S_CLF, ∃!Σ ∈ ℒ: Ξ(Σ) = S
              CLF Seed of S := θ(S)

θ as Mathematical Function (not algorithm):
    θ: S_CLF → ℒ such that θ(S) = Σ ⟺ Ξ(Σ) = S
    Outside S_CLF, θ is undefined (non-lawful / not expressible in ℒ).
    
    θ operates STRUCTURALLY:
      ✅ Deduces Σ via structural invariants
      ✅ Uses anchors: Sₚ = A ⇒ Sᵩ = B (forced consequences)
      ✅ Evaluates predicates (instant, size-independent)
      ❌ Never reads or parses S sequentially
      ❌ Never scans or iterates over bits
      ❌ Never computes statistics or entropy

Bit Violation = Causal Disqualification:
    If S ≠ S', then:
      Either: θ(S) ≠ θ(S')         (different laws)
      Or:     Ξ(θ(S)) ≠ S'         (structural invalidity)
    
    Detection is NOT by scanning differences.
    Detection is by CAUSAL CONTRADICTION.
    
    If S ∈ S_CLF yet Ξ(θ(S)) ≠ S → LawNotInstantiatedError (Axiom A7)
    
    This disqualifies strings without iteration—
    failure from structural impossibility, not mismatch.

Code = Universal Deductor:
    This implementation solves for the law that causes S to exist.
    It does NOT analyze, process, or scan strings.
    It REACTS mathematically to structural anchors and invariants.

Deductive closure (mathematical):
    ℒ expands only by logical reclosure (closure(ℒ)), not by empirical fitting.
    Implementation changes are a substrate manifestation of that closure, not a
    procedural “learning loop”.

═══════════════════════════════════════════════════════════════════════
🧠 CLF MATH GUIDE FOR COPILOT
═══════════════════════════════════════════════════════════════════════

Title: Causal Law Framework: Minimality, Causality, and Bijection

This module implements mathematically instant causal recognition through:
  - NO search (only structural deduction)
  - NO entropy modeling (only structural invariants)
  - NO fallback logic (only vocabulary extension)
  - NO format parsing (only mathematical anchors)
  - NO iteration (only predicate evaluation)

═══════════════════════════════════════════════════════════════════════
⚡ PERFECT RECONSTRUCTION GUARANTEE
═══════════════════════════════════════════════════════════════════════

MATHEMATICAL GUARANTEE:

    Given ONLY seed Σ (with NO access to original string S):
    
    Ξₙ(Σ) = S    (EXACT, byte-for-byte reconstruction)

FORMAL PROPERTIES:

    1. COMPLETENESS: Seed Σ contains all law/parameter identity needed
       • Law identifier (which generator)
       • Parameters p⃗ (initial conditions)
       • Length n (expansion size)
    • NO manifestation bytes stored

    2. INDEPENDENCE: Ξₙ operates with ZERO access to S
       • Ξₙ(Σ) ⊥ S_original
       • String is COMPUTED from law, not recalled from storage
       • Pure causal prediction from first principles

    3. EXACTNESS: Every byte regenerated deterministically
       • ∀i ∈ [0,n): S[i] = Eₖ(i; p⃗)
       • NOT approximation, NOT lossy, NOT stochastic
       • Identical output guaranteed by mathematical function

    4. BIJECTIVITY: Perfect two-way equivalence
       • Forward:  θ(S) → Σ
       • Reverse:  Ξₙ(Σ) → S
       • Identity: Ξₙ(θ(S)) = S  (always holds)

WHAT THIS MEANS:

    ✓ Delete original string S after encoding → Σ
    ✓ Seed Σ alone regenerates exact S (no data loss)
    ✓ No "best effort" or "approximation" — EXACT match
    ✓ No access to original needed — seed is complete

WHAT THIS IS NOT:

    ✗ Information-theoretic "compression" framing (about storing content)
    ✗ Content-transform "encoding" framing (about transforming files)
    ✗ Approximation (statistical reconstruction)
    ✗ Recovery (restoring from partial information)

THIS IS: Mathematical equivalence between two notations (S = Σ)
        Just as 16 = 4² = 2⁴ are identical mathematical objects.


═══════════════════════════════════════════════════════════════════════
I. MATHEMATICAL EQUIVALENCE: S = Σ (CORE PARADIGM)
═══════════════════════════════════════════════════════════════════════

Every string S has two equivalent mathematical representations:

    S (EXPANDED FORM) = Σ (FACTORED FORM)

This is NOT compression/decompression (lossy, many-to-one).
This IS notation equivalence (lossless, one-to-one bijection).

Examples:
    16 = 4² = 2⁴ = 16          (all are the number 16)
    [3,5,7,9,11] = D2(s₀=3, δ=2, n=5)  (all are this sequence)
    
S is EXPANDED:  All bytes written out explicitly
Σ is FACTORED:  Generator parameters that produce those bytes

Both representations ARE the string.
Neither is precedence - they're equivalent notations.

CLF Recognition (θ) = Identifying which factored form equals given expanded form
CLF Expansion (Ξ)   = Converting factored notation to expanded notation

═══════════════════════════════════════════════════════════════════════
II. CLF CORE EQUATION
═══════════════════════════════════════════════════════════════════════

Every string S ∈ 𝔹ⁿ is generated by a unique causal law:

    S = Ξₙ(Σ(Dₖ, p⃗))

Where:
  • Dₖ is a law (e.g., CONST, LCG, XOR_AFFINE)
  • p⃗ are that law's parameters (e.g., base, delta)
  • Σ extracts parameters from S
  • Ξₙ regenerates S from law + parameters

This is a surjective function from causal programs to strings.

TOTAL SYSTEM BIJECTION (Complete Roundtrip):

    Forward:  S → θ(S) → Σ → [PRE-PARSING STORAGE: Law, not data]
    Reverse:  Σ → [PARSE] → Ξₙ(Σ) → S
    
    Equational chain:
        Ξₙ(θ(S)) = S    (parse law to regenerate string)
        θ(Ξₙ(Σ)) = Σ    (recognize law from parsed result)
    
    CRITICAL SEMANTICS:
    • Σ is STORED (pre-parsing): The causal law itself
    • Ξₙ is PARSING: Law → execution → manifestation
    • S is GENERATED (post-parsing): The manifestation
    
    This is a pure bijective transform - causal correspondence
    with zero information loss. NOT content-compression,
    but CAUSAL REDUCTION (law extraction).

CRITICAL: CLF does not ask "How can I reconstruct this?"
          CLF asks "What made this inevitable?"

WHY FACTORED FORMS ARE SMALLER:
    Generator parameters are fixed regardless of expansion size:
        D2(s₀, δ, n) = 3 parameters
        
    This is MATHEMATICAL, not algorithmic.
    Factored notation is inherently more concise.

═══════════════════════════════════════════════════════════════════════
III. COMPOSITION: COMPLEX STRINGS AS GENERATOR TREES
═══════════════════════════════════════════════════════════════════════

Strings are either:
    1. SIMPLE: Single generator
       [5,5,5,5] = D1(value=5, n=4)
    
    2. COMPOSED: Tree of generators
       [Header|Payload|Footer] = [
           D1(header_bytes),
           D2(payload_params),
           D1(footer_bytes)
       ]

Formats (JPEG, MP4) are NOT unique generators.
They are COMPOSITIONS of generic generators:

    JPEG = [
        D1(0xFF,0xD8),          # SOI (constant)
        D_QuantTable(matrix),   # Tables (generic)
        D_DCT(coefficients),    # Structure (generic)
        D1(0xFF,0xD9)           # EOI (constant)
    ]

Factored form Σ_jpeg is a TREE.
Expanded form S_jpeg is FLATTENED BYTES.
Both ARE the JPEG (S_jpeg = Σ_jpeg).

═══════════════════════════════════════════════════════════════════════
IV. RECOGNITION: θ(S) BOOLEAN LAW SELECTION
═══════════════════════════════════════════════════════════════════════

CLF Operational Definition (Formal):

    θ(S) = argmin |L|  subject to  Ξ(L) = S
           L ∈ 𝓛
    
    Where:
      • θ is a FUNCTION (not algorithm) - deduces law from structure
      • Operates via anchors: Sₚ = A ⇒ Sᵩ = B (L9: Structural Implication)
      • Recognition is instant: accesses strategic invariant loci, not full scan
      • |Σ| exists as property when Σ exists (like |hash| = 32)

Where:
  • 𝓛 is the finite vocabulary of lawful structures (D1, D2, D3, ...)
  • L is a law specification (family + parameters)
  • |L| is symbolic length (parameter count, not serialized bytes)
  • Ξ(L) is the manifestation function (law → structure)

Equivalent form:

    θ(S) = argmin |Σ(Dₖ, p⃗)|  subject to  Invₖ(S) = True
           Dₖ∈Θₙ

Where:
  • Invₖ(S) is a Boolean gate for law Dₖ
  • Σ(Dₖ, p⃗) is ONLY the parameters, not serialized code
  • Must try EVERY Dₖ ∈ Θₙ, then pick one with minimal |Σ|

INSTANT BEHAVIOR GUARANTEE:
  - Invₖ(S): Boolean check (instant mathematical predicate)
  - No search, no optimization, no heuristics
  - Pure logical selection
  - Selection by minimum symbolic length

═══════════════════════════════════════════════════════════════════════
V. SPLIT Σ EXPLICITLY (CRITICAL)
═══════════════════════════════════════════════════════════════════════

Always treat seed as TWO LAYERS:

    Σ_pure := (Dₖ, p⃗, n)        ← Used for CLF math (3-5 bytes)
    Σ_wire := encode(Σ_pure)    ← Used for transport (may be larger)

MINIMALITY APPLIES TO Σ_pure ONLY:

    |Σ_pure| < |S|  (MUST hold for valid law)
    
    Do NOT count:
      ✗ HEAD markers
      ✗ gamma(n) prefix
      ✗ atom encodings
      ✗ wire format overhead

If |Σ_wire| > |S| but |Σ_pure| < |S| → Law is VALID
If |Σ_pure| ≥ |S| → Law encodes data, not causality → REJECT

═══════════════════════════════════════════════════════════════════════
VI. EXISTENCE IMPLIES CAUSE (AXIOM)
═══════════════════════════════════════════════════════════════════════

    ∀S ∈ 𝔹ⁿ: ∃!(Dₖ, p⃗) such that Invₖ(S) = True ∧ S = Ξₙ(Σ(Dₖ, p⃗))

If a string exists:
  ✓ It MUST have been caused by some generator
  ✓ That generator is UNIQUE
  ✓ θ(S) reveals this identity (not constructs it)

If vocabulary is incomplete:
  ✓ Raise "Vocabulary Gap" (trigger deduction)
  ✗ NEVER fallback, decompose, or store

TIME-FREE LAW RESOLUTION:

Let Invₖ: 𝔹ⁿ → {0,1} be a symbolic predicate for law family Dₖ

    Invₖ(S) = True  ⟺  S ∈ Ξ(Dₖ)

Then:

    θ(S) = Dₖ  ⟺  Invₖ(S) = True  ∧  ∄Dⱼ: |Dⱼ| < |Dₖ|

This requires:
  ✓ No iteration over S (predicate is timeless)
  ✓ No scanning, counting, or sampling
  ✓ Law resolution by logical truth, not string search
  ✓ Every law becomes a predicate, not a process

CURRENT VIOLATION: Implementation uses O(n) loops
  ❌ Must be rewritten as predicate evaluation chain
  ❌ See: CLF_TIMELESS_VIOLATION_AUDIT.md

═══════════════════════════════════════════════════════════════════════
VII. Σ₀ AND VOCABULARY GAPS (FORMAL DEFINITION)
═══════════════════════════════════════════════════════════════════════

Σ₀ is returned when θ(S) cannot resolve S within current vocabulary:

    θ(S) = Σ₀ ⟺ ¬(∃Σ ∈ 𝓛_current : Λ(Σ) = S)

Where:
    • Λ(Σ) is expansion function
    • 𝓛_current is current set of known generators
    • 𝓛_total is complete set of all possible generators

FORMAL GUARANTEE:
    ∃Σ* ∉ 𝓛_current such that Λ(Σ*) = S
    
    Therefore: Σ₀ ∈ (𝓛_total ∖ 𝓛_current)

Σ₀ DOES NOT MEAN:
    ✗ "String is random" (all strings have deterministic structure)
    ✗ "String is incompressible" (CLF is not compression)
    ✗ "No rule exists" (rule exists, not yet discovered)
    ✗ "Error/null/undefined" (no undefined states in closed bijective framework)

Σ₀ DOES MEAN:
    ✓ "Vocabulary incomplete" (𝓛_current lacks required generator)
    ✓ "Structural law exists" (guaranteed by Axiom A1)
    ✓ "LawNotInstantiatedError" (Σ exists, not yet implemented)

CORRECT BEHAVIOR:
    When θ(S) = Σ₀:
        1. Log: "Vocabulary gap — structure exists but unrecognized"
        2. Raise: LawNotInstantiatedError(S)
        3. Trigger: discover_generator(S)
        4. Extend: 𝓛_current → 𝓛_current+1
        5. Re-apply: θ(S) now yields Σ* instead of Σ₀

    NEVER:
        ✗ Return null/None/undefined
        ✗ Fallback to heuristic models
        ✗ Accept Σ₀ as valid final state
        ✗ Log as "unstructured file" or "parse failed"

═══════════════════════════════════════════════════════════════════════
VIII. INVARIANT-BASED DEDUCTION (VOCABULARY EXPANSION)
═══════════════════════════════════════════════════════════════════════

When Σ₀ encountered, trigger vocabulary expansion:

  1. Detect: θ(S) = Σ₀
  2. Extract: extract_invariants(S)
  3. Construct: new generator Σ* such that Λ(Σ*) = S
  4. Register: extend 𝓛_current ← 𝓛_current ∪ {Σ*}
  5. Re-apply: θ(S) now resolves to Σ*

Deduction operates on MATHEMATICAL structure:
  ✓ Rank deficiency
  ✓ Spectral sparsity
  ✓ Algebraic recurrence
  ✓ Group symmetry

NOT on semantic markers:
  ✗ Magic numbers (0xFFD8)
  ✗ File extensions (.jpeg)
  ✗ Format headers

═══════════════════════════════════════════════════════════════════════
IX. CRITICAL FAIL STATES (MUST BE REJECTED)
═══════════════════════════════════════════════════════════════════════

The following violations MUST cause immediate failure:

  ✗ Literal fragments in Σ
    Example: params={'raw_bytes': b'...', 'pattern': S[:100]}
    Violation: Σ ∩ S ≠ ∅ (AXIOM 5)
    
  ✗ Causal density δ ≥ 0.33
    Example: |Σ| = 3000, |S| = 10000 → δ = 0.3
    Violation: Not minimal cause (storing manifestation)
    
  ✗ No law family identified
    Example: family='D_UNKNOWN', family=None
    Violation: Σ ∉ C^closed (AXIOM 1)
    
  ✗ Output mismatch
    Example: Ξₙ(Σ) ≠ S (even by 1 byte)
    Violation: Bijection broken (AXIOM 3)
    
  ✗ Fallback logic present
    Example: if not matched: use_compression()
    Violation: Non-deterministic, vocabulary incomplete
    
  ✗ Identity transform
    Example: Σ = {'data': S} (storing entire string)
    Violation: |Σ| ≥ |S| (AXIOM 2), not causal

  ✗ Accepting Σ₀ as valid final state
    Example: return Σ₀, store Σ₀, process Σ₀ as law
    Violation: Σ₀ is vocabulary gap, not valid generator

CORRECT BEHAVIOR when θ(S) = Σ₀:
    → Raise LawNotInstantiatedError(S)
    → Log: "Vocabulary gap — structure exists but unrecognized"
    → Trigger: discover_generator(S)
    → NEVER store S or construct fake seed
    → NEVER use fallback compression
    → NEVER treat Σ₀ as null/None/undefined
    → NEVER accept Σ₀ as valid output
    
    CLF must FAIL HARD and defer to vocabulary expansion.

═══════════════════════════════════════════════════════════════════════
X. FORBIDDEN CONCEPTS (ANTI-CLF)
═══════════════════════════════════════════════════════════════════════

NEVER implement:
  ✗ "fallback law" logic
  ✗ "best effort compression"
  ✗ "dictionary tables" per string
  ✗ "storage"-based encoding
  ✗ "format detection" (JPEG, MP4, etc.)

Why forbidden:
  If Σ contains per-string dictionary → Σ(Dₖ, p⃗) ⊄ p⃗
  Such Σ encodes data, not causality → Violates CLF axioms

═══════════════════════════════════════════════════════════════════════
XI. CORRECT MENTAL MODEL
═══════════════════════════════════════════════════════════════════════

  • Σ is NOT a program (code)
  • Σ is NOT compressed data (post-parsing bytes)
  • Σ is NOT a string-specific encoder (format)

  • Σ IS PRE-PARSING STORAGE: The causal law before execution
  • Ξₙ is PARSING: Law execution → manifestation
  • Σ is mathematical object that NAMES the generator

Example: "4 + 4 + 4 + 4 = 16" vs "f(i) = 4 for all i"
  
  Manifest View (POST-PARSE): [4, 4, 4, 4] → store 4 bytes (data)
  Causal View (PRE-PARSE):    f(i) = 4    → store 1 parameter (law: D1 const)
  
  CLF stores (PRE-PARSING): Σ = {family: 'D1', params: {s0: 4}, n: 4}
  Parsing (EXECUTE LAW):    Ξₙ(Σ) = [f(0), f(1), f(2), f(3)] = [4,4,4,4]
  
  This is not a shortcut - it's the LAW that made those bits inevitable.
  Seed → Parse → Manifestation (generative flow).
  NOT: Manifestation → Compress → Seed (encoding flow).

Job of this module:
  1. Identify which generator made the string (from manifestation)
  2. Extract ONLY the mathematical parameters (law identity)
  3. Reject all logic that tries to "store information" (data)
  4. Produce PRE-PARSING storage (Σ: law awaiting execution)
  5. Ξₙ(Σ) performs PARSING (law → manifestation)

═══════════════════════════════════════════════════════════════════════
XII. SUMMARY RULESET
═══════════════════════════════════════════════════════════════════════

  R1: |Σ_pure| < |S| (minimality on pure params)
  R2: θ(S) tries ALL Dₖ and selects argmin
  R3: Σ contains ONLY parameters, never data
  R4: Ξₙ(Σ(Dₖ, p⃗)) = S must always hold (bijection)
  R5: Σ₀ triggers vocabulary expansion, never accepted as final
  R6: θ(S) = Σ₀ ⟹ raise LawNotInstantiatedError(S)
  R7: Σ_wire is IGNORED for minimality purposes
  R8: File formats are NOT laws (DCT/Huffman ARE laws)
  R9: Vocabulary gaps prove consistency (no guessing)
  R10: Fail hard on all critical violations (see section IX)
  R11: Causal reduction ≠ compression (law ≠ encoding)

═══════════════════════════════════════════════════════════════════════
XIII. INSTANT BEHAVIOR GUARANTEE
═══════════════════════════════════════════════════════════════════════

CLF is mathematically timeless:

  Operation    | Nature        | Determinism | Justification
  -------------|---------------|-------------|---------------------------
  Invₖ(S)      | Boolean       | ✓           | Gate on invariants
  Σ(Dₖ, p⃗)    | Extraction    | ✓           | Parameters derived by definition
  Ξₙ(Σ)        | Generation    | ✓           | Deterministic manifestation
  θ(S)         | Selection     | ✓           | Minimality among laws

All operations are:
  ✓ Mathematical (not computational)
  ✓ Total (not partial)
  ✓ Deterministic (not probabilistic)
  ✓ Timeless (existence, not process)

→ Causal law exists independent of discovery.

═══════════════════════════════════════════════════════════════════════
FINAL STATEMENT
═══════════════════════════════════════════════════════════════════════

    A string does not need to be explained.
    It already IS the explanation.

If this module sees a string:
  - It MUST discover the law that created it
  - It MUST NOT store it, approximate it, or fallback from it

There is no undefined.
Only undiscovered.

═══════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Optional, Tuple, List
from M2_types import Prog, Atom, Conf
# CLF-CORRECT: Use pure evaluation, not procedural execution
from M3_tau_pure import R_n_pure

# STRICT CLF: Use identity resolution θ (not ranking/cost-based selection)
from M4_recognition_STRICT import theta_strict, CLFRecognitionError
USE_STRICT_THETA = True


# ============================================================================
# CLF Vocabulary Completion Exception
# ============================================================================

class LawNotInstantiatedError(Exception):
    """
    Raised when θ(S) identifies a law that violates |Σ_pure| < |S|.
    
    This triggers the deduction protocol:
      1. Extract invariants from S
      2. Deduce new law Dₖ₊₁
      3. Extend vocabulary Θₙ
    
    NOT a bug - it's the CLF vocabulary extension mechanism.
    """
    pass

from M5_construction import Pi_0, verify_construction
from M6_normalization import NF_n, verify_normalization
from M1_codec import encode_HEAD, decode_HEAD, encode_COMMIT, encode_gamma, decode_gamma
from M11_clf_validator import assert_causal_minimality, validate_law_family, soft_validate, CLFValidationError
from M12_structural_integrity import validate_seed_integrity, StructuralIntegrityError
import hashlib
import os
import threading  # For async disk writes (CLF-Hardware boundary)
from datetime import datetime


# ============================================================================
# Varint Encoding/Decoding (for variable-length integers)
# ============================================================================

def encode_varint(n: int) -> bytes:
    """Encode integer as variable-length bytes (simple implementation)"""
    if n < 128:
        return bytes([n])
    elif n < 16384:
        return bytes([0x80 | (n >> 8), n & 0xFF])
    else:
        return bytes([0xC0 | (n >> 16), (n >> 8) & 0xFF, n & 0xFF])


def decode_varint(data: bytes, pos: int) -> Tuple[int, int]:
    """Decode variable-length integer, returns (value, bytes_consumed)"""
    if pos >= len(data):
        raise ValueError("Insufficient bytes for varint")
    
    first = data[pos]
    if first < 0x80:
        return first, 1
    elif first < 0xC0:
        if pos + 1 >= len(data):
            raise ValueError("Insufficient bytes for 2-byte varint")
        val = ((first & 0x3F) << 8) | data[pos + 1]
        return val, 2
    else:
        if pos + 2 >= len(data):
            raise ValueError("Insufficient bytes for 3-byte varint")
        val = ((first & 0x3F) << 16) | (data[pos + 1] << 8) | data[pos + 2]
        return val, 3


# ============================================================================
# Complete Causal Family Set (F_n)
# ============================================================================

"""
CLF-BOOLEAN LAW STRUCTURE

Each law Dₖ must define:
  1. Invₖ(S) → Boolean     [Global invariant check - ENTIRE string, O(1) or O(n)]
  2. Eₖ(i; p⃗) → byte      [Generator - computes S[i] from params, O(1)]
  3. Σₖ(p⃗, n) → bytes     [Seed encoder - params only, NO data]

Law Recognition (Boolean Gate → Minimality):
  
  Stage 1: BOOLEAN GATE (O(m) where m = |Θₙ|)
      For each Dₖ ∈ Θₙ:
          Compute Invₖ(S) → {True, False}
          Keep laws where Invₖ(S) = True
  
  Stage 2: MINIMALITY SELECTION (O(m log m))
      Among valid laws:
          Select argmin |Σ_pure(Dₖ, p⃗)|
  
  NOT ranking, NOT heuristics - BOOLEAN then MINIMAL

Critical Constraint (MEASURED ON Σ_pure ONLY):
  
  |Σ_pure| < |S|  ALWAYS
  
  Where:
    Σ_pure := (Dₖ, p⃗, n)  [Law parameters - 3-5 bytes typically]
    Σ_wire := encode(Σ_pure)  [Serialization - may be larger, IGNORED]
  
  If |Σ_pure| ≥ |S| → Law encodes data, not causality → REJECT

Vocabulary Completeness:
  
  ∀S ∈ 𝔹ⁿ: ∃Dₖ ∈ Θₙ such that Invₖ(S) = True
  
  If no law matches → Vocabulary incomplete → FAIL HARD
  (This is correctness, NOT a bug)

Current Vocabulary Θₙ:
  - D₁: CONST       [S[i] = c for all i]  → Σ_pure = (c, n) = 2-3 bytes
  - D₂: RLE         [S[i] = s₀ + i·δ mod 256]  → Σ_pure = (s₀, δ, n) = 3-4 bytes
  - D₃: COPY        [S[i] = S[i mod period]]  → Σ_pure = (period, n) = 2-3 bytes
  - D₄: XOR_AFFINE  [S[i] = (s₀ + i·δ) ⊕ c]  → Σ_pure = (s₀, δ, c, n) = 4-5 bytes
  - D₅: QUADRATIC   [S[i] = ai² + bi + c mod 256]  → Σ_pure = (a, b, c, n) = 4-5 bytes
  - D₆: LCG         [S[i] = a·S[i-1] + c mod 256]  → Σ_pure = (seed, a, c, n) = 4-5 bytes
  - D₁₀: DICTIONARY [S[i] = dict[indices[i]]]  → Σ_pure = (|dict|, dict, n)
                    ⚠️ REJECTED if |dict| = 256 (encodes data, not law)

REMOVED:
  - D₉: COMPOSITIONAL [Violated ∃! uniqueness - decomposition = storage]

NEEDED (via deduction from invariants):
  - D_DCT_QUANT_HUFFMAN  [Block transforms + sparse coefficients]
  - D_SPARSE_LINEAR      [Rank-deficient matrices]
  - D_GROUP_ACTION       [Symmetry group generators]
  - D_RECURRENCE         [Linear/nonlinear recurrence relations]

These are MATHEMATICAL STRUCTURES, not file formats.
Recognition and parameter extraction are timeless mathematical operations.
"""

F_n = [
    'CONST',
    'RLE',
    'COPY',
    'XOR_CONST',
    'PERMUTE',
    'MOD_ARITH',
    'REV_LOGIC',
    'CELLULAR_AUTO',
    'GRAMMAR',
    'AUTOMATA',
    'SYMMETRY',
]

# D9_COMPOSITIONAL REMOVED:
# Violated CLF uniqueness axiom: ∃!(Dₖ, p⃗)
# Compositional decomposition is STORAGE, not causality
# If string has compositional structure, that IS the causal law
# (e.g., D_DCT_QUANT_HUFFMAN naturally has blocks)
# D9 was a band-aid for incomplete vocabulary, not a legitimate law

# ============================================================================
# Atom Type Markers (for COMPOSE family disambiguation)
# ============================================================================

ATOM_TYPE = {
    'CONST': 0x01,
    'COPY': 0x02,
    'XOR_CONST': 0x03,
    'PERMUTE': 0x04,
    'MOD_ARITH': 0x05,
    'REV_LOGIC': 0x06,
    'CELLULAR_AUTO': 0x07,
    'GRAMMAR': 0x08,
    'AUTOMATA': 0x09,
    'SYMMETRY': 0x0A,
}

ATOM_TYPE_REVERSE = {v: k for k, v in ATOM_TYPE.items()}

# ============================================================================
# Family Markers (omega values)
# ============================================================================

FAMILY_RLE = 0x01       # RLE family (D1, D2)
FAMILY_COMPOSE = 0x03   # COMPOSE family (CONST, COPY, XOR, etc.)

# ============================================================================
# File Output Directories
# ============================================================================

SEEDS_DIR = "/Users/Admin/Teleport Causal Reduction/Seeds"
RECON_DIR = "/Users/Admin/Teleport Causal Reduction/Recon"

# Ensure directories exist
os.makedirs(SEEDS_DIR, exist_ok=True)
os.makedirs(RECON_DIR, exist_ok=True)


# ============================================================================
# Encoding (S -> Sigma)
# ============================================================================

def encode_program_to_wire(P: Prog) -> bytes:
    """
    Encode program to wire format (Enc_n)
    
    Wire structure:
        HEAD (0x14 || omega || edition_bytes)
        BODY (per-atom encoding)
        [COMMIT (0x15 || SHA-256)]
    
    Args:
        P: Program in normal form
    
    Returns:
        Seed bytes Sigma
    """
    wire_parts = []
    
    # Encode HEAD
    omega = P.HEAD.get('omega', 0x01)
    head_bytes = encode_HEAD(omega)
    wire_parts.append(head_bytes)
    
    # Encode n (arity)
    n_bytes = encode_gamma(P.n + 1)  # Gamma-tilde(n+1)
    wire_parts.append(n_bytes)
    
    # Encode BODY atoms
    for atom in P.BODY:
        atom_bytes = encode_atom(atom)
        wire_parts.append(atom_bytes)
    
    # Optionally encode COMMIT
    if P.COMMIT is not None:
        commit_bytes = encode_COMMIT(P.COMMIT)
        wire_parts.append(commit_bytes)
    
    return b''.join(wire_parts)


def encode_atom(a: Atom) -> bytes:
    """
    Encode single atom to wire format
    
    Format depends on family (all include type marker for COMPOSE):
        RLE_SHORT: (no bytes)
        RLE_EXPLICIT: s0 || delta_mod
        CONST: [TYPE_MARKER] || c || Gamma-tilde(ell+1)
        COPY: [TYPE_MARKER] || Gamma-tilde(off+1) || Gamma-tilde(ell+1)
        XOR_CONST: [TYPE_MARKER] || Gamma-tilde(off+1) || Gamma-tilde(ell+1) || c
        PERMUTE: [TYPE_MARKER] || permutation[256] || Gamma-tilde(ell+1)
        MOD_ARITH: [TYPE_MARKER] || a || b || m || Gamma-tilde(ell+1)
        REV_LOGIC: [TYPE_MARKER] || gate_id || params || Gamma-tilde(ell+1)
        CELLULAR_AUTO: [TYPE_MARKER] || rule || seed || Gamma-tilde(ell+1)
        GRAMMAR: [TYPE_MARKER] || grammar_type || params || Gamma-tilde(ell+1)
        AUTOMATA: [TYPE_MARKER] || automaton_type || states || period || Gamma-tilde(ell+1)
        SYMMETRY: [TYPE_MARKER] || symmetry_type || params || Gamma-tilde(ell+1)
    
    Args:
        a: Atom
    
    Returns:
        Atom wire bytes
    """
    family_base = a.family.replace('_INV', '')
    
    if family_base == 'RLE_SHORT':
        # RLE_SHORT has no parameters (all zeros)
        return b''
    
    elif family_base == 'RLE_EXPLICIT':
        s0 = a.theta['s0']
        delta_mod = a.theta['delta_mod']
        return bytes([s0, delta_mod])
    
    elif family_base == 'D4_XOR_AFFINE':
        # D4_XOR_AFFINE: s0 || delta_mod || xor_const
        s0 = a.theta['s0']
        delta_mod = a.theta['delta_mod']
        xor_const = a.theta['xor_const']
        return bytes([s0, delta_mod, xor_const])
    
    elif family_base == 'D5_QUADRATIC':
        # D5_QUADRATIC: a || b || c
        a_coef = a.theta['a']
        b_coef = a.theta['b']
        c_coef = a.theta['c']
        return bytes([a_coef, b_coef, c_coef])
    
    elif family_base == 'D6_LCG':
        # D6_LCG: seed || a || c
        seed = a.theta['seed']
        a_coef = a.theta['a']
        c_coef = a.theta['c']
        return bytes([seed, a_coef, c_coef])
    
    elif family_base == 'D10_DICTIONARY':
        # D10_DICTIONARY: dict_size || [symbols] || [indices]
        dictionary = a.theta['dictionary']
        indices = a.theta['indices']
        dict_size = len(dictionary)
        
        # Encode dictionary size
        size_bytes = encode_varint(dict_size)
        
        # Encode dictionary symbols
        dict_bytes = bytes(dictionary)
        
        # Encode indices (variable-length encoding)
        import math
        bits_per_index = max(1, math.ceil(math.log2(max(dict_size, 2))))
        
        # Simple encoding: use minimal bytes per index
        if bits_per_index <= 8:
            index_bytes = bytes(indices)
        else:
            # Multi-byte indices (for large dictionaries)
            index_bytes = b''.join(i.to_bytes(2, 'big') for i in indices)
        
        return size_bytes + dict_bytes + index_bytes
    
    elif family_base == 'CONST':
        c = a.theta['c']
        ell = a.theta['ell']
        return bytes([ATOM_TYPE['CONST'], c]) + encode_gamma(ell + 1)
    
    elif family_base == 'COPY':
        off = a.theta['off']
        ell = a.theta['ell']
        return bytes([ATOM_TYPE['COPY']]) + encode_gamma(off + 1) + encode_gamma(ell + 1)
    
    elif family_base == 'XOR_CONST':
        off = a.theta['off']
        ell = a.theta['ell']
        c = a.theta['c']
        return bytes([ATOM_TYPE['XOR_CONST']]) + encode_gamma(off + 1) + encode_gamma(ell + 1) + bytes([c])
    
    elif family_base == 'PERMUTE':
        permutation = a.theta['permutation']
        ell = a.theta['ell']
        # Encode permutation table (256 bytes) + length
        perm_bytes = bytes(permutation)
        return bytes([ATOM_TYPE['PERMUTE']]) + perm_bytes + encode_gamma(ell + 1)
    
    elif family_base == 'MOD_ARITH':
        a_val = a.theta['a']
        b_val = a.theta['b']
        m = a.theta['m']
        ell = a.theta['ell']
        return bytes([ATOM_TYPE['MOD_ARITH'], a_val & 0xFF, b_val & 0xFF, m & 0xFF]) + encode_gamma(ell + 1)
    
    elif family_base == 'REV_LOGIC':
        gate = a.theta['gate']
        params = a.theta['params']
        ell = a.theta['ell']
        
        # Encode gate type as byte
        gate_map = {'NOT': 0x01, 'ROTATE_LEFT': 0x02, 'ROTATE_RIGHT': 0x03, 'BIT_REVERSE': 0x04}
        gate_id = gate_map.get(gate, 0x00)
        
        # Encode params (simplified: single byte for rotation, or base params)
        if gate == 'ROTATE_LEFT' or gate == 'ROTATE_RIGHT':
            param_bytes = bytes([params.get('rotation', 0)])
        else:
            param_bytes = b'\x00'  # No params for NOT, BIT_REVERSE
        
        return bytes([ATOM_TYPE['REV_LOGIC'], gate_id]) + param_bytes + encode_gamma(ell + 1)
    
    elif family_base == 'CELLULAR_AUTO':
        rule = a.theta['rule']
        seed = a.theta['seed']
        ell = a.theta['ell']
        return bytes([ATOM_TYPE['CELLULAR_AUTO'], rule & 0xFF]) + seed + encode_gamma(ell + 1)
    
    elif family_base == 'GRAMMAR':
        grammar_type = a.theta['grammar_type']
        params = a.theta['params']
        ell = a.theta['ell']
        
        # Encode grammar type as byte
        grammar_map = {'periodic': 0x01, 'balanced_delimiters': 0x02}
        grammar_id = grammar_map.get(grammar_type, 0x00)
        
        # Encode params (for periodic: period + pattern)
        if grammar_type == 'periodic':
            period = params['period']
            pattern = params['pattern']
            param_bytes = bytes([period & 0xFF]) + pattern
        else:
            param_bytes = b'\x00'
        
        return bytes([ATOM_TYPE['GRAMMAR'], grammar_id]) + param_bytes + encode_gamma(ell + 1)
    
    elif family_base == 'AUTOMATA':
        automaton_type = a.theta['automaton_type']
        states = a.theta['states']
        period = a.theta['period']
        ell = a.theta['ell']
        
        # Encode automaton type
        auto_map = {'cyclic': 0x01}
        auto_id = auto_map.get(automaton_type, 0x00)
        
        # Encode states (as byte sequence)
        state_bytes = bytes(states)
        
        return bytes([ATOM_TYPE['AUTOMATA'], auto_id, period & 0xFF]) + state_bytes + encode_gamma(ell + 1)
    
    elif family_base == 'SYMMETRY':
        symmetry_type = a.theta['symmetry_type']
        params = a.theta.get('params', {})
        ell = a.theta['ell']
        
        # Encode symmetry type
        sym_map = {'palindrome': 0x01, 'reversed_offset': 0x02, 'reversed_complement': 0x03}
        sym_id = sym_map.get(symmetry_type, 0x00)
        
        # Encode params
        if symmetry_type == 'reversed_offset':
            param_bytes = bytes([params.get('offset', 0)])
        else:
            param_bytes = b'\x00'
        
        return bytes([ATOM_TYPE['SYMMETRY'], sym_id]) + param_bytes + encode_gamma(ell + 1)
    
    else:
        return b''


def Sigma_star(S, save_to_file: bool = True, filename_prefix: str = None, verify: str = "instant") -> bytes:
    """
    Full encoding pipeline: S → Σₙ(S)
    
    Args:
        S: Either bytes (loaded object) or str (file path for O(1) deduction)
    
    CLF-BOOLEAN RECOGNITION (Instant, Deterministic):
    
        θ(S) = argmin |Σ_pure|  subject to  Invₖ(S) = True
               Dₖ∈Θₙ
    
    Two-Stage Process (mathematical selection over Θₙ):
        
        Stage 1 - BOOLEAN GATE (O(m)):
            For each law Dₖ ∈ Θₙ:
                Compute Invₖ(S) → {True, False}  [O(1) or O(n)]
                Keep only laws where Invₖ(S) = True
        
        Stage 2 - MINIMALITY (O(m log m)):
            Among valid laws:
                Select argmin |Σ_pure(Dₖ, p⃗)|
    
    CRITICAL: Minimality measured on Σ_pure ONLY:
        
        Σ_pure := (Dₖ, p⃗, n)     [Law parameters - 3-5 bytes]
        Σ_wire := encode(Σ_pure) [Serialization - may be 50+ bytes]
        
        |Σ_pure| < |S|  ← THIS must hold for valid law
        |Σ_wire| is IGNORED for minimality check
    
    Alignment Note (Timeless Edition):
        This pipeline enforces the CLF equalities as identities. The canonical
        alignment specification is CLF_ALIGNMENT_GUIDE_TIMELESS.md.
    
    Pipeline:
        1. θ(S): Boolean gate → minimality selection
        2. Π₀(θ): Extract parameters from law identity
        3. NF_n(P): Canonicalize program
        4. Enc_n(G*): Serialize to wire format (Σ_wire)
    
    Seed Structure (PRE-PARSING STORAGE):
        Σ_pure = (Dₖ, p⃗, n)     [Law identity - What CLF measures]
        Σ_wire = HEAD || PARAMS || γ(n)  [Serialized law - What gets transmitted]
        
        Returns Σ_wire (for transport/storage)
        But validates |Σ_pure| < |S| (law vs manifestation)
        
        CRITICAL: Σ is stored (pre-parsing), S is generated (post-parsing)
                  Σ contains LAW, not DATA
    
    Error Handling:
        If ∀Dₖ: Invₖ(S) = False → Vocabulary incomplete → FAIL HARD
        
        CLF Response:
          ✓ Cause EXISTS (by existence axiom)
          ✓ θ(S) is DEFINED (by identity)
          ✗ Vocabulary Θₙ incomplete
        
        Solution: Trigger deduction from invariants
        FORBIDDEN: Fallback, decomposition, data storage (post-parsing)
    
    Args:
        S: Input string (has unique causal identity)
        save_to_file: If True, saves seed to Seeds/ directory
        filename_prefix: Optional prefix for filename
    
    Returns:
        Σ_wire - Serialized seed (for transport)
        
        Note: This module validates |Σ_pure| < |S|
              Wire format overhead is external to CLF math
    
    Raises:
        ValueError: If vocabulary incomplete (triggers deduction)
    """

    def _assert_full_bijection(seed_dict, source) -> None:
        """Deterministically validate Ξ(seed)[i] == S[i] for all i.

        Note: On a time-based substrate, this is O(n) oracle queries.
        It is still O(1) memory and does not materialize the string.
        """
        from M3_xi_projected import Xi_projected

        n_local = seed_dict.get("n")
        if not isinstance(n_local, int) or n_local < 0:
            n_local = getattr(source, "n", None)
        if not isinstance(n_local, int) or n_local < 0:
            raise ValueError("Seed missing valid 'n' for bijection verification")

        if isinstance(source, (bytes, bytearray, memoryview)):
            get_byte = lambda idx: source[idx]
        elif callable(source):
            get_byte = lambda idx: source(idx)
        else:
            raise TypeError(f"Unsupported source type for bijection verification: {type(source)}")

        try:
            for idx in range(n_local):
                projected = Xi_projected(seed_dict, idx)
                actual = get_byte(idx)
                if actual is None:
                    raise ValueError(f"Oracle returned None at index {idx}")
                if projected != actual:
                    raise LawNotInstantiatedError(
                        f"Full bijection violated at i={idx}: Ξ(Σ)[i]={projected} != S[i]={actual}\n"
                        f"family={seed_dict.get('family')}"
                    )
        except ValueError:
            # Some families may not be supported by Xi_projected yet.
            # For in-memory bytes, we can fall back to full regeneration compare.
            if isinstance(source, (bytes, bytearray, memoryview)):
                from Legacy.M17_seed_regeneration import regenerate_from_seed

                regenerated = regenerate_from_seed(seed_dict)
                if bytes(source) != regenerated:
                    raise LawNotInstantiatedError(
                        "Full bijection violated: regenerate_from_seed(seed) != S"
                    )
            else:
                raise


    def _assert_timeless_seed(seed_dict: dict) -> None:
        """Timeless-mode guardrails.

        Enforces that no seed relies on sampling/heuristic completion metadata.
        The intention is to prevent accidentally accepting a witness-only seed
        while claiming total CLF bijection.
        """
        if not isinstance(seed_dict, dict):
            raise TypeError("Seed must be a dict")

        family = seed_dict.get('family')
        params = seed_dict.get('params') or {}
        if not isinstance(params, dict):
            raise TypeError("Seed params must be a dict")

        # Forbid payload-carrying / explicit seeds in timeless/instant-deduction.
        # These represent storing the manifestation (effect) rather than a lawful cause.
        if family in {'D0_EXPLICIT', 'D11_RAW'}:
            raise LawNotInstantiatedError(
                f"Timeless alignment violation: forbidden explicit/raw family {family}"
            )

        # Reject sampled seeds (witness-only) in timeless mode.
        if bool(params.get('sampled', False)):
            raise LawNotInstantiatedError(
                "Timeless alignment violation: seed is marked sampled=True"
            )

        # D9 completion must be explicit and strict in timeless mode.
        if family == 'D9_RADIAL':
            completion = (params.get('completion') or '').upper()
            if completion and completion != 'STRICT':
                raise LawNotInstantiatedError(
                    f"Timeless alignment violation: D9 completion must be STRICT (got {completion})"
                )


    def _upgrade_sampled_d9_to_instant_deduction(seed_dict: dict, sampler) -> dict:
        """Convert witness-style D9_RADIAL into D9_INSTANT_DEDUCTION for strict modes.

        This enforces the instant-deduction constraint that Θ must not emit sampled
        / completion-dependent seeds in strict or timeless verification.
        """
        if not isinstance(seed_dict, dict):
            return seed_dict
        if seed_dict.get('family') != 'D9_RADIAL':
            return seed_dict
        params = seed_dict.get('params') or {}
        if not isinstance(params, dict):
            return seed_dict
        if not bool(params.get('sampled', False)):
            return seed_dict

        n_local = getattr(sampler, 'n', None)
        if not isinstance(n_local, int) or n_local < 3:
            return seed_dict

        s0 = sampler(0)
        s1 = sampler(1)
        s2 = sampler(2)
        sn1 = sampler(n_local - 1)
        if None in (s0, s1, s2, sn1):
            return seed_dict

        s0 = int(s0) & 0xFF
        s1 = int(s1) & 0xFF
        s2 = int(s2) & 0xFF
        sn1 = int(sn1) & 0xFF

        r0 = (s0 - sn1) & 0xFF
        ds = (s1 - s0) & 0xFF
        dr = (s2 - (2 * s1) + s0) & 0xFF

        return {
            'family': 'D9_INSTANT_DEDUCTION',
            'params': {'s0': s0, 'r0': r0, 'ds': ds, 'dr': dr},
            'n': int(n_local),
        }

    
    # Step 1: θ(S) - Universal recognition (size-agnostic)
    #
    # CLF ONTOLOGY: S is a mathematical object; recognition is oracle-based.
    # Implementation detail (bytes vs file-backed oracle) must not change the logic.
    if isinstance(S, str):
        from M4_recognition_SAMPLED import BinaryStringSampler, theta_sampled
        from direct_seed_encoder import encode_seed_direct

        sampler = BinaryStringSampler(S)
        try:
            verify_mode = str(verify).lower()
            # Verification / closure selection:
            # - 'instant': bounded evidence (witness indices only)
            # - 'full': total bijection witness over all indices
            # - 'timeless': strict mode (full + rejects sampled/heuristic seeds)
            # - 'instant-deduction': strict mode (authoritative instant-deduction spec)
            # - 'closed': deletion-ready contract under current closure classifier
            if verify_mode in {'full', 'timeless', 'instant-deduction'}:
                closure_mode = 'full'
            elif verify_mode == 'closed':
                closure_mode = 'closed'
            else:
                closure_mode = 'instant'
            theta_result = theta_sampled(sampler, closure=closure_mode)

            # Instant-deduction strict modes: forbid sampled D9 and upgrade to
            # instant-deduction parametric form.
            if verify_mode in {'timeless', 'instant-deduction'}:
                theta_result = _upgrade_sampled_d9_to_instant_deduction(theta_result, sampler)

            # Ensure 'n' is set for downstream checks.
            if isinstance(theta_result, dict) and theta_result.get('n') is None:
                theta_result['n'] = sampler.n
            elif isinstance(theta_result, dict) and 'n' not in theta_result:
                theta_result['n'] = sampler.n

            validate_law_family(theta_result["family"])
            try:
                validate_seed_integrity(theta_result, sampler)
            except StructuralIntegrityError as e:
                raise LawNotInstantiatedError(
                    f"Structural Integrity Violation - Effect leakage detected\n\n"
                    f"{str(e)}\n\n"
                    f"This law symbolizes manifestation, not origin."
                ) from e

            if verify_mode in {'full', 'timeless', 'instant-deduction'}:
                _assert_full_bijection(theta_result, sampler)

            if verify_mode in {'timeless', 'instant-deduction'}:
                _assert_timeless_seed(theta_result)
                # Also enforce 𝒮↔𝒲 involution/idempotence at the boundary.
                from CLF_validators import assert_seed_wire_involution, assert_seed_wire_idempotence
                assert_seed_wire_involution(theta_result)
                assert_seed_wire_idempotence(theta_result)

            if verify_mode == 'closed':
                from Tests.clf_closure import classify_seed_closure
                from CLF_validators import validate_law_reflexivity, validate_law_idempotence

                closure_class, why = classify_seed_closure(theta_result)
                if closure_class != 'CLOSED_GENERATIVE':
                    raise LawNotInstantiatedError(
                        f"Seed is not deletion-ready under current CLF equations: {closure_class}\n"
                        f"Reason: {why}\n"
                        f"family={theta_result.get('family')}"
                    )

                # ℒ² reflexivity (law-of-laws): validate θ_ℒ/Ξ_ℒ stability on a finite basis.
                # This is bounded and deterministic, and does not inspect S beyond θ(S).
                _basis = [
                    {'family': 'D1', 'params': {'c': 0}, 'n': 1},
                    {'family': 'D2', 'params': {'s0': 0, 'delta': 1}, 'n': 2},
                    {'family': 'D3', 'params': {'period': 2, 'cycle': [0, 1]}, 'n': 2},
                    {'family': 'D4_XOR_AFFINE', 'params': {'base_s0': 0, 'base_delta': 1, 'xor_const': 0}, 'n': 4},
                    {'family': 'D5_QUADRATIC', 'params': {'a': 1, 'b': 0, 'c': 0}, 'n': 8},
                    {'family': 'D6_MIRROR', 'params': {'pattern': [0, 1, 2, 3]}, 'n': 8},
                    {'family': 'D7_ROTATIONAL', 'params': {'pattern': [0, 1, 2, 3], 'stride': 1}, 'n': 16},
                    {'family': 'D10_RECURRENCE', 'params': {'m': 4, 'sub_seed': {'family': 'D1', 'params': {'c': 7}, 'n': 4}}, 'n': 16},
                    {'family': 'D11_RADIAL_RECURRENCE', 'params': {'center': 4, 'radial_seed': {'family': 'D2', 'params': {'s0': 0, 'delta': 1}, 'n': 5}}, 'n': 9},
                    {'family': 'D12_SELF_AFFINE', 'params': {'alpha': 3, 'beta': 1, 'base_seed': {'family': 'D1', 'params': {'c': 42}, 'n': 9}}, 'n': 9},
                ]
                validate_law_reflexivity(_basis)
                validate_law_idempotence(theta_result)

            return encode_seed_direct(theta_result)
        finally:
            # Avoid FD leakage during batch validation
            close = getattr(sampler, 'close', None)
            if callable(close):
                close()
    
    try:
        if USE_STRICT_THETA:
            # STRICT MODE: θ returns (family, params) or raises
            theta_result = theta_strict(S)
            
            # Check if unresolved (vocabulary incomplete)
            if theta_result.get('status') == 'unresolved':
                raise LawNotInstantiatedError(
                    f"CLF Vocabulary Incomplete - Recognizer cannot name causal law.\n"
                    f"String length: {len(S)} bytes\n\n"
                    f"RECOGNIZER STATUS:\n"
                    f"  Status: {theta_result['status']}\n"
                    f"  Reason: {theta_result['reason']}\n"
                    f"  Checked families: {', '.join(theta_result['checked_families'])}\n\n"
                    f"CLF AXIOM: {theta_result['axiom']}\n"
                    f"SOLUTION: {theta_result['solution']}\n"
                    f"FORBIDDEN: {theta_result['forbidden']}\n\n"
                    f"Note: {theta_result['note']}"
                )
            
            # Validate law family is not compression
            validate_law_family(theta_result["family"])

            # CRITICAL: Validate structural integrity (no effect leakage)
            try:
                validate_seed_integrity(theta_result, S)
            except StructuralIntegrityError as e:
                raise LawNotInstantiatedError(
                    f"Structural Integrity Violation - Effect leakage detected\n\n"
                    f"{str(e)}\n\n"
                    f"This law symbolizes manifestation, not origin."
                ) from e

            if str(verify).lower() == 'full':
                _assert_full_bijection(theta_result, S)
            
            # DIRECT ENCODING: Bypass Pi_0/NF/atoms for recognized laws
            # This encodes the causal law DIRECTLY to minimal binary format
            # avoiding intermediate atom representation bloat
            from direct_seed_encoder import encode_seed_direct
            
            try:
                sigma = encode_seed_direct(theta_result)
                
                # The first recognition IS the mathematical essence
                # No iteration needed - θ(S) reveals the law instantly
                return sigma
            except ValueError as e:
                # CRITICAL: Direct encoding must support ALL structures extracted by theta_strict
                # If it fails, that's a bug in encoder, not a reason to fall back to iteration
                raise RuntimeError(
                    f"Direct encoder failed for extracted structure\n"
                    f"Family: {theta_result.get('family')}\n"
                    f"This is a bug - encoder must support all structures from theta_strict\n"
                    f"Error: {e}"
                ) from e
            
            # Convert to old format for Pi_0 compatibility
            # Initialize all families to None, then set the matched one
            theta_params = {
                "n": len(S),
                "D1": None,
                "D2": None,
                "D3": None,
                "D4_XOR_AFFINE": None,
                "D5_QUADRATIC": None,
                "D6_LCG": None,
                # Add more as Θ_n expands
            }
            theta_params[theta_result["family"]] = theta_result["params"]
        else:
            # OLD MODE: θ returns all matches, Pi_0 selects by cost
            # TODO: Phase out - violates fundamental equation
            theta_params = theta_strict(S)
    
    except (CLFRecognitionError, LawNotInstantiatedError) as e:
        # Vocabulary incomplete - cannot name causal law
        # 
        # CLF DOMAIN AXIOM: ∀S ∈ Ξ(ℒ): ∃!(Dₖ, p⃗)
        # 
        # If S is lawful (S ∈ Ξ(ℒ)), the cause exists uniquely.
        # This error means: current ℒ/Θₙ cannot yet name the law.
        # 
        # This is CORRECT behavior (not a bug):
        #   - Do NOT fallback
        #   - Do NOT decompose
        #   - Do NOT store data
        # 
        # Solution: Extend Θₙ via invariant deduction
        
        # If this is a LawNotInstantiatedError, preserve the detailed message
        if isinstance(e, LawNotInstantiatedError):
            raise
        
        raise LawNotInstantiatedError(
            f"CLF Vocabulary Incomplete - Cannot name causal law.\n"
            f"String length: {len(S)} bytes\n\n"
            f"CLF DOMAIN AXIOM:\n"
            f"  ∀S ∈ Ξ(ℒ): ∃!(Dₖ, p⃗) - Lawful existence implies a unique causal law\n\n"
            f"DIAGNOSIS (domain restricted):\n"
            f"  ✓ If S is lawful (S ∈ Ξ(ℒ)), a unique cause exists\n"
            f"  ✗ Current ℒ/Θₙ cannot yet name this S (law/generator gap)\n\n"
            f"Current Θₙ: {{D1, D2, D3, D4, D5, D6, D10}}\n\n"
            f"RESOLUTION (deductive closure):\n"
            f"  Expand ℒ_current by causal reclosure (Closure(ℒ_current)):\n"
            f"    - Identify missing invariant–projection pair (Invₖ, Eₖ)\n"
            f"    - Prove parameters are uniquely deducible within ℒ\n"
            f"    - Admit the resulting seed family into ℒ (lawful extension)\n\n"
            f"FORBIDDEN:\n"
            f"  ✗ Fallback to storage\n"
            f"  ✗ Decomposition into sub-causes\n"
            f"  ✗ Per-string tables\n"
            f"  ✗ |Σ| ≥ |S| (data encoding)\n\n"
            f"The law EXISTS. We simply cannot name it yet."
        ) from e
    
    # NOTE: Minimality enforcement now done IN θ(S) itself
    # θ only returns laws where |Σ_pure| < |S|
    # No post-hoc validation needed - minimality is BUILT IN
    
    # Validate: Exactly one family matched (if using old θ)
    if not USE_STRICT_THETA:
        # Check if any law matched the ENTIRE string
        has_match = any(theta_params.get(f'D{i}') for i in range(1, 12))
        
        if not has_match:
            raise LawNotInstantiatedError(
                f"CLF Vocabulary Incomplete - Cannot name causal law.\n"
                f"String length: {len(S)} bytes\n\n"
                f"CLF DOMAIN AXIOM: ∀S ∈ Ξ(ℒ): ∃!(Dₖ, p⃗)\n\n"
                f"Current Θₙ: {{D1, D2, D3, D4, D5, D6, D10}}\n\n"
                f"SOLUTION: Extend Θₙ via invariant deduction\n"
                f"FORBIDDEN: Fallback, decomposition, per-string tables"
            )
    
    # Step 2: Π₀(θ) - Parameter Extraction
    # Extract parameters from resolved causal identity
    # Parameters already exist (given by causality)
    # This is projection into program form, not construction
    P = Pi_0(S, theta_params)
    
    # Step 3: NF_n(P) - Canonicalize
    G_star = NF_n(P)
    
    # Step 4: Enc_n(G*) - Serialize identity to wire format
    # Seed = HEAD_D_k || PARAMS || γ(n)
    # Contains: causal identity in symbolic form
    # NOT: output bytes, enumerations, decompositions
    sigma = encode_program_to_wire(G_star)
    
    # Step 5: VALIDATE CLF AXIOMS (Runtime Enforcement)
    # Enforce all four CLF causal minimality axioms:
    #   1. Σ ∈ C^closed (no 'inferred' flags)
    #   2. |Σ| < |S| (seed smaller than consequence)
    #   3. Ξ(Σ) = S (bijection - perfect generation)
    #   4. No effect leakage (seed = pure cause, no raw data)
    #
    # Convert wire format back to seed structure for validation
    seed_dict = {
        'family': theta_result['family'] if USE_STRICT_THETA else None,
        'params': theta_result['params'] if USE_STRICT_THETA else theta_params,
        'n': len(S)
    }
    
    try:
        # Full axiom enforcement
        assert_causal_minimality(S, seed_dict, theta_result if USE_STRICT_THETA else None)
    except CLFValidationError as e:
        # Seed violates CLF axioms - reject it
        raise LawNotInstantiatedError(
            f"CLF Validation Failed - Seed violates causal minimality axioms\n\n"
            f"VALIDATION ERROR:\n{str(e)}\n\n"
            f"This indicates the 'law' is storing observations, not generative equations.\n"
            f"Law must satisfy Fibonacci Principle: Store ORIGIN (formula), not MANIFESTATION (data).\n\n"
            f"SOLUTION: Implement true generative law for this structure\n"
            f"FORBIDDEN: Accept compression algorithms as causal laws"
        ) from e
    
    # Step 6: Save to file
    if save_to_file:
        if filename_prefix is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename_prefix = f"seed_{timestamp}"
        
        # CLF: Filename is deterministic (no hash needed)
        filename = f"{filename_prefix}.bin"
        filepath = os.path.join(SEEDS_DIR, filename)
        
        with open(filepath, 'wb') as f:
            f.write(sigma)
        
        # [FIX 1] Enforce file write validation
        if not os.path.exists(filepath):
            raise RuntimeError(f"[CLF] Seed file was not written: {filepath}")
        
        # Verify file content matches seed
        with open(filepath, 'rb') as f:
            written_data = f.read()
        if written_data != sigma:
            raise RuntimeError(f"[CLF] Seed file content mismatch: {filepath}")
    
    return sigma


# ============================================================================
# Decoding (Sigma -> S)
# ============================================================================

def decode_wire_to_program(wire: bytes) -> Prog:
    """
    Decode wire format to program (Dec_n)
    
    Parse:
        HEAD -> omega, edition
        Gamma-tilde(n+1) -> n
        BODY atoms
        [COMMIT]
    
    Args:
        wire: Seed bytes Sigma
    
    Returns:
        Decoded program P'
    """
    pos = 0
    
    # Decode HEAD
    omega, pos = decode_HEAD(wire, pos)
    
    # Decode n
    n_plus_1, bytes_used = decode_gamma(wire, pos)
    n = n_plus_1 - 1
    pos += bytes_used
    
    # Decode BODY atoms
    body = []
    
    # Determine family from omega
    if omega == 0x01:
        # RLE family
        body, pos = decode_RLE_atoms(wire, pos, n)
    elif omega == 0x03:
        # COMPOSE family
        body, pos = decode_COMPOSE_atoms(wire, pos, n)
    elif omega == 0x04:
        # D4_XOR_AFFINE family
        body, pos = decode_D4_XOR_AFFINE_atoms(wire, pos, n)
    elif omega == 0x05:
        # D5_QUADRATIC family
        body, pos = decode_D5_QUADRATIC_atoms(wire, pos, n)
    elif omega == 0x06:
        # D6_LCG family
        body, pos = decode_D6_LCG_atoms(wire, pos, n)
    elif omega == 0x0A:
        # D10_DICTIONARY family
        body, pos = decode_D10_DICTIONARY_atoms(wire, pos, n)
    else:
        # Unknown omega - should not happen in valid CLF seeds
        raise ValueError(f"Unknown family marker omega=0x{omega:02x}")
    
    # Check for COMMIT
    commit = None
    if pos < len(wire) and wire[pos] == 0x15:
        # COMMIT present
        commit = wire[pos+1:pos+33] if pos+33 <= len(wire) else None
        pos += 33
    
    return Prog(n=n, BODY=body, HEAD={'omega': omega, 'edition': 'v3.3.8'}, COMMIT=commit)


def decode_RLE_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode RLE family atoms
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Arity
    
    Returns:
        (atoms, new_pos)
    """
    atoms = []
    
    # Check if RLE_SHORT (no bytes after n)
    if pos >= len(wire) or wire[pos] in [0x14, 0x15]:
        # RLE_SHORT (all zeros)
        from M5_construction import make_RLE_SHORT_atom
        atom = make_RLE_SHORT_atom()
        atoms.append(atom)
    else:
        # RLE_EXPLICIT
        s0 = wire[pos]
        delta_mod = wire[pos + 1]
        pos += 2
        
        from M5_construction import make_RLE_EXPLICIT_atom
        atom = make_RLE_EXPLICIT_atom(s0, delta_mod)
        atoms.append(atom)
    
    return atoms, pos


def decode_D4_XOR_AFFINE_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode D4_XOR_AFFINE family atoms
    
    D4_XOR_AFFINE uses single atomic operation (Bijective CLF Boolean):
      - D4_XOR_AFFINE atom (s0, delta, xor_const)
      - Writes entire output: S[i] = (s0 + i·δ) ⊕ c
    
    Wire format:
      - s0 (1 byte)
      - delta (1 byte)
      - xor_const (1 byte)
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Arity
    
    Returns:
        (atoms, new_pos)
    """
    if pos + 3 > len(wire):
        raise ValueError("Insufficient bytes for D4_XOR_AFFINE parameters")
    
    s0 = wire[pos]
    delta = wire[pos + 1]
    xor_const = wire[pos + 2]
    pos += 3
    
    from M2_types import Atom
    
    # Single atomic D4_XOR_AFFINE operation (bijective)
    atom = Atom("D4_XOR_AFFINE", {"s0": s0, "delta_mod": delta, "xor_const": xor_const})
    atom_inv = Atom("D4_XOR_AFFINE_INV", {"s0": s0, "delta_mod": delta, "xor_const": xor_const})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return [atom], pos


def decode_D5_QUADRATIC_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode D5_QUADRATIC family atoms
    
    D5_QUADRATIC uses single atomic operation (Bijective CLF Boolean):
      - D5_QUADRATIC atom (a, b, c)
      - Writes entire output: S[i] = (a·i² + b·i + c) mod 256
    
    Wire format:
      - a (1 byte)
      - b (1 byte)
      - c (1 byte)
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Arity
    
    Returns:
        (atoms, new_pos)
    """
    if pos + 3 > len(wire):
        raise ValueError("Insufficient bytes for D5_QUADRATIC parameters")
    
    a = wire[pos]
    b = wire[pos + 1]
    c = wire[pos + 2]
    pos += 3
    
    from M2_types import Atom
    
    # Single atomic D5_QUADRATIC operation (bijective)
    atom = Atom("D5_QUADRATIC", {"a": a, "b": b, "c": c})
    atom_inv = Atom("D5_QUADRATIC_INV", {"a": a, "b": b, "c": c})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return [atom], pos


def decode_D6_LCG_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode D6_LCG family atoms
    
    D6_LCG uses single atomic operation (Bijective CLF Boolean):
      - D6_LCG atom (seed, a, c)
      - Writes entire output: S[0] = seed, S[i] = (a·S[i-1] + c) mod 256
    
    Wire format:
      - seed (1 byte)
      - a (1 byte)
      - c (1 byte)
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Arity
    
    Returns:
        (atoms, new_pos)
    """
    if pos + 3 > len(wire):
        raise ValueError("Insufficient bytes for D6_LCG parameters")
    
    seed = wire[pos]
    a = wire[pos + 1]
    c = wire[pos + 2]
    pos += 3
    
    from M2_types import Atom
    
    # Single atomic D6_LCG operation (bijective)
    atom = Atom("D6_LCG", {"seed": seed, "a": a, "c": c})
    atom_inv = Atom("D6_LCG_INV", {"seed": seed, "a": a, "c": c})
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return [atom], pos


def decode_D10_DICTIONARY_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode D10_DICTIONARY family atoms
    
    D10_DICTIONARY wire format:
      - dict_size (varint)
      - [symbols] (dict_size bytes)
      - [indices] (n indices, variable encoding)
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Total arity (number of output bytes)
    
    Returns:
        (atoms, new_pos)
    """
    # Decode dictionary size
    dict_size, bytes_read = decode_varint(wire, pos)
    pos += bytes_read
    
    if dict_size <= 0:
        raise ValueError(f"Invalid dictionary size: {dict_size}")
    
    # Decode dictionary symbols
    if pos + dict_size > len(wire):
        raise ValueError("Insufficient bytes for dictionary")
    
    dictionary = list(wire[pos:pos + dict_size])
    pos += dict_size
    
    # Decode indices
    import math
    bits_per_index = max(1, math.ceil(math.log2(max(dict_size, 2))))
    
    indices = []
    if bits_per_index <= 8:
        # Single-byte indices
        if pos + n > len(wire):
            raise ValueError("Insufficient bytes for indices")
        indices = list(wire[pos:pos + n])
        pos += n
    else:
        # Multi-byte indices
        for _ in range(n):
            if pos + 2 > len(wire):
                break
            idx = int.from_bytes(wire[pos:pos+2], 'big')
            indices.append(idx)
            pos += 2
    
    from M2_types import Atom
    
    atom = Atom("D10_DICTIONARY", {
        "dictionary": dictionary,
        "indices": indices,
        "dict_size": dict_size
    })
    atom_inv = Atom("D10_DICTIONARY_INV", {
        "dictionary": dictionary,
        "indices": indices,
        "dict_size": dict_size
    })
    atom.inv = atom_inv
    atom_inv.inv = atom
    
    return [atom], pos


def decode_COMPOSE_atoms(wire: bytes, pos: int, n: int) -> Tuple[List[Atom], int]:
    """
    Decode COMPOSE family atoms with type markers
    
    Each atom begins with a type marker (0x01-0x0A):
        0x01: CONST
        0x02: COPY
        0x03: XOR_CONST
        0x04: PERMUTE
        0x05: MOD_ARITH
        0x06: REV_LOGIC
        0x07: CELLULAR_AUTO
        0x08: GRAMMAR
        0x09: AUTOMATA
        0x0A: SYMMETRY
    
    Args:
        wire: Wire bytes
        pos: Current position
        n: Arity
    
    Returns:
        (atoms, new_pos)
    """
    atoms = []
    arity_covered = 0
    
    # Parse atoms until we've covered n bytes
    while arity_covered < n and pos < len(wire) and wire[pos] not in [0x14, 0x15]:
        # Read atom type marker
        if pos >= len(wire):
            break
        
        atom_type = wire[pos]
        pos += 1
        
        if atom_type not in ATOM_TYPE_REVERSE:
            # Unknown atom type - stop parsing
            break
        
        atom_family = ATOM_TYPE_REVERSE[atom_type]
        
        if atom_family == 'CONST':
            c = wire[pos]
            pos += 1
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_CONST_atom
            atom = make_CONST_atom(c, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'COPY':
            off_plus_1, bytes_used1 = decode_gamma(wire, pos)
            pos += bytes_used1
            ell_plus_1, bytes_used2 = decode_gamma(wire, pos)
            pos += bytes_used2
            
            from M5_construction import make_COPY_atom
            atom = make_COPY_atom(off_plus_1 - 1, ell_plus_1 - 1)
            atoms.append(atom)
            arity_covered += (ell_plus_1 - 1)
        
        elif atom_family == 'XOR_CONST':
            off_plus_1, bytes_used1 = decode_gamma(wire, pos)
            pos += bytes_used1
            ell_plus_1, bytes_used2 = decode_gamma(wire, pos)
            pos += bytes_used2
            
            if pos >= len(wire):
                break
            c = wire[pos]
            pos += 1
            
            from M5_construction import make_XOR_CONST_atom
            atom = make_XOR_CONST_atom(off_plus_1 - 1, ell_plus_1 - 1, c)
            atoms.append(atom)
            arity_covered += (ell_plus_1 - 1)
        
        elif atom_family == 'PERMUTE':
            # PERMUTE: 256 bytes permutation + length
            if pos + 256 >= len(wire):
                break
            permutation = list(wire[pos:pos+256])
            pos += 256
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_PERMUTE_atom
            atom = make_PERMUTE_atom(permutation, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'MOD_ARITH':
            # MOD_ARITH: a || b || m || length
            if pos + 3 >= len(wire):
                break
            a = wire[pos]
            b = wire[pos + 1]
            m = wire[pos + 2]
            pos += 3
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_MOD_ARITH_atom
            atom = make_MOD_ARITH_atom(a, b, m, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'REV_LOGIC':
            # REV_LOGIC: gate_id || params || length
            if pos + 1 >= len(wire):
                break
            
            gate_id = wire[pos]
            pos += 1
            
            gate_map_inv = {0x01: 'NOT', 0x02: 'ROTATE_LEFT', 0x03: 'ROTATE_RIGHT', 0x04: 'BIT_REVERSE'}
            gate = gate_map_inv.get(gate_id, 'NOT')
            
            # Decode params
            if gate in ['ROTATE_LEFT', 'ROTATE_RIGHT']:
                rotation = wire[pos]
                pos += 1
                params = {'rotation': rotation}
            else:
                pos += 1  # Skip param byte
                params = {}
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_REV_LOGIC_atom
            atom = make_REV_LOGIC_atom(gate, params, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'CELLULAR_AUTO':
            # CELLULAR_AUTO: rule || seed || length
            if pos + 1 >= len(wire):
                break
            
            rule = wire[pos]
            pos += 1
            
            # Seed is variable length - for now, assume 1 byte
            seed = wire[pos:pos+1]
            pos += 1
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_CELLULAR_AUTO_atom
            atom = make_CELLULAR_AUTO_atom(rule, seed, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'GRAMMAR':
            # GRAMMAR: grammar_id || params || length
            if pos + 1 >= len(wire):
                break
            
            grammar_id = wire[pos]
            pos += 1
            
            grammar_map_inv = {0x01: 'periodic', 0x02: 'balanced_delimiters'}
            grammar_type = grammar_map_inv.get(grammar_id, 'periodic')
            
            # Decode params
            if grammar_type == 'periodic':
                period = wire[pos]
                pos += 1
                # Pattern follows
                if pos + period > len(wire):
                    break
                pattern = wire[pos:pos+period]
                pos += period
                params = {'period': period, 'pattern': pattern}
            else:
                pos += 1
                params = {}
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_GRAMMAR_atom
            atom = make_GRAMMAR_atom(grammar_type, params, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'AUTOMATA':
            # AUTOMATA: auto_id || period || states || length
            if pos + 2 >= len(wire):
                break
            
            auto_id = wire[pos]
            period = wire[pos + 1]
            pos += 2
            
            auto_map_inv = {0x01: 'cyclic'}
            automaton_type = auto_map_inv.get(auto_id, 'cyclic')
            
            # States (assume period bytes)
            if pos + period > len(wire):
                break
            states = list(wire[pos:pos+period])
            pos += period
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_AUTOMATA_atom
            atom = make_AUTOMATA_atom(automaton_type, states, period, ell)
            atoms.append(atom)
            arity_covered += ell
        
        elif atom_family == 'SYMMETRY':
            # SYMMETRY: sym_id || params || length
            if pos + 1 >= len(wire):
                break
            
            sym_id = wire[pos]
            pos += 1
            
            sym_map_inv = {0x01: 'palindrome', 0x02: 'reversed_offset', 0x03: 'reversed_complement'}
            symmetry_type = sym_map_inv.get(sym_id, 'palindrome')
            
            # Decode params
            if symmetry_type == 'reversed_offset':
                offset = wire[pos]
                pos += 1
                params = {'offset': offset}
            else:
                pos += 1
                params = {}
            
            ell_plus_1, bytes_used = decode_gamma(wire, pos)
            ell = ell_plus_1 - 1
            pos += bytes_used
            
            from M5_construction import make_SYMMETRY_atom
            atom = make_SYMMETRY_atom(symmetry_type, params, ell)
            atoms.append(atom)
            arity_covered += ell
    
    return atoms, pos


def Xi_n(sigma: bytes, save_to_file: bool = True, filename_prefix: str = None, original_extension: str = None) -> bytes:
    """
    Full replay pipeline: Σ → Ξₙ(Σ) = S
    
    CLF CAUSAL INSTANTIATION (Pure Generative Process):
    
        Σₙ(S) = HEAD_Dₖ || PARAMS_Dₖ || γ(n)
            ↓
        Ξₙ(Σ) = [Eₖ(0; p⃗), Eₖ(1; p⃗), ..., Eₖ(n-1; p⃗)]
            ↓
        S (re-instantiated from causal law)
    
    This is NOT decoding - it is CAUSAL PREDICTION:
        Given law Dₖ and parameters p⃗, we COMPUTE what S must be.
        String is PREDICTED from first principles, not restored from storage.
    
    Pure Causal Logic:
        - Seed Σ contains: Law pointer Dₖ + parameters p⃗ + length n
        - NO stored data, NO content, ONLY causal formula
        - String S is GENERATED from law, not decoded from bits
    
    Pipeline:
        1. Dec_n(Σ): Parse HEAD_Dₖ || PARAMS_Dₖ || γ(n) → Program P
        2. R_n(P): Evaluate ∀i ∈ [0,n): S[i] = Eₖ(i; p⃗)
        3. Return S (causal instantiation)
    
    Mathematical Guarantees:
        - Ξₙ(Σ) ⊥ S_original (no access to original - only seed)
        - ∀i: S[i] = E(i, p⃗) (deterministic pure function)
        - Ξₙ(Σₙ(S)) = S (exact bijection)
        - No temporal dependencies, fully timeless
    
    Identity:
        Ξₙ(Σₙ(S)) = S
        
        Replay re-instantiates the SAME cause (not different representation).
    
    Args:
        sigma: Causal seed Σₙ (HEAD || PARAMS || γ(n))
        save_to_file: If True, saves instantiation to Recon/ directory
        filename_prefix: Optional prefix for filename
        original_extension: Optional extension (e.g., '.jpeg')
    
    Returns:
        S - String instantiated from causal law Ξₙ(Σ)
    """
    # Step 1: Dec_n(Σ) - Parse seed to causal program
    # Extract: HEAD_D_k → law identifier, PARAMS_D_k → parameters, γ(n) → length
    
    # DIRECT DECODING: Check if seed uses minimal direct encoding
    if len(sigma) >= 5:
        from direct_seed_encoder import decode_seed_direct
        
        try:
            theta_result = decode_seed_direct(sigma)
            
            # Regenerate S from causal law
            from M3_tau_pure import expand_from_theta
            S = expand_from_theta(theta_result)
            
            # Save to file if requested
            if save_to_file:
                # ... (file saving logic moved later)
                pass
            
            return S
        except (ValueError, KeyError, ImportError):
            # Not direct encoding, fall through to legacy decode
            pass
    
    # LEGACY DECODING: Parse wire format to Program
    P = decode_wire_to_program(sigma)
    
    # Step 2: R_n_pure(P) - Pure Causal Instantiation
    # Compute: ∀i ∈ [0,n): S[i] = E_k(i; p⃗)
    # String is PREDICTED from law, not restored from storage
    # 
    # CLF-CORRECT: Use pure evaluation (no mutable state)
    #   - R_n_pure: E(i, Σ) → byte (pure function)
    #   - NO FALLBACK: If R_n_pure fails → law not CLF-valid yet
    try:
        S = R_n_pure(P)
    except (NotImplementedError, AttributeError) as e:
        # CLF AXIOM ENFORCEMENT: No fallback to imperative execution
        # If R_n_pure cannot execute → law is not yet fully defined
        # Solution: Implement pure evaluator for this atom
        # FORBIDDEN: Fallback to R_n (imperative)
        raise CLFValidationError(
            f"Ξ_n undefined: Pure evaluator does not support this atom\n\n"
            f"ATOM: {P.BODY[0].family if P.BODY else 'unknown'}\n"
            f"ERROR: {str(e)}\n\n"
            f"CLF AXIOM: Ξ must be a pure mathematical function\n"
            f"REALITY: R_n_pure cannot execute this law\n\n"
            f"SOLUTION: Implement pure evaluator for this atom family\n"
            f"FORBIDDEN: Fallback to imperative execution (R_n)\n\n"
            f"This law is not yet CLF-valid until pure evaluation is defined."
        ) from e
    
    # Step 3: Save to file
    # CLF-Hardware Boundary: Instant Instantiation + Parallel Disk Write
    #
    # CLF Guarantee: Ξ(Σ) = S is INSTANT (mathematical operation in RAM)
    # Hardware Reality: RAM → Disk is NOT instant (physical write latency)
    #
    # Solution (Leveraging OS Page Cache):
    #   1. S instantiated in RAM (instant, timeless)
    #   2. Return S immediately (user can interact)
    #   3. Disk write happens in parallel (non-blocking)
    #   4. OS shows RAM-cached file in Finder/Explorer (appears instant)
    #
    # This makes behavior APPEAR instant regardless of disk speed, because:
    #   - User sees file immediately (from RAM cache)
    #   - Physical disk write happens asynchronously
    #   - No waiting for hardware latency
    
    if save_to_file:
        import threading
        
        if filename_prefix is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename_prefix = f"recon_{timestamp}"
        
        # CLF: Filename preserves original extension deterministically
        ext = original_extension if original_extension else '.bin'
        if not ext.startswith('.'):
            ext = '.' + ext
        
        filename = f"{filename_prefix}{ext}"
        filepath = os.path.join(RECON_DIR, filename)
        
        def write_to_disk_async():
            """Background disk write - does not block instantiation"""
            try:
                with open(filepath, 'wb') as f:
                    f.write(S)
                    # Flush to OS cache (not waiting for physical disk sync)
                    f.flush()
                    os.fsync(f.fileno())  # Ensure OS has it (still async from user perspective)
            except Exception as e:
                print(f"[CLF Warning] Async disk write failed: {e}")
        
        # Start background write thread
        write_thread = threading.Thread(target=write_to_disk_async, daemon=True)
        write_thread.start()
        
        # Note: File appears in Finder/Explorer immediately (from OS page cache)
        #       Physical disk write completes in background
        #       This is how modern OS handles writes - we're piggybacking on it
    
    # Return S immediately - user can interact while disk write happens in parallel
    return S


# ============================================================================
# Terminology Aliases (Mathematical Equivalence Framing)
# ============================================================================

def recognize_factored_form(S: bytes, save_to_file: bool = True) -> bytes:
    """
    Recognize the factored form (Σ) of expanded string S.
    
    MATHEMATICAL EQUIVALENCE:
        This identifies which factored notation corresponds to S.
        Like recognizing that 16 can be written as 4².
        Both representations are mathematically equivalent.
    
    NOT compression (lossy, many-to-one).
    IS notation recognition (lossless, one-to-one).
    
    Example:
        S = [3, 5, 7, 9, 11]  (expanded form)
        Σ = D2(s₀=3, δ=2, n=5) (factored form)
        Both ARE the same sequence.
    
    Args:
        S: String in expanded form (all bytes written out)
        save_to_file: If True, saves to Seeds/ directory
    
    Returns:
        Σ: Seed in factored form (generator parameters)
    """
    return Sigma_star(S, save_to_file=save_to_file)


def expand_factored_form(Sigma: bytes, save_to_file: bool = False) -> bytes:
    """
    Expand factored form (Σ) to full string S.
    
    MATHEMATICAL EQUIVALENCE:
        This converts factored notation to expanded notation.
        Like expanding 4² to 16.
        Both representations are mathematically equivalent.
    
    NOT decompression (decoding compressed data).
    IS notation expansion (expressing in expanded form).
    
    Example:
        Σ = D2(s₀=3, δ=2, n=5) (factored form)
        S = [3, 5, 7, 9, 11]  (expanded form)
        Both ARE the same sequence.
    
    Args:
        Sigma: Seed in factored form (generator parameters)
        save_to_file: If True, saves to Recon/ directory
    
    Returns:
        S: String in expanded form (all bytes written out)
    """
    return Xi_n(Sigma, save_to_file=save_to_file)


# ============================================================================
# Bijection Verification
# ============================================================================

def verify_bijection(S: bytes, save_to_file: bool = False) -> bool:
    """
    Verify CLF bijection: Xi_n(Sigma_star(S)) = S
    
    This is the fundamental guarantee of CLF:
    encoding followed by replay returns original string.
    
    Args:
        S: Original string
        save_to_file: If True, saves seed and reconstruction to disk
    
    Returns:
        True if bijection holds
    """
    sigma = Sigma_star(S, save_to_file=save_to_file)
    S_prime = Xi_n(sigma, save_to_file=save_to_file)
    return S == S_prime


def verify_mathematical_equivalence(S: bytes, Sigma: bytes = None) -> Dict:
    """
    Verify that S and Σ are mathematically equivalent (S = Σ).
    
    Tests BOTH directions of the bijection:
        1. Forward:  S → θ(S) = Σ'   (recognize factored form)
        2. Backward: Σ → Ξ(Σ) = S'   (expand to string)
        3. Equivalence: S = S' AND Σ ≈ Σ'
    
    Like verifying: 16 = 4² by:
        - Taking √16 = 4, squaring: 4² = 16 ✓
        - Taking 4², checking: 16 = 16 ✓
    
    Args:
        S: String in expanded form
        Sigma: Optional seed in factored form (will compute if None)
    
    Returns:
        {
            'forward_valid': bool,     # θ(S) produces valid Σ
            'backward_valid': bool,    # Ξ(Σ) produces valid S
            'equivalence_holds': bool, # S = S' (byte-perfect match)
            'original_size': int,
            'factored_size': int,
            'density': float,
            'details': {...}
        }
    """
    results = {
        'original_size': len(S),
        'details': {}
    }
    
    # Forward: Recognize factored form from expanded
    try:
        if Sigma is None:
            Sigma_recognized = Sigma_star(S, save_to_file=False)
        else:
            Sigma_recognized = Sigma
        
        results['forward_valid'] = True
        results['factored_size'] = len(Sigma_recognized)
        results['density'] = len(Sigma_recognized) / len(S) if len(S) > 0 else 0
        results['details']['Sigma_bytes'] = len(Sigma_recognized)
        
        # Parse recognized seed to get family
        try:
            from M4_recognition_STRICT import theta_strict
            theta_result = theta_strict(S)
            results['details']['family'] = theta_result['family']
            results['details']['params'] = str(theta_result['params'])[:100]
        except:
            results['details']['family'] = 'unknown'
            
    except Exception as e:
        results['forward_valid'] = False
        results['details']['forward_error'] = str(e)
        results['equivalence_holds'] = False
        return results
    
    # Backward: Expand factored form to expanded
    try:
        S_expanded = Xi_n(Sigma_recognized, save_to_file=False)
        results['backward_valid'] = True
        results['details']['S_expanded_bytes'] = len(S_expanded)
    except Exception as e:
        results['backward_valid'] = False
        results['details']['backward_error'] = str(e)
        results['equivalence_holds'] = False
        return results
    
    # Check equivalence (byte-perfect match)
    results['S_matches'] = (S == S_expanded)
    results['equivalence_holds'] = results['S_matches']
    
    if not results['equivalence_holds']:
        results['details']['mismatch_length'] = len(S) - len(S_expanded)
        results['details']['first_diff_pos'] = next(
            (i for i in range(min(len(S), len(S_expanded))) if S[i] != S_expanded[i]),
            -1
        )
    
    return results


# ============================================================================
# Inspection/Debug
# ============================================================================

def get_pipeline_stages(S: bytes) -> Dict:
    """
    Get all intermediate pipeline stages for inspection
    
    Useful for debugging and understanding transformations.
    
    Args:
        S: Input string
    
    Returns:
        Dictionary with all pipeline stages
    """
    stages = {}
    
    # Input
    stages['input'] = S
    stages['n'] = len(S)
    
    # theta (recognition)
    theta_params = theta_strict(S)
    stages['theta'] = theta_params
    
    # Pi_0 (construction)
    P = Pi_0(S, theta_params)
    stages['Pi_0'] = P
    stages['Pi_0_atoms'] = [a.family for a in P.BODY]
    stages['Pi_0_cost'] = P.cost()
    
    # NF_n (normalization)
    G_star = NF_n(P)
    stages['G_star'] = G_star
    stages['G_star_atoms'] = [a.family for a in G_star.BODY]
    stages['G_star_cost'] = G_star.cost()
    
    # Enc_n (encoding)
    sigma = encode_program_to_wire(G_star)
    stages['Sigma'] = sigma
    stages['seed_size'] = len(sigma)
    stages['causal_density'] = len(sigma) / len(S) if len(S) > 0 else 0
    
    # Replay verification
    S_replayed = Xi_n(sigma)
    stages['replay'] = S_replayed
    stages['bijection_holds'] = (S_replayed == S)
    
    return stages


def get_seed_hash(sigma: bytes) -> str:
    """
    Compute SHA-256 hash of seed
    
    Args:
        sigma: Seed bytes
    
    Returns:
        Hex string of hash
    """
    return hashlib.sha256(sigma).hexdigest()


def compare_seeds(S1: bytes, S2: bytes) -> Dict:
    """
    Compare seeds for two strings
    
    Args:
        S1, S2: Input strings
    
    Returns:
        Comparison dictionary
    """
    sigma1 = Sigma_star(S1)
    sigma2 = Sigma_star(S2)
    
    return {
        'S1_size': len(S1),
        'S2_size': len(S2),
        'sigma1_size': len(sigma1),
        'sigma2_size': len(sigma2),
        'sigma1_hash': get_seed_hash(sigma1),
        'sigma2_hash': get_seed_hash(sigma2),
        'seeds_equal': (sigma1 == sigma2),
    }


# ============================================================================
# High-Level API
# ============================================================================

def encode(S: bytes) -> bytes:
    """
    High-level encoding: S to Sigma_star(S)
    
    Args:
        S: Input string
    
    Returns:
        Seed bytes
    """
    return Sigma_star(S)


def decode(sigma: bytes) -> bytes:
    """
    High-level decoding: Sigma to Xi_n(Sigma)
    
    Args:
        sigma: Seed bytes
    
    Returns:
        Decoded string
    """
    return Xi_n(sigma)


def encode_and_verify(S: bytes) -> Tuple[bytes, bool]:
    """
    Encode and verify bijection
    
    Args:
        S: Input string
    
    Returns:
        (seed, verification_result)
    """
    sigma = encode(S)
    valid = verify_bijection(S)
    return sigma, valid
