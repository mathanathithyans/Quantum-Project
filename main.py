from itertools import product

# Four delivery zones
zones = ["A", "B", "C", "D"]

# Connections between zones and their weights
edges = [
    ("A", "B", 5),
    ("A", "C", 2),
    ("A", "D", 4),
    ("B", "C", 3),
    ("B", "D", 6),
    ("C", "D", 1)
]


def calculate_cut(partition):
    cut_value = 0

    for u, v, weight in edges:
        if partition[u] != partition[v]:
            cut_value += weight

    return cut_value


best_value = -1
best_partitions = []

# Try all possible assignments of four zones
for assignment in product([0, 1], repeat=len(zones)):
    partition = dict(zip(zones, assignment))
    cut_value = calculate_cut(partition)

    if cut_value > best_value:
        best_value = cut_value
        best_partitions = [partition.copy()]

    elif cut_value == best_value:
        best_partitions.append(partition.copy())

print("DELIVERY ZONE MAX-CUT OPTIMIZATION")
print("-" * 40)

print("Zones:", zones)
print("Connections:", len(edges))
print("Maximum cut value:", best_value)
print("\nOptimal partition:")

for partition in best_partitions:
    group_0 = [z for z in zones if partition[z] == 0]
    group_1 = [z for z in zones if partition[z] == 1]

    print(f"Group 1: {group_0} | Group 2: {group_1}")
