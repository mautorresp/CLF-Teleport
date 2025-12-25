#!/usr/bin/env python3
"""
Analyze gradient patterns in ring_laws to understand closure requirements.
"""

from M4_recognition_SAMPLED import BinaryStringSampler, theta_sampled

# Pick a representative file
filepath = './test_artifacts/test_message.txt'

print(f"Analyzing: {filepath}")
print("="*80)

s = BinaryStringSampler(filepath)
seed = theta_sampled(s)

ring_laws = seed['params'].get('ring_laws', {})
print(f"Ring laws count: {len(ring_laws)}\n")

# Extract and sort radii
radii = sorted([int(k) if isinstance(k, str) else k for k in ring_laws.keys()])
print(f"Sampled radii: {radii}\n")

# Extract s₀ and δ values
s0_list = []
delta_list = []

for r in radii:
    rseed = ring_laws[r]
    family = rseed.get('family')
    params = rseed.get('params', {})
    
    if family == 'D1':
        s0 = int(params.get('c', 0))
        delta = 0
    elif family == 'D2':
        s0 = int(params.get('s0', 0))
        delta = int(params.get('delta', 0))
    else:
        s0 = 0
        delta = 0
    
    s0_list.append(s0)
    delta_list.append(delta)

print("r\ts₀\tδ\tΔs₀\tΔ²s₀")
print("-"*60)

s0_diffs = []
for i in range(len(radii)):
    r = radii[i]
    s0 = s0_list[i]
    delta = delta_list[i]
    
    # First difference
    if i > 0:
        ds0 = (s0 - s0_list[i-1]) & 0xFF
        s0_diffs.append(ds0)
    else:
        ds0 = "-"
    
    # Second difference
    if i > 1:
        d2s0 = (s0_diffs[-1] - s0_diffs[-2]) & 0xFF if len(s0_diffs) >= 2 else "-"
    else:
        d2s0 = "-"
    
    print(f"{r}\t{s0}\t{delta}\t{ds0}\t{d2s0}")

print("\n" + "="*80)
print("ANALYSIS:")
print("="*80)

# Check if any pattern exists
if len(set(s0_diffs)) == 1:
    print(f"✅ First-order constant: Δs₀ = {s0_diffs[0]} (constant)")
elif len(s0_diffs) >= 2:
    s0_diff2 = [(s0_diffs[i+1] - s0_diffs[i]) & 0xFF for i in range(len(s0_diffs)-1)]
    unique_diff2 = set(s0_diff2)
    print(f"❌ First-order NOT constant: Δs₀ varies: {set(s0_diffs)}")
    print(f"   Second-order differences Δ²s₀: {s0_diff2}")
    print(f"   Unique Δ²s₀ values: {unique_diff2}")
    
    if len(unique_diff2) <= 3:
        print(f"   ⚠️  Near-quadratic (Δ²s₀ has {len(unique_diff2)} unique values)")
    else:
        print(f"   ❌ Highly non-linear (Δ²s₀ has {len(unique_diff2)} unique values)")

print("\n" + "="*80)
print("INTERPRETATION:")
print("="*80)
print("If Δ²s₀ is constant → quadratic s₀(r) = b + α₀·r + ½α₁·r²")
print("If Δ²s₀ varies → higher-order or truly discrete")
print("If all radii are evenly spaced → easier to detect patterns")
print(f"Actual spacing: {[radii[i+1]-radii[i] for i in range(len(radii)-1)]}")
