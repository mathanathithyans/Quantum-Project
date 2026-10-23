import numpy as np
from scipy.linalg import expm

# Four delivery zones
zones = ["A", "B", "C", "D"]

# Weighted connections
edges = [
    (0, 1, 5),  # A-B
    (0, 2, 2),  # A-C
    (0, 3, 4),  # A-D
    (1, 2, 3),  # B-C
    (1, 3, 6),  # B-D
    (2, 3, 1)   # C-D
]

N = len(zones)
DIM = 2**N

I = np.eye(2, dtype=complex)

X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex)

Z = np.array([
    [1, 0],
    [0, -1]
], dtype=complex)


def operator_on_qubit(operator, qubit):
    result = np.array([[1]], dtype=complex)

    for i in range(N):
        result = np.kron(
            result,
            operator if i == qubit else I
        )

    return result


# Construct Pauli operators for each qubit
X_ops = [operator_on_qubit(X, i) for i in range(N)]
Z_ops = [operator_on_qubit(Z, i) for i in range(N)]

# Mixer Hamiltonian
H_mixer = -sum(X_ops)

# Cost Hamiltonian for adiabatic minimization
H_cost = np.zeros((DIM, DIM), dtype=complex)

for i, j, weight in edges:
    H_cost -= (
        weight / 2
        * (np.eye(DIM) - Z_ops[i] @ Z_ops[j])
    )

# Verify the Hamiltonian construction
print("Mixer Hermitian:", np.allclose(H_mixer, H_mixer.conj().T))
print("Cost Hermitian:", np.allclose(H_cost, H_cost.conj().T))

print("Mixer ground-state energy:",
      np.linalg.eigvalsh(H_mixer)[0])

print("Cost ground-state energy:",
      np.linalg.eigvalsh(H_cost)[0])

# Initial state: equal superposition of all 16 basis states
state = np.ones(DIM, dtype=complex) / np.sqrt(DIM)

# Adiabatic evolution settings
steps = 100
total_time = 10.0
dt = total_time / steps

# Trotterized evolution
for step in range(steps):
    s = (step + 0.5) / steps

    H_mix_part = (1 - s) * H_mixer
    H_cost_part = s * H_cost

    U_mix = expm(-1j * H_mix_part * dt)
    U_cost = expm(-1j * H_cost_part * dt)

    state = U_cost @ state
    state = U_mix @ state

# Measurement probabilities
probabilities = np.abs(state) ** 2


# Classical cut value for a measured bitstring
def calculate_cut(bitstring):
    value = 0

    for i, j, weight in edges:
        if bitstring[i] != bitstring[j]:
            value += weight

    return value


# Rank all outcomes by probability
results = []

for index, probability in enumerate(probabilities):
    bitstring = format(index, f"0{N}b")
    cut_value = calculate_cut(bitstring)

    results.append(
        (bitstring, probability, cut_value)
    )

results.sort(key=lambda item: item[1], reverse=True)

print("\nADIABATIC MAX-CUT SIMULATION")
print("-" * 45)

print("Number of qubits:", N)
print("Trotter steps:", steps)
print("Total evolution time:", total_time)

print("\nMost probable outcomes:")

for bitstring, probability, cut_value in results[:10]:
    print(
        f"State: {bitstring} | "
        f"Probability: {probability:.4f} | "
        f"Cut value: {cut_value}"
    )

# Calculate expected cut value
expected_cut = sum(
    probability * cut_value
    for _, probability, cut_value in results
)

# Calculate probability of measuring an optimal solution
optimal_probability = sum(
    probability
    for _, probability, cut_value in results
    if cut_value == 15
)

print("\nRESULT ANALYSIS")
print("-" * 45)

print("Classical optimal cut:", 15)
print("Expected quantum cut:", round(expected_cut, 4))
print(
    "Probability of measuring an optimal cut:",
    f"{optimal_probability:.6%}"
)

print(
    "Highest cut value represented:",
    max(item[2] for item in results)
)
