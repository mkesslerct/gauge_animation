import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FIGURES_DIRECTORY = Path("quique_figures")
if not FIGURES_DIRECTORY.exists():
    FIGURES_DIRECTORY.mkdir(parents=True, exist_ok=True)


tps_values_java = np.array([1, 50, 100, np.NaN, np.NaN, np.NaN, 60])
tps_values_rust = np.array([1, 50, 100, 150, 200, 250, 240])
java_results = np.array([1, 1, 0, 0, 0, 0, 1])
rust_results = np.array([1, 1, 1, 1, 1, 0, 1])
colores = {0: "red", 1: "green"}
# Data for Rust service
# Plotting the dat
# for i in range(tps_values.shape[0]):
delta = 0.5
for i in range(1, 8):
    x_values = np.array([1, 2, 3, 4, 5, 6, 9])[:i]
    y_values_java = tps_values_java[:i]
    y_values_rust = tps_values_rust[:i]
    fig, ax = plt.subplots(figsize=(10, 6))
    java_bars = ax.bar(
        x_values - delta / 2,
        y_values_java,
        width=delta,
        color=[colores[r] for r in java_results[:i]],
        edgecolor="white",
    )
    rust_bars = ax.bar(
        x_values + delta / 2,
        y_values_rust,
        width=delta,
        color=[colores[r] for r in rust_results[:i]],
        edgecolor="white",
    )
    ax.bar_label(java_bars, ["Java" for j in range(i)])
    ax.bar_label(rust_bars, ["Rust" for j in range(i)])
    ax.set_xlabel("Attempt")
    ax.set_ylabel("TPS")
    ax.set_title("Load Test Results: Rust (upper half) vs Java (lower half)")
    ax.set_ylim(0, 275)
    ax.set_xlim(0, 10)
    plt.savefig(FIGURES_DIRECTORY / f"tps_values_{i:02}.png")
    plt.close(fig)
