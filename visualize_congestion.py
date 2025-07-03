import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# Parameters
DIM = 10
NODES = 1 << DIM

# Helper to build graph and extract congestion
def load_congestion(filename):
    df = pd.read_csv(filename)
    g = nx.Graph()
    g.add_nodes_from(range(NODES))
    for _, row in df.iterrows():
        g.add_edge(row['node1'], row['node2'], congestion=row['congestion'])
    congestion = np.array([d['congestion'] for u, v, d in g.edges(data=True)])
    return g, congestion

# Load both modes
G_valiant, cong_valiant = load_congestion('congestion_valiant.csv')
G_det, cong_det = load_congestion('congestion_deterministic.csv')

# Normalize for color/thickness
max_cong = max(cong_valiant.max(), cong_det.max())
min_cong = min(cong_valiant.min(), cong_det.min())

# Layout (same for both for fair comparison)
pos = nx.spring_layout(G_valiant, seed=42, dim=2)

# --- Network Plots ---
fig = plt.figure(figsize=(18, 8))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 0.05], wspace=0.15)
ax0 = fig.add_subplot(gs[0])
ax1 = fig.add_subplot(gs[1])
cax = fig.add_subplot(gs[2])  # Colorbar axis

for ax, G, congestion, title in zip(
    [ax0, ax1],
    [G_valiant, G_det],
    [cong_valiant, cong_det],
    ["Valiant's Routing (Random Intermediate)", "Deterministic Bit-Fixing Routing"]
):
    edge_colors = [(c - min_cong) / (max_cong - min_cong + 1e-6) for c in congestion]
    edge_widths = [1 + 4 * (c - min_cong) / (max_cong - min_cong + 1e-6) for c in congestion]
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color='lightblue', ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=7)
    edges = nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=edge_widths,
        edge_cmap=plt.cm.plasma,
        edge_vmin=0, edge_vmax=1,
        ax=ax
    )
    ax.set_title(title)
    ax.axis('off')

fig.colorbar(edges, cax=cax, label='Normalized Congestion')
plt.suptitle('4D Hypercube Network Congestion Comparison')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('network_comparison.png')
plt.show()

# --- Histogram Plots ---
fig, axes = plt.subplots(1, 2, figsize=(16, 5))
for ax, congestion, title in zip(
    axes,
    [cong_valiant, cong_det],
    ["Valiant's Routing (Random Intermediate)", "Deterministic Bit-Fixing Routing"]
):
    ax.hist(congestion, bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel('Link Congestion (Number of Flows)')
    ax.set_ylabel('Number of Links')
    ax.set_title(f'Histogram: {title}')
plt.suptitle('Histogram of Link Congestion Comparison')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('histogram_comparison.png')
plt.show() 