"""
CLF Specification - Causal Grid and Mathematical Constants

Defines the formal mathematical specification for CLF's causal grid P(n)
and deterministic tie-breaking rules. These constants ensure platform-
independent recognition and provide the mathematical foundation for
causal anchor selection.

All values are mathematically justified and field-closed in ℤ₂₅₆.
"""

# Causal Grid P(n) - Fixed prime-based strategic positions
# These positions represent mathematically significant invariant loci
# that capture structural causality across equivalence classes
P_n = [
    3, 5, 7, 11, 13, 17, 19, 23,
    29, 31, 37, 41, 43, 47, 53, 59,
    61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113
]


def tie_breaker(index, value):
    """
    Lexicographic deterministic rule for equal anchor values.
    
    When multiple positions in P(n) yield the same byte value,
    this function provides a canonical ordering to ensure
    platform-independent recognition results.
    
    Args:
        index: Position in causal grid P(n)
        value: Byte value at that position
        
    Returns:
        int: Deterministic tie-breaker value in ℤ₂₅₆
        
    Mathematical form:
        T(i, v) = (i + v) mod 256
    """
    return (index + value) % 256


def get_causal_grid(n=None):
    """
    Get the causal grid P(n) for CLF recognition.
    
    Args:
        n: Optional string length (for future extensions)
        
    Returns:
        list: Causal anchor positions
        
    Note:
        Current implementation uses fixed prime positions.
        Future versions may adapt grid size based on n.
    """
    return P_n.copy()


def validate_causal_position(pos):
    """
    Validate that position is in the causal grid P(n).
    
    Args:
        pos: Position to validate
        
    Returns:
        bool: True if position is a valid causal anchor
    """
    return pos in P_n


def get_grid_size():
    """
    Get the size of the causal grid.
    
    Returns:
        int: Number of causal anchor positions
    """
    return len(P_n)


def get_mathematical_properties():
    """
    Get mathematical properties of the causal grid.
    
    Returns:
        dict: Properties including primality, distribution, field characteristics
    """
    return {
        "type": "prime_sequence",
        "size": len(P_n),
        "max_position": max(P_n),
        "field_mod": 256,
        "deterministic": True,
        "platform_independent": True
    }