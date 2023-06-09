"""
   Script to turn .wdl raw data into .png plots.
"""

import matplotlib.pyplot as plt


class wdldata:
    def __init__(self, prefix, dir=""):
        # Load d data from the file prefix.wdl
        self.prefix = prefix
        self.d = []
        with open(dir + prefix + ".wdl") as f:
            for line in f:
                self.d.append(1000 - int(line.split()[1]))

    def create_graph(self, dir=""):
        dweek = self.d[-168:]
        fig, ax = plt.subplots()
        ax.hist(
            dweek,
            range=(0, 1000),
            bins=100,
            density=True,
            alpha=0.5,
            color="blue",
            edgecolor="black",
            label="last 7 days",
        )
        ax.hist(
            self.d,
            range=(0, 1000),
            bins=100,
            density=True,
            alpha=0.5,
            color="red",
            edgecolor="yellow",
            label="all time",
        )
        ax.legend()
        move, _, ply = self.prefix.partition("m")
        fig.suptitle(f"Distribution of W+L likelihood for 1. {move}")
        ax.set_title(
            f'(WDL data obtained by "stockfish bench 1024 16 28 {self.prefix}.epd depth NNUE" on {"leaf positions" if ply == "" else f"positions {ply} plies from leafs"} in {move}.poll)',
            fontsize=6,
            family="monospace",
        )
        xt = list(range(0, 1001, 200))
        xtl = [str(x // 10) for x in xt]
        mmmm = [min(self.d), max(self.d), min(dweek), max(dweek)]
        for m in mmmm:
            if m not in xt:
                xt.append(m)
                xtl.append(f"{m/10:.1f}")
        ax.set_xticks(xt, xtl)
        plt.setp(
            ax.get_xticklabels()[6:],
            color="darkgray",
            position=(0, -0.03),
            rotation=45,
            ha="right",
            rotation_mode="anchor",
            fontsize=6,
            weight="bold",
        )
        plt.savefig(dir + self.prefix + "wdl.png", dpi=300)


for move in ["g4", "h4", "Na3", "Nh3", "f3"]:
    data = wdldata(move, dir="wdl/")
    data.create_graph(dir="images/")
    data = wdldata(move + "m6", dir="wdl/")
    data.create_graph(dir="images/")
