"""
CLF Causal Family Registry - Formal Definition of Law Space ℒ

Defines the complete algebra of causal laws available to CLF recognition.
Each family represents a distinct mathematical structure for generating
string sequences through deterministic position functions.

Registry serves as mathematical specification for:
- Law family validation
- Closure property verification
- Parameter arity constraints
- Compositional rules for D9_RADIAL
"""

# Law Not Found Error for registry misses
class LawNotFoundError(Exception):
    """Raised when accessing undefined causal law family."""
    pass


# Complete definition of CLF causal families
CAUSAL_FAMILIES = {
    "D1_CONST": {
        "arity": 1, 
        "closure": "constant",
        "description": "Constant law: E₁(i, {c, n}) = c",
        "parameters": ["c"],
        "mathematical_form": "∀i: S[i] = c"
    },
    "D2_AFFINE": {
        "arity": 2, 
        "closure": "affine",
        "description": "Affine law: E₂(i, {a, b, n}) = (a×i + b) mod 256", 
        "parameters": ["base_s0", "gradient_s0"],
        "mathematical_form": "S[i] = (a×i + b) mod 256"
    },
    "D3_PERIODIC": {
        "arity": 3, 
        "closure": "periodic",
        "description": "Periodic law: E₃(i, {pattern, n}) = pattern[i mod len(pattern)]",
        "parameters": ["pattern", "period"],
        "mathematical_form": "S[i] = pattern[i mod |pattern|]"
    },
    "D4_XOR_AFFINE": {
        "arity": 4,
        "closure": "xor_composition", 
        "description": "XOR-Affine composition: E₄(i, {s0, delta, xor}) = (s0 + i×delta) ⊕ xor",
        "parameters": ["s0", "delta_mod", "xor_const"],
        "mathematical_form": "S[i] = (s0 + i×delta) ⊕ xor_const"
    },
    "D5_QUADRATIC": {
        "arity": 5,
        "closure": "polynomial",
        "description": "Quadratic polynomial: E₅(i, {a, b, c}) = (a×i² + b×i + c) mod 256",
        "parameters": ["a", "b", "c"],
        "mathematical_form": "S[i] = (a×i² + b×i + c) mod 256"
    },
    "D6_LCG": {
        "arity": 6,
        "closure": "linear_congruential",
        "description": "Linear congruential generator with affine transform",
        "parameters": ["seed", "multiplier", "increment", "offset"],
        "mathematical_form": "LCG state with position mapping"
    },
    "D6_MIRROR": {
        "arity": 6,
        "closure": "palindromic",
        "description": "Mirror/palindrome structure detection",
        "parameters": ["center", "pattern"],
        "mathematical_form": "S[i] = S[2c - i] for center c"
    },
    "D7_SEGMENTED": {
        "arity": 7,
        "closure": "piecewise",
        "description": "Piecewise constant segments",
        "parameters": ["boundaries", "values"],
        "mathematical_form": "Piecewise constant over intervals"
    },
    "D9_RADIAL": {
        "arity": 9, 
        "closure": "bounded-radial",
        "description": "Radial compositional: E₉(i, {center, laws}) = E_{law_r}(i) where r = |i - center|",
        "parameters": ["center", "ring_laws"],
        "mathematical_form": "Ξ₉(i) = Ξ_{law_r}(i) where r = |i - center|"
    },
    "D9_LIMIT_CAUSAL_CLOSURE": {
        "arity": 9,
        "closure": "limit_closure", 
        "description": "Asymptotic causal closure for large strings",
        "parameters": ["limit_law", "convergence_rate"],
        "mathematical_form": "lim_{n→∞} causal_structure(S_n)"
    },
    "D9_CAUSAL_CLOSED": {
        "arity": 9,
        "closure": "complete_closure",
        "description": "Complete causal closure - mathematical closure achieved", 
        "parameters": ["closed_law"],
        "mathematical_form": "∀i: structural_law(i) determined"
    }
}


def get_family(name):
    """
    Retrieve causal family definition by name.
    
    Args:
        name: Family identifier (e.g., "D2_AFFINE")
        
    Returns:
        dict: Family specification with arity, closure, description
        
    Raises:
        LawNotFoundError: If family not registered in ℒ
    """
    if name not in CAUSAL_FAMILIES:
        raise LawNotFoundError(f"Family {name} not registered in causal algebra ℒ")
    return CAUSAL_FAMILIES[name]


def validate_family_parameters(family_name, params):
    """
    Validate parameters match family arity specification.
    
    Args:
        family_name: Name of causal family
        params: Parameter dictionary
        
    Returns:
        bool: True if parameters match family specification
        
    Raises:
        LawNotFoundError: If family undefined
        ValueError: If parameter arity mismatch
    """
    family = get_family(family_name)
    expected_params = family["parameters"]
    
    # Check parameter presence
    for param in expected_params:
        if param not in params:
            raise ValueError(f"Missing parameter {param} for family {family_name}")
    
    return True


def get_closure_type(family_name):
    """
    Get mathematical closure type for family.
    
    Args:
        family_name: Name of causal family
        
    Returns:
        str: Closure type ("constant", "affine", "periodic", etc.)
    """
    family = get_family(family_name)
    return family["closure"]


def is_compositional_family(family_name):
    """
    Check if family supports compositional laws (like D9_RADIAL).
    
    Args:
        family_name: Name of causal family
        
    Returns:
        bool: True if family can compose other laws
    """
    closure = get_closure_type(family_name)
    return closure in ["bounded-radial", "limit_closure", "complete_closure"]


def list_available_families():
    """
    List all registered causal families.
    
    Returns:
        list: Family names available in current vocabulary
    """
    return list(CAUSAL_FAMILIES.keys())


def get_mathematical_form(family_name):
    """
    Get the mathematical form/equation for a family.
    
    Args:
        family_name: Name of causal family
        
    Returns:
        str: Mathematical description of the law
    """
    family = get_family(family_name)
    return family["mathematical_form"]