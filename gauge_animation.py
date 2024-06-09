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
    arrow = ax.annotate(
        f"{tps_value}",
        xytext=(0, 0),
        xy=(x_axis_val, 2),
        arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="white", shrinkA=0),
        bbox=dict(
            boxstyle="circle",
            facecolor="white",
            linewidth=0.1,
        ),
        fontsize=45,
        color="black",
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
n_frames_initial_delay, n_frames_delay_1, n_frames_delay_2 = 20, 5, 20
tps_values_java = np.concatenate(
    [
        np.array([1] * n_frames_initial_delay),
        np.arange(5, 70, 5),
        np.arange(64, 59, -1),  # tiene que tener longitud n_frames_delay_1
        np.repeat(60, n_frames_delay_2),
    ]
)
x_values_java = np.pi - tps_values_java / max_value_gauge * np.pi
colores_java = [["white", "green"]] * (
    tps_values_java.shape[0] - (n_frames_delay_1 + n_frames_delay_2)
)
colores_java.extend([["white", "red"]] * n_frames_delay_1)
colores_java.extend([["red", "green"]] * n_frames_delay_2)
tps_values_rust = np.concatenate(
    [
        np.array([1]),
        np.arange(5, 230, 5),
        np.arange(224, 219, -1),
        np.repeat(220, n_frames_delay_2),
    ]
)
x_values_rust = np.pi - tps_values_rust / max_value_gauge * np.pi
colores_rust = [["white", "green"]] * (
    tps_values_rust.shape[0] - (6 + n_frames_delay_2)
)
colores_rust.extend([["white", "red"]] * 5)
colores_rust.extend([["red", "green"]] * (1 + n_frames_delay_2))
plt.pause(3)
fig = plt.figure(figsize=(36, 18))
ax1 = fig.add_subplot(1, 2, 1, projection="polar")
ax1.set_axis_off()
ax1.set_title(
    "Java", loc="center", pad=20, fontsize=35, fontweight="bold", color="white"
)
ax2 = fig.add_subplot(1, 2, 2, projection="polar")
ax2.set_axis_off()
ax2.set_title(
    "Rust",
    loc="center",
    pad=20,
    fontsize=35,
    fontweight="bold",
    color="white",
)
# turn off axis spines
ax1.xaxis.set_visible(False)
ax1.yaxis.set_visible(False)
ax1.set_frame_on(False)
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)
ax2.set_frame_on(False)
fig.patch.set_facecolor("#202228")
ax1.set_facecolor("#202228")
ax2.set_facecolor("#202228")
fig.tight_layout()
gauge_java, arrow_java = plot_gauge(
    ax1,
    f"{tps_values_java[0]}",
    x_values_java[0],
    colors=colores_java[0],
    title="Java",
)
gauge_rust, arrow_rust = plot_gauge(
    ax2,
    f"{tps_values_rust[0]}",
    x_values_rust[0],
    colors=colores_rust[0],
    title="Rust",
)


def animate(i):
    if i < tps_values_java.shape[0]:
        x_axis_val_java = x_values_java[i]
        gauge_java[0].set_width(x_axis_val_java)
        gauge_java[0].set_color(colores_java[i][0])
        gauge_java[1].set_x(x_axis_val_java)
        gauge_java[1].set_width(np.pi - x_axis_val_java)
        gauge_java[1].set_color(colores_java[i][1])
        arrow_java.set_text(f"{tps_values_java[i]}")
        arrow_java.xy = (x_axis_val_java, 2)
    else:
        j = i - tps_values_java.shape[0]
        x_axis_val_rust = x_values_rust[j]
        gauge_rust[0].set_width(x_axis_val_rust)
        gauge_rust[0].set_color(colores_rust[j][0])
        gauge_rust[1].set_x(x_axis_val_rust)
        gauge_rust[1].set_width(np.pi - x_axis_val_rust)
        gauge_rust[1].set_color(colores_rust[j][1])
        arrow_rust.set_text(f"{tps_values_rust[j]}")
        arrow_rust.xy = (x_axis_val_rust, 2)
    return gauge_java, arrow_java, gauge_rust, arrow_rust

    # plt.savefig(FIGURES_DIRECTORY / f"gauge_{i:02}.png")
    # plt.close(fig)


total_frames = tps_values_java.shape[0] + tps_values_rust.shape[0]

ani = animation.FuncAnimation(
    fig,
    animate,
    interval=100,
    blit=False,  # blitting can't be used with Figure artists
    # frames=frame_gen,
    frames=total_frames,
    repeat=False,
)
plt.show()

# with open("embed_video_code.html", "w") as f:
#     print(ani.to_html5_video(), file=f)
