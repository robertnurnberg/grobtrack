"""
   Script to turn .poll raw data from cdblib/cdbpvpoll.py into .png plots.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from datetime import datetime


class polldata:
    def __init__(self, prefix):
        # Load eval, depth and PV data from the file prefix.poll
        self.prefix = prefix
        self.date = []  # list of datetime entries
        self.eval = []  # list of cdb evals
        self.depth = []  # list of PV depths
        self.pvs = []
        with open(prefix + ".poll") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) < 4:
                        continue
                    self.date.append(datetime.fromisoformat(parts[0][:-1]))
                    self.eval.append(int(parts[1][:-2]))
                    self.depth.append(len(parts) - 3)
                    self.pvs.append(parts[3:])

    def showdata(self):
        print("prefix = ", self.prefix)
        print("date: ", self.date)
        print("eval: ", self.eval)
        print("depth: ", self.depth)
        print("pvs: ", self.pvs)

    def create_graph(self, length=4, cmapName="tab20b"):
        """
        Create a plot of eval and depth over time, distinguishing different PVs
        by using different colours. PVs are truncated to length to keep the
        number of unique PVs under control.
        Output: prefix.png file with the plot
        """
        col_id = []  # list of colour ids to use for eval data points
        pv_color = {}  # dict that stores the color id used for each unique PV
        number_of_colors = 0  # number of different PVs => colours needed
        for pv in self.pvs:
            pvString = " ".join(m for m in pv[:length])
            if pvString not in pv_color:
                pv_color[pvString] = number_of_colors
                number_of_colors += 1
            col_id.append(pv_color[pvString])

        fig, ax1 = plt.subplots()
        evalColor, dateColor, depthColor = "black", "black", "gray"
        if len(self.date) >= 400:
            evalDotSize = 10
            evalLineWidth, deptLineWidth = 0.5, 0.25
        elif len(self.date) >= 200:
            evalDotSize = 20
            evalLineWidth, deptLineWidth = 1, 0.5
        else:
            evalDotSize = 40
            evalLineWidth, deptLineWidth = 2, 1
        ax1.set_ylabel("eval", color=evalColor)
        cmap = cm.get_cmap(cmapName, number_of_colors)
        scat = ax1.scatter(self.date, self.eval, c=col_id, s=evalDotSize, cmap=cmap)
        ax1.plot(self.date, self.eval, color=dateColor, linewidth=evalLineWidth)
        ax1.tick_params(axis="y", labelcolor=evalColor)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%y"))
        plt.setp(
            ax1.get_xticklabels(),
            rotation=45,
            ha="right",
            rotation_mode="anchor",
            fontsize=7,
        )
        ax2 = ax1.twinx()
        ax2.set_ylabel("depth", color=depthColor)
        ax2.plot(
            self.date,
            self.depth,
            color=depthColor,
            linestyle="dashed",
            linewidth=deptLineWidth,
        )
        ax2.tick_params(axis="y", labelcolor=depthColor)

        for i, pvString in enumerate(sorted(pv_color)):
            top, stepsize, left = 1.12, 0.025, 0
            if length >= 25:
                left = -0.15
            elif length >= 22:
                left = -0.1
            ax1.text(
                left,
                top - stepsize * i,
                pvString,
                color=cmap(pv_color[pvString]),
                transform=ax1.transAxes,
                fontsize=6,
                family="monospace",
                weight="bold",
            )

        plt.savefig(self.prefix + ".png", dpi=300)


for move in [("g4", 2), ("h4", 8), ("Na3", 16), ("Nh3", 4), ("f3", 12)]:
    data = polldata(move[0])
    data.create_graph(move[1])
