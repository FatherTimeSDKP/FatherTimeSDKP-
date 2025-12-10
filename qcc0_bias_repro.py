# qcc0_bias_repro.py
# Reproduce biased 3-qubit measurement distribution with '111' ≈ 26%
# Requires: qiskit (pip install qiskit qiskit-aer)

from qiskit import QuantumCircuit, Aer, transpile
from qiskit.quantum_info import Statevector
from math import sqrt
import numpy as np

# Target probabilities
p_target = 0.26                     # probability for |111>
p_other = (1.0 - p_target) / 7.0    # equal probability for each of the other 7 states

# Amplitudes (real, equal phase)
amp_target = sqrt(p_target)         # amplitude for |111>
amp_other  = sqrt(p_other)          # amplitude for each other basis state

# Build statevector in computational order |000>,|001>,...,|111>
state = [amp_other] * 7 + [amp_target]
# Verify normalization (should be 1.0)
norm = sum(abs(a)**2 for a in state)
if abs(norm - 1.0) > 1e-12:
    raise RuntimeError(f"State not normalized (norm={norm})")

# Create circuit and initialize with the statevector
qc = QuantumCircuit(3, 3)
qc.initialize(state, [0, 1, 2])
qc.measure([0,1,2],[0,1,2])

# Run on Aer simulator
backend = Aer.get_backend('aer_simulator')
tqc = transpile(qc, backend)
shots = 8192
result = backend.run(tqc, shots=shots, seed_simulator=42).result()
counts = result.get_counts()

# Print sorted counts (binary strings in qiskit are little-endian by default)
# Convert bitstrings to big-endian order for human-friendly display
def rev_bits(bitstr):
    return bitstr[::-1]

counts_be = {rev_bits(k): v for k, v in counts.items()}
sorted_counts = dict(sorted(counts_be.items(), key=lambda kv: kv[0]))
print("Measurement counts (big-endian):")
for k,v in sorted_counts.items():
    pct = 100.0 * v / shots
    print(f"  {k} : {v} ({pct:.2f}%)")

# Example expectation: '111' ~26.00%
