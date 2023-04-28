"""
   Script to turn .poll raw data from cdblib/cdbpvpoll.py into .png plots.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from datetime import datetime


def create_graph(prefix, length=4, cmap_name="tab20b"):
    """
    Create a plot of eval and depth for a given position on cdb over time
    Input: prefix: filename of the stored polling data is prefix.poll
           length: allowed number of plies when trying to find unique PVs
    Output: prefix.png file with the plot
    """
    date = []  # list of datetime entries
    eval = []  # list of cdb evals
    depth = []  # list of PV depths
    col = []  # list of colours to use for eval data points
    pv_color = {}  # dict that store the colour used for each unique PV
    number_of_colors = 0  # number of different PVs => colours needed
    with open(prefix + ".poll") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) < 4:
                    continue
                date.append(datetime.fromisoformat(parts[0][:-1]))
                eval.append(int(parts[1][:-2]))
                depth.append(len(parts) - 3)
                pv_moves = " ".join(m for m in parts[3 : 3 + length])
                if pv_moves not in pv_color:
                    pv_color[pv_moves] = number_of_colors
                    number_of_colors += 1
                col.append(pv_color[pv_moves])

    fig, ax1 = plt.subplots()
    color = "black"
    ax1.set_ylabel("eval", color=color)
    cmap = cm.get_cmap(cmap_name, number_of_colors)
    scat = ax1.scatter(date, eval, c=col, s=40, cmap=cmap)
    ax1.plot(date, eval, color=color, linewidth=2)
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor", fontsize=7)
    ax2 = ax1.twinx()
    color = "gray"
    ax2.set_ylabel("depth", color=color)
    ax2.plot(date, depth, color=color, linestyle="dashed", linewidth=1)
    ax2.tick_params(axis="y", labelcolor=color)

    for i, pv in enumerate(sorted(pv_color)):
        top, stepsize, left = 1.12, 0.025, 0
        if length >= 25: left = -0.15
        elif length >= 22: left = -0.1
        ax1.text(
            left,
            top - stepsize * i,
            pv,
            color=cmap(pv_color[pv]),
            transform=ax1.transAxes,
            fontsize=6,
            family="monospace",
            weight="bold",
        )

    plt.savefig(prefix + ".png", dpi=300)


for move in [("g4",3), ("h4",8), ("Na3",18), ("Nh3",4), ("f3",20)]:
    create_graph(*move) # , cmap_name="turbo")
