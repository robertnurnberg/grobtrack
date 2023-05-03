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
                    if len(parts) < 4 or "error" in line:
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

    def create_graph_data(self, plotStart=0, pvLength=4):
        """
        Prepare (color) data needed for plots, distinguishing different PVs
        by using different colors. PVs are truncated to pvLength to keep the
        number of unique PVs under control. Return number of colors needed.
        """
        self.plotStart = plotStart  # index to start plot from
        self.pvLength = pvLength  # length of truncated PVs
        self.colorId = []  # list of color ids to use for eval data points
        self.pvColor = {}  # dict that stores the color id used for each unique PV
        numberOfColors = 0  # number of different PVs => colors needed
        for pv in self.pvs[self.plotStart :]:
            pvString = " ".join(m for m in pv[:pvLength])
            if pvString not in self.pvColor:
                self.pvColor[pvString] = numberOfColors
                numberOfColors += 1
            self.colorId.append(self.pvColor[pvString])

    def create_optimal_graph_data(self, plotStart=0, pvLength=25):
        # find optimal pvLength to still fit all unique PV strings on screen
        while pvLength > 0:
            self.create_graph_data(plotStart=plotStart, pvLength=pvLength)
            if len(self.pvColor) <= 5 or len(self.pvColor) <= 10 and pvLength <= 12:
                break
            pvLength -= 1

    def create_graph(self, dir="", suffix="", cmapName="tab20b"):
        # plot current graph data and save to file prefix.png
        date = self.date[self.plotStart :]
        eval = self.eval[self.plotStart :]
        depth = self.depth[self.plotStart :]
        fig, ax1 = plt.subplots()
        evalColor, dateColor, depthColor = "black", "black", "gray"
        if len(date) >= 400:
            evalDotSize = 10
            evalLineWidth, deptLineWidth = 0.5, 0.25
        elif len(date) >= 200:
            evalDotSize = 20
            evalLineWidth, deptLineWidth = 1, 0.5
        else:
            evalDotSize = 30
            evalLineWidth, deptLineWidth = 1.5, 0.75
        ax1.set_ylabel("eval", color=evalColor)
        cmap = cm.get_cmap(cmapName, len(self.pvColor))
        scat = ax1.scatter(date, eval, c=self.colorId, s=evalDotSize, cmap=cmap)
        ax1.plot(date, eval, color=dateColor, linewidth=evalLineWidth)
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
            date,
            depth,
            color=depthColor,
            linestyle="dashed",
            linewidth=deptLineWidth,
        )
        ax2.tick_params(axis="y", labelcolor=depthColor)

        pvFontSize, moveWidth, maxLines = 6, 0.049, 5
        top, stepsize, left, right = 1.12, 0.025, 0, 1
        if self.pvLength >= 13:
            pvMaxDisplay = maxLines  # maximal number of PVs we can show above plot
        else:
            pvMaxDisplay = 2 * maxLines
        textLength = (
            self.pvLength if len(self.pvColor) <= maxLines else 2 * self.pvLength + 1
        )
        textLength = min(
            textLength, 25
        )  # maximum to fit on screen with current font size
        if textLength > 20:
            offset = 0.55 * moveWidth * (textLength - 20)
            left -= offset
            right += offset

        for i, pvString in enumerate(sorted(self.pvColor)[:pvMaxDisplay]):
            ax1.text(
                left if i <= 4 else right - moveWidth * self.pvLength,
                top - stepsize * (i % maxLines),
                pvString,
                color=cmap(self.pvColor[pvString]),
                transform=ax1.transAxes,
                fontsize=pvFontSize,
                family="monospace",
                weight="bold",
            )

        plt.savefig(dir + self.prefix + suffix + ".png", dpi=300)


for move in ["g4", "h4", "Na3", "Nh3", "f3"]:
    data = polldata(move)
    data.create_optimal_graph_data()
    data.create_graph(dir="images/")
    data.create_optimal_graph_data(plotStart=-168)
    data.create_graph(dir="images/", suffix="week")
    data.create_optimal_graph_data(plotStart=-24)
    data.create_graph(dir="images/", suffix="day")
