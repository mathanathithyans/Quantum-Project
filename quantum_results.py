import matplotlib.pyplot as plt

# Results from the current quantum simulation
states = [
    "0011", "1100", "0100", "1011",
    "1001", "0110", "1010", "0101",
    "1101", "0010"
]

probabilities = [
    0.4108, 0.4108, 0.0512, 0.0512,
    0.0371, 0.0371, 0.0005, 0.0005,
    0.0003, 0.0003
]

cut_values = [15, 15, 14, 14, 14, 14, 13, 13, 6, 6]

# Highlight optimal solutions
colors = [
    "green" if cut == 15 else "skyblue"
    for cut in cut_values
]

plt.figure(figsize=(12, 6))

plt.bar(states, probabilities, color=colors)

plt.title("Quantum Adiabatic Max-Cut Results")
plt.xlabel("Measured Quantum State")
plt.ylabel("Probability")
plt.ylim(0, 0.46)

plt.figtext(
    0.5, 0.01,
    "Green = Optimal cut (15) | Blue = Suboptimal cuts",
    ha="center"
)

plt.tight_layout()
plt.show()

# Display summary
print("QUANTUM RESULTS SUMMARY")
print("-" * 35)
print("Classical optimal cut: 15")
print("Expected quantum cut: 14.8148")
print("Optimal-solution probability: 82.164274%")
