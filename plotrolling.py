"""
   Script to turn .poll and wdl/.wdl data into rolling average .png plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
from datetime import datetime


def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, "same")


class polldata:
    def __init__(self, move, wdldir="wdl/"):
        # Load eval and depth data from the file move.poll
        self.move = move
        self.date = []  # list of datetime entries
        self.eval = []  # list of cdb evals
        self.depth = []  # list of PV depths
        with open(move + ".poll") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) < 4 or "error" in line:
                        continue
                    self.date.append(datetime.fromisoformat(parts[0][:-1]))
                    self.eval.append(int(parts[1][:-2]))
                    self.depth.append(len(parts[3:]))

        self.wl = []  # list of W+L values at leafs
        with open(wdldir + move + ".wdl") as f:
            for line in f:
                self.wl.append(1000 - int(line.split()[1]))

        self.wlm6 = []  # list of W+L values at leafs minus 6 plies
        with open(wdldir + move + "m6.wdl") as f:
            for line in f:
                self.wlm6.append(1000 - int(line.split()[1]))

    def create_graph(self, dir="", suffix=""):
        rollingWidth = 168  # window size to be averaged is 168h = 1week

        date = self.date[rollingWidth // 2 : -rollingWidth // 2]
        eval = movingaverage(self.eval, rollingWidth)[
            rollingWidth // 2 : -rollingWidth // 2
        ]
        depth = movingaverage(self.depth, rollingWidth)[
            rollingWidth // 2 : -rollingWidth // 2
        ]
        wl = (
            movingaverage(self.wl, rollingWidth)[rollingWidth // 2 : -rollingWidth // 2]
            / 10
        )
        wlm6 = (
            movingaverage(self.wlm6, rollingWidth)[
                rollingWidth // 2 : -rollingWidth // 2
            ]
            / 10
        )

        fig, ax1 = plt.subplots()
        evalColor, depthColor = "black", "gray"
        wlColor, wlm6Color = "lightpink", "tab:red"
        deptLineWidth = 0.5
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.setp(
            ax1.get_xticklabels(),
            rotation=45,
            ha="right",
            rotation_mode="anchor",
            fontsize=6,
        )
        ax1.set_ylabel("W+L (%)", color=wlm6Color)
        ax1.tick_params(axis="y", colors=wlm6Color)
        ax1.plot(
            date,
            wl,
            color=wlColor,
            label="SF's W+L at leafs",
        )
        ax1.plot(
            date,
            wlm6,
            color=wlm6Color,
            label="SF's W+L at leafs minus 6 plies",
        )
        ax1.legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.13))
        ax2 = ax1.twinx()
        ax2.plot(date, eval, color=evalColor)
        ax2.tick_params(axis="y", labelcolor=evalColor)
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax2.plot([], [], " ", label=f"1. {self.move}")
        ax2.legend(handletextpad=0, handlelength=0)
        ybox1 = TextArea(
            "cdb's eval",
            textprops=dict(
                size=9, color=evalColor, rotation=90, ha="left", va="bottom"
            ),
        )
        ybox2 = TextArea(
            "(and depth)",
            textprops=dict(
                size=6, color=depthColor, rotation=90, ha="left", va="bottom"
            ),
        )

        ybox = VPacker(children=[ybox2, ybox1], align="center", pad=0, sep=5)
        anchored_ybox = AnchoredOffsetbox(
            loc=8,
            child=ybox,
            pad=0.0,
            frameon=False,
            bbox_to_anchor=(1.1, 0.4),
            bbox_transform=ax2.transAxes,
            borderpad=0.0,
        )
        ax2.add_artist(anchored_ybox)
        ax3 = ax1.twinx()
        ax3.plot(
            date,
            depth,
            color=depthColor,
            linestyle="dashed",
            linewidth=deptLineWidth,
        )
        t = [int(min(depth)), int(max(depth)) + 1]
        ax3.set_yticks(t, t)
        plt.setp(
            ax3.get_yticklabels(),
            position=(1.06, 0),
            fontsize=6,
            color=depthColor,
        )
        plt.setp(
            ax3.get_yticklines(),
            color=depthColor,
            markersize=24,
            markeredgewidth=0.1,
        )
        # ax3.tick_params(axis="y", labelcolor=depthColor)
        plt.savefig(dir + self.move + "rolling.png", dpi=300)


for move in ["g4", "h4", "Na3", "Nh3", "f3"]:
    data = polldata(move)
    data.create_graph(dir="images/")
