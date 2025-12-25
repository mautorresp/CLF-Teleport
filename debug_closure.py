#!/usr/bin/env python3
"""Debug polynomial closure on test_message.txt"""

from M4_recognition_SAMPLED import BinaryStringSampler, theta_sampled, complete_ring_laws_causal

filepath = './test_artifacts/test_message.txt'
s = BinaryStringSampler(filepath)
seed = theta_sampled(s)

ring_laws = seed['params'].get('ring_laws', {})
print(f"Ring laws: {len(ring_laws)}")

# Try causal completion
meta = complete_ring_laws_causal(ring_laws, max_degree=3)

if meta:
    print(f"\n✅ Closure successful!")
    print(f"Type: {meta['type']}")
    print(f"Degree: {meta.get('degree', 'N/A')}")
    print(f"Alpha coeffs: {meta.get('alpha_coeffs', 'N/A')}")
    print(f"Beta coeffs: {meta.get('beta_coeffs', 'N/A')}")
else:
    print("\n❌ Closure failed - returned None")
    print("Polynomial did not converge or fit failed verification")
