import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pathlib import Path

FIGURES_DIRECTORY = Path("quique_figures") / "tmp"
if not FIGURES_DIRECTORY.exists():
    FIGURES_DIRECTORY.mkdir(parents=True, exist_ok=True)


def plot_gauge(ax, tps_value, x_axis_val, colors, title):
    gauge = ax.bar(
        x=[0, x_axis_val],
        width=[x_axis_val, np.pi - x_axis_val],
        height=0.5,
        bottom=2,
        linewidth=3,
        edgecolor="white",
        color=colors,
        align="edge",
    )
    # for loc, val in zip([0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64, 3.14], values):
    #     zx.annotate(val, xy=(loc, 2.5), ha="right" if val <= 20 else "left")
    arrow = plt.annotate(
        f"{tps_value}",
        xytext=(0, 0),
        xy=(x_axis_val, 2),
        arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
        bbox=dict(
            boxstyle="circle",
            facecolor="black",
            linewidth=2.0,
        ),
        fontsize=45,
        color="white",
        ha="center",
    )
    return gauge, arrow


# fig = plt.figure(figsize=(36, 18))
# ax1 = fig.add_subplot(1, 2, 1, projection="polar")
# ax1 = plot_gauge(ax1, 100, x_axis_val, colors=["white", "green"], title="Rust")
# ax2 = fig.add_subplot(1, 2, 2, projection="polar")
# ax2 = plot_gauge(ax2, 100, x_axis_val, colors=["white", "green"], title="Java")
# plt.savefig(FIGURES_DIRECTORY / "gauge.png")


max_value_gauge = 300
tps_values_java = np.array([1, 50, 100, 60, 60, 60, 60, 60])
x_values_java = np.pi - tps_values_java / max_value_gauge * np.pi
colores_java = [
    ["white", "green"],
    ["white", "green"],
    ["white", "red"],
    ["red", "green"],
    ["red", "green"],
    ["red", "green"],
    ["red", "green"],
    ["red", "green"],
]
tps_values_rust = np.concatenate([np.array([1]), np.arange(5, 230, 5), np.array([220])])
x_values_rust = np.pi - tps_values_rust / max_value_gauge * np.pi
colores_rust = [["white", "green"]] * (tps_values_rust.shape[0] - 2)
colores_rust.append(["white", "red"])
colores_rust.append(["red", "green"])
fig = plt.figure(figsize=(36, 18))
ax1 = fig.add_subplot(projection="polar")
ax1.set_axis_off()
gauge_rust, arrow_rust = plot_gauge(
    ax1,
    f"{tps_values_rust[0]}",
    x_values_rust[0],
    colors=colores_rust[0],
    title="Rust",
)


def animate(i):
    x_axis_val_rust = x_values_rust[i]
    gauge_rust[0].set_width(x_axis_val_rust)
    gauge_rust[0].set_color(colores_rust[i][0])
    gauge_rust[1].set_x(x_axis_val_rust)
    gauge_rust[1].set_width(np.pi - x_axis_val_rust)
    gauge_rust[1].set_color(colores_rust[i][1])
    arrow_rust.set_text(f"{tps_values_rust[i]}")
    arrow_rust.xy = (x_axis_val_rust, 2)
    return gauge_rust, arrow_rust

    # plt.savefig(FIGURES_DIRECTORY / f"gauge_{i:02}.png")
    # plt.close(fig)


ani = animation.FuncAnimation(
    fig,
    animate,
    interval=200,
    blit=False,  # blitting can't be used with Figure artists
    frames=tps_values_rust.shape[0] - 1,
    repeat=False,
)
plt.show()
fig = plt.figure(figsize=(36, 18))
ax1 = fig.add_subplot(projection="polar")
ax1.set_axis_off()
gauge_rust, arrow_rust = plot_gauge(
    ax1,
    f"{tps_values_rust[-1]}",
    x_values_rust[-1],
    colors=colores_rust[-1],
    title="Rust",
)
plt.show()
