#include <iostream>
#include <vector>
#include <random>
#include <fstream>
#include <map>
#include <ctime>
#include <string>
#include <algorithm>

// Parameters
constexpr int DIM = 10; // 6D hypercube => 64 nodes
constexpr int NODES = 1 << DIM;
constexpr int TRIALS = 1; // Only need one trial for adversarial permutation

using Edge = std::pair<int, int>;

// Bit-fixing routing: fix bits from left (MSB) to right (LSB)
std::vector<Edge> bit_fixing_route(int src, int dst) {
    std::vector<Edge> path;
    int current = src;
    for (int d = DIM - 1; d >= 0; --d) {
        int src_bit = (current >> d) & 1;
        int dst_bit = (dst >> d) & 1;
        if (src_bit != dst_bit) {
            int next = current ^ (1 << d);
            path.emplace_back(std::min(current, next), std::max(current, next));
            current = next;
        }
    }
    return path;
}

// Bit-reversal function for DIM bits
int bit_reverse(int x) {
    int y = 0;
    for (int d = 0; d < DIM; ++d) {
        if (x & (1 << d)) y |= (1 << (DIM - 1 - d));
    }
    return y;
}

int main(int argc, char* argv[]) {
    // Choose routing mode: 'valiant' (default) or 'deterministic'
    std::string mode = "deterministic";
    if (argc > 1) {
        mode = argv[1];
    }
    std::string out_filename = (mode == "deterministic") ? "congestion_deterministic.csv" : "congestion_valiant.csv";

    std::mt19937 rng(static_cast<unsigned>(time(nullptr)));
    std::map<Edge, int> edge_congestion;

    for (int t = 0; t < TRIALS; ++t) {
        // Adversarial permutation: bit-reversal
        std::vector<int> dest(NODES);
        for (int i = 0; i < NODES; ++i) dest[i] = bit_reverse(i);

        for (int src = 0; src < NODES; ++src) {
            int dst = dest[src];
            if (src == dst) continue;
            if (mode == "deterministic") {
                auto path = bit_fixing_route(src, dst);
                for (const auto& edge : path) edge_congestion[edge]++;
            } else {
                int intermediate = rng() % NODES;
                while (intermediate == src || intermediate == dst) intermediate = rng() % NODES;
                auto path1 = bit_fixing_route(src, intermediate);
                auto path2 = bit_fixing_route(intermediate, dst);
                for (const auto& edge : path1) edge_congestion[edge]++;
                for (const auto& edge : path2) edge_congestion[edge]++;
            }
        }
    }

    // Output edge congestion to CSV
    std::ofstream out(out_filename);
    out << "node1,node2,congestion\n";
    for (const auto& entry : edge_congestion) {
        out << entry.first.first << "," << entry.first.second << "," << entry.second << "\n";
    }
    out.close();

    std::cout << "Simulation complete (" << mode << " routing, bit-reversal permutation). Congestion data written to " << out_filename << "\n";
    return 0;
} 
