# Scalable Randomized Routing for Data Center Networks: Adversarial Permutation Analysis

## Overview

This project simulates and analyzes permutation routing in a hypercube data center network, comparing deterministic bit-fixing routing and Valiant's randomized routing. The focus is on the adversarial (bit-reversal) permutation, a classic worst-case scenario for deterministic routing. The results are visualized to show the dramatic advantage of Valiant's routing in balancing network load and reducing maximum congestion.

## Methodology

- **Network Model:** n Dim hypercube (2^n nodes), where each node represents a server/switch and edges represent network links.
- **Permutation Routing:** Each node sends a message to the bit-reversal of its address (adversarial permutation).
- **Routing Algorithms:**
  - **Deterministic Bit-Fixing:** Route from source to destination by fixing bits from left to right (MSB to LSB).
  - **Valiant's Routing:** Route from source to a random intermediate node, then from intermediate to destination, both using bit-fixing.
- **Congestion Analysis:** For each routing strategy, count how many flows traverse each link (edge).
- **Visualization:** Python scripts visualize the network, coloring/thickening edges by congestion, and plot a histogram of link congestion.

## Files

- `hypercube_sim.cpp` — C++ simulation code for both routing strategies and congestion analysis.
- `congestion_valiant.csv` — Output file for Valiant's routing (per-link congestion).
- `congestion_deterministic.csv` — Output file for deterministic routing (per-link congestion).
- `visualize_congestion.py` — Python script for network and histogram visualization.
- `README.md` — This documentation file.

## How to Run

### 1. Compile and Run the C++ Simulation

**Compile:**

```bash
# On Linux/Mac (g++ required)
g++ -std=c++11 -O2 -o hypercube_sim hypercube_sim.cpp
# On Windows (using g++ from MinGW or similar)
g++ -std=c++11 -O2 -o hypercube_sim.exe hypercube_sim.cpp
```

**Run for Valiant's routing:**

```bash
./hypercube_sim
# or
hypercube_sim.exe
```

**Run for deterministic routing:**

```bash
./hypercube_sim deterministic
# or
hypercube_sim.exe deterministic
```

This will generate `congestion_valiant.csv` and `congestion_deterministic.csv` in the same directory.

### 2. Visualize the Results in Python

**Install dependencies:**

```bash
pip install networkx matplotlib pandas numpy
```

**Run the visualization:**

```bash
python visualize_congestion.py
```

This will display:

- A plot of the hypercube network, with edge color/thickness representing congestion for both strategies.
- A histogram of link congestion values for both strategies.

## Output Explanation

- **congestion_valiant.csv / congestion_deterministic.csv:** Each row contains `node1,node2,congestion`, where `congestion` is the number of flows traversing the link between `node1` and `node2`.
- **Network Plot:** Nodes are arranged using a spring layout. Edges with higher congestion are thicker and more intensely colored.
- **Histogram:** Shows the distribution of congestion across all links for each routing strategy.

## Key Findings

- **Valiant's routing dramatically reduces maximum link congestion and balances the load across the network in the adversarial (bit-reversal) permutation.**
- **Deterministic bit-fixing routing creates severe bottlenecks, with some links experiencing much higher congestion.**
- This validates the use of Valiant's routing in scalable data center and parallel computer networks for worst-case traffic patterns.

## Customization

- To change the hypercube dimension, edit the `DIM` constant in `hypercube_sim.cpp`.
- The visualization script automatically adapts to the number of nodes/edges in the CSV files.

## Contact

For questions or improvements, please contact [Your Name].
