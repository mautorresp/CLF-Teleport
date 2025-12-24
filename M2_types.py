"""
M2_types.py - Core Mathematical Objects
CLF 2.txt Section 0: Vocabulary & objects

Defines: Conf, Atom, Prog
Pure data structures - no semantics, no execution

These types represent mathematical objects in CLF's universe:
- Conf: Configuration space (state at a point in execution)
- Atom: Single operation (ω, θ) with declared inverse
- Prog: Finite program (sequence of atoms)

All objects are self-contained with complete information.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


# ============================================================================
# Configuration Space: Conf
# ============================================================================

@dataclass
class Conf:
    """
    Configuration: (M, A, σ, edition-pinned loci)
    
    CLF 2.txt Section 0:
    - M: Memory (includes ℓ_out output region)
    - A(n): Ancilla/state registers (working memory)
    - σ: Sentinel/state vector (for guarded families)
    
    Represents complete machine state at any point in execution.
    """
    M: bytearray  # Full memory
    ell_out_start: int  # Output region start index
    ell_out_len: int  # Output region length (= n)
    A: Dict[str, Any]  # Ancilla registers
    sigma: bytearray  # Sentinels
    edition: str  # Edition identifier
    
    def __post_init__(self):
        """Verify configuration invariants"""
        if self.ell_out_start < 0:
            raise ValueError("ell_out_start must be >= 0")
        if self.ell_out_len < 0:
            raise ValueError("ell_out_len must be >= 0")
        if self.ell_out_start + self.ell_out_len > len(self.M):
            raise ValueError("ell_out region exceeds memory bounds")
    
    def get_output(self) -> bytes:
        """Extract ℓ_out (output region)"""
        return bytes(self.M[self.ell_out_start:self.ell_out_start + self.ell_out_len])
    
    def set_output(self, data: bytes):
        """Write to ℓ_out region"""
        if len(data) != self.ell_out_len:
            raise ValueError(f"Output data must be {self.ell_out_len} bytes")
        self.M[self.ell_out_start:self.ell_out_start + self.ell_out_len] = bytearray(data)
    
    def clone(self) -> 'Conf':
        """Deep copy configuration"""
        return Conf(
            M=bytearray(self.M),
            ell_out_start=self.ell_out_start,
            ell_out_len=self.ell_out_len,
            A=dict(self.A),
            sigma=bytearray(self.sigma),
            edition=self.edition
        )
    
    def __repr__(self) -> str:
        output_hex = self.get_output().hex()
        preview = output_hex[:40] + ('...' if len(output_hex) > 40 else '')
        return f"Conf(n={self.ell_out_len}, ℓ_out={preview})"


def make_C_init(n: int, edition: str = "v3.3.8") -> Conf:
    """
    Construct C_init(n): initial configuration.
    
    CLF 2.txt Section 0: C_init(n) = (M_init, σ_init)
    
    Args:
        n: Arity (output length)
        edition: Edition identifier
    
    Returns:
        Initial configuration with:
        - Memory initialized to zeros
        - ℓ_out region = [0:n]
        - Empty ancilla
        - Initialized sentinels
    """
    return Conf(
        M=bytearray(n),  # Initially all zeros
        ell_out_start=0,
        ell_out_len=n,
        A={},  # No ancilla initially
        sigma=bytearray(),  # No sentinels initially
        edition=edition
    )


# ============================================================================
# Atomic Operation: Atom
# ============================================================================

@dataclass
class Atom:
    """
    Atomic operation: (ω, θ)
    
    CLF 2.txt Section 0: "Families ω ∈ 𝓕"
    CLF 2.txt Section 1: "each atom (ω,θ) has τ_{inv_ω(θ)} = τ_{(ω,θ)}⁻¹"
    
    Components:
    - family: Operation family ω (e.g., "RLE_SHORT", "CONST", "COPY")
    - theta: Parameters θ (family-specific)
    - inv: Declared inverse atom (for reversibility)
    - embedding: Optional embedding index (for MOVE operations)
    """
    family: str
    theta: Dict[str, Any]
    inv: Optional['Atom'] = None
    embedding: Optional[int] = None
    
    def __post_init__(self):
        """Establish bidirectional inverse relationship"""
        if self.inv is not None and self.inv.inv is None:
            self.inv.inv = self
    
    def is_identity(self) -> bool:
        """Check if this is the identity operation"""
        return self.family == 'id'
    
    def is_inverse_of(self, other: 'Atom') -> bool:
        """Check if this atom is the inverse of another"""
        return self.inv is other or other.inv is self
    
    def __repr__(self) -> str:
        theta_str = ', '.join(f"{k}={v}" for k, v in self.theta.items())
        emb_str = f"@{self.embedding}" if self.embedding is not None else ""
        return f"Atom({self.family}{emb_str}, θ=[{theta_str}])"


def id_atom() -> Atom:
    """
    Identity atom: τ_id = id
    
    CLF 2.txt Section 4: R1: id → ε
    """
    atom = Atom(family='id', theta={})
    atom.inv = atom  # Identity is self-inverse
    return atom


def make_inverse_atom(family: str, theta: Dict[str, Any]) -> Atom:
    """
    Construct inverse atom for a given family.
    
    Naming convention: family_INV (e.g., "RLE_SHORT_INV")
    Preserves theta parameters (operation is symmetric).
    """
    inv_family = f"{family}_INV"
    return Atom(family=inv_family, theta=theta.copy())


# ============================================================================
# Program: Prog
# ============================================================================

@dataclass
class Prog:
    """
    Program: finite sequence of atoms
    
    CLF 2.txt Section 0: "Prog(n): SDL-typed, finite, decidable"
    CLF 2.txt Section 5: Structure = HEAD || BODY [|| COMMIT]
    
    Components:
    - n: Arity (output length)
    - BODY: Sequence of atoms
    - HEAD: Edition/codec metadata
    - COMMIT: Optional SHA-256 witness
    """
    n: int
    BODY: List[Atom]
    HEAD: Dict[str, Any] = field(default_factory=dict)
    COMMIT: Optional[bytes] = None
    
    def __post_init__(self):
        """Verify program invariants"""
        if self.n < 0:
            raise ValueError("Arity n must be >= 0")
        if not isinstance(self.BODY, list):
            raise ValueError("BODY must be a list")
        
        # Set default HEAD if not provided
        if not self.HEAD:
            self.HEAD = {"edition": "v3.3.8"}
    
    def reverse(self) -> 'Prog':
        """
        Construct Π^†: reverse program using inverses.
        
        CLF 2.txt Section 1: Π^† (reverse list using inv_ω)
        satisfies τ_{Π^†} = (τ_Π)⁻¹
        
        Returns:
            Reversed program with inverse atoms
        """
        reversed_atoms = []
        for atom in reversed(self.BODY):
            if atom.inv is None:
                raise ValueError(f"Atom {atom.family} has no declared inverse")
            reversed_atoms.append(atom.inv)
        
        return Prog(
            n=self.n,
            BODY=reversed_atoms,
            HEAD=self.HEAD.copy(),
            COMMIT=self.COMMIT
        )
    
    def cost(self) -> int:
        """
        Compute cost: |BODY| (non-identity atoms)
        
        CLF 2.txt Section 6: cost_n(Π) := |BODY(NF_n(Π))|
        cost_HEAD = cost_COMMIT = 0
        
        Returns:
            Number of non-identity atoms
        """
        return len([a for a in self.BODY if not a.is_identity()])
    
    def wire_size(self) -> int:
        """
        Access wire representation size property.
        
        CLF Principle: Program P exists → |wire(P)| exists as intrinsic property
        The wire size is NOT computed - it EXISTS as a mathematical property.
        
        On Turing substrate: Must determine through encoding structure
        On CLF substrate: Would be directly accessible
        
        CLF 2.txt Section 6:
        |Σ*_n(S)| = c_H + c_C + ∑(c_I(ω_j) + ‖θ_j‖_{ω_j})
        
        Returns:
            Wire size in bits
        """
        # Import here to avoid circular dependency
        from M1_codec import cost_HEAD, Lgamma
        
        total_bits = cost_HEAD()
        total_bits += Lgamma(self.n + 1)  # Arity prefix
        
        # Atom costs (family-specific, simplified)
        for atom in self.BODY:
            total_bits += 8  # Opcode
            # Parameters
            for val in atom.theta.values():
                if isinstance(val, int) and val >= 0:
                    total_bits += Lgamma(val + 1)
        
        if self.COMMIT is not None:
            from M1_codec import cost_COMMIT
            total_bits += cost_COMMIT()
        
        return total_bits
    
    def __len__(self) -> int:
        """Number of atoms in BODY"""
        return len(self.BODY)
    
    def __repr__(self) -> str:
        atoms_preview = self.BODY[:3]
        atoms_str = ', '.join(str(a) for a in atoms_preview)
        if len(self.BODY) > 3:
            atoms_str += f', ... ({len(self.BODY)} total)'
        return f"Prog(n={self.n}, atoms=[{atoms_str}])"
    
    def __eq__(self, other: object) -> bool:
        """
        Structural equality for programs.
        
        Two programs are equal if they have:
        - Same arity n
        - Same BODY atoms (family + theta)
        - Same HEAD edition
        """
        if not isinstance(other, Prog):
            return NotImplemented
        
        if self.n != other.n:
            return False
        
        if len(self.BODY) != len(other.BODY):
            return False
        
        for a1, a2 in zip(self.BODY, other.BODY):
            if a1.family != a2.family or a1.theta != a2.theta:
                return False
        
        return self.HEAD.get("edition") == other.HEAD.get("edition")


# ============================================================================
# Module Metadata
# ============================================================================

__all__ = [
    # Configuration
    'Conf',
    'make_C_init',
    
    # Atoms
    'Atom',
    'id_atom',
    'make_inverse_atom',
    
    # Programs
    'Prog',
]
