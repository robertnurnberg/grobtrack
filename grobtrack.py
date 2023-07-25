"""
   Script to turn .poll raw data from cdblib/cdbpvpoll.py into .png plots.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.ticker import MaxNLocator
from datetime import datetime


class polldata:
    def __init__(self, move):
        # Load eval, depth and PV data from the file move.poll
        self.move = move
        self.date = []  # list of datetime entries
        self.eval = []  # list of cdb evals
        self.pvs = []  # list of PVs themselves
        with open(move + ".poll") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) < 4 or "error" in line:
                        continue
                    self.date.append(datetime.fromisoformat(parts[0][:-1]))
                    self.eval.append(int(parts[1][:-2]))
                    self.pvs.append(parts[3:])

    def showdata(self):
        print("move = ", self.move)
        print("date: ", self.date)
        print("eval: ", self.eval)
        print("pvs: ", self.pvs)

    def find_uniquePVs(self, plotStart=0, pvLength=4):
        # count number of unique PVs when truncated to pvLength
        self.plotStart = plotStart  # index to start plot from
        self.pvLength = pvLength  # length of truncated PVs
        self.uniquePVs = set()
        for pv in self.pvs[self.plotStart :]:
            pvString = " ".join(m for m in pv[: self.pvLength])
            if pvString not in self.uniquePVs:
                self.uniquePVs.add(pvString)

    def find_optimal_pvLength(self, plotStart=0, pvLength=25):
        # find optimal pvLength to still fit all unique PV strings on screen
        while pvLength > 0:
            self.find_uniquePVs(plotStart=plotStart, pvLength=pvLength)
            if len(self.uniquePVs) <= 5 or len(self.uniquePVs) <= 10 and pvLength <= 12:
                break
            pvLength -= 1

    def create_graph(self, dir="", suffix="", cmapName="tab20b"):
        # plotdata from plotStart, using numberOfColors for truncated PVs
        date = self.date[self.plotStart :]
        eval = self.eval[self.plotStart :]
        depth = []  # list of PV depths
        pvColor = {}  # dict that stores the color id used for each unique PV
        for i, pvString in enumerate(sorted(self.uniquePVs)):
            pvColor[pvString] = i  # assign color id in alphabetical order
        colorId = []  # list of color ids to use for eval data points
        for pv in self.pvs[self.plotStart :]:
            pvString = " ".join(m for m in pv[: self.pvLength])
            colorId.append(pvColor[pvString])
            depth.append(len(pv))

        fig, ax1 = plt.subplots()
        evalColor, depthColor, alpha = "black", "gray", 1
        if len(date) >= 1100:
            evalDotSize, depthDotSize, alpha = 2, 0.5, 0.5
            evalLineWidth, deptLineWidth = 0, 0
        elif len(date) >= 800:
            evalDotSize, depthDotSize = 3, 1
            evalLineWidth, deptLineWidth = 0.1, 0
        elif len(date) >= 600:
            evalDotSize, depthDotSize = 5, 1
            evalLineWidth, deptLineWidth = 0.25, 0
        elif len(date) >= 400:
            evalDotSize = 10
            evalLineWidth, deptLineWidth = 0.5, 0.25
        elif len(date) >= 200:
            evalDotSize = 20
            evalLineWidth, deptLineWidth = 1, 0.5
        else:
            evalDotSize = 40
            evalLineWidth, deptLineWidth = 1.5, 0.75
        ax1.set_ylabel("eval", color=evalColor)
        cmap = cm.get_cmap(cmapName, len(self.uniquePVs))
        scat = ax1.scatter(date, eval, c=colorId, s=evalDotSize, cmap=cmap, alpha=alpha)
        ax1.grid(alpha=0.4, linewidth=0.5)
        if evalLineWidth:
            ax1.plot(date, eval, color=evalColor, linewidth=evalLineWidth)
        ax1.tick_params(axis="y", labelcolor=evalColor)
        # hack to avoid fractional y ticks
        if min(eval) == max(eval):
            ax1.set_ylim([eval[0] - 1.1, eval[0] + 1.1])
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.setp(
            ax1.get_xticklabels(),
            rotation=45,
            ha="right",
            rotation_mode="anchor",
            fontsize=6,
        )
        ax2 = ax1.twinx()
        ax2.set_ylabel("depth", color=depthColor)
        if deptLineWidth:
            ax2.plot(
                date,
                depth,
                color=depthColor,
                linestyle="dashed",
                linewidth=deptLineWidth,
            )
        else:
            ax2.scatter(date, depth, color=depthColor, s=depthDotSize, linewidths=0)
        ax2.tick_params(axis="y", labelcolor=depthColor, colors=depthColor)
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

        pvFontSize, moveWidth, maxLines = 6, 0.05, 5
        top, stepsize, left, right = 1.12, 0.025, 0, 1.002
        if self.pvLength >= 13:
            pvMaxDisplay = maxLines  # maximal number of PVs we can show above plot
        else:
            pvMaxDisplay = 2 * maxLines
        textLength = (
            self.pvLength if len(self.uniquePVs) <= maxLines else 2 * self.pvLength + 1
        )
        if textLength > 20:
            if textLength >= 25:  # maximum to fit on screen with current font size
                textLength = 25
            left -= 0.55 * moveWidth * (textLength - 20)
            right += 0.5 * moveWidth * (textLength - 20)

        for i, pvString in enumerate(sorted(self.uniquePVs)[:pvMaxDisplay]):
            ax1.text(
                left if i <= 4 else right - moveWidth * self.pvLength,
                top - stepsize * (i % maxLines),
                pvString,
                color=cmap(pvColor[pvString]),
                transform=ax1.transAxes,
                fontsize=pvFontSize,
                family="monospace",
                weight="bold",
            )

        ax1.plot([], [], " ", label=f"1. {self.move}")
        loc = "lower left" if self.move == "g4" else "best"
        ax1.legend(handletextpad=0, handlelength=0, loc=loc)
        plt.savefig(dir + self.move + suffix + ".png", dpi=300)


for move in ["g4", "h4", "Na3", "Nh3", "f3"]:
    data = polldata(move)
    data.find_optimal_pvLength()
    data.create_graph(dir="images/")
    data.find_optimal_pvLength(plotStart=-168)
    data.create_graph(dir="images/", suffix="week")
    data.find_optimal_pvLength(plotStart=-24)
    data.create_graph(dir="images/", suffix="day")
