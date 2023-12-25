import matplotlib.pyplot as plt
import numpy as np
from time import sleep

class ScatterPlot:
    margin = 0.05
    def __init__(self, xlabel, ylabel, title) -> None:
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.x, self.y = [0], [0]
        self.sc = self.ax.scatter(self.x, self.y)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        # self.ax.set_xlim([0, 10])
        # self.ax.set_ylim([0, 10])
        plt.draw()

    def add_point(self, x, y, render, pause=0.0001):
        self.x.append(x)
        self.y.append(y)
        if not render: return
        self.update(pause)
    
    def update(self, pause=0.0001):
        ax = plt.gca()
        xmin, xmax = min(self.x), max(self.x)
        ymin, ymax = min(self.y), max(self.y)
        dx, dy = (xmax - xmin) * self.margin, (ymax - ymin) * self.margin
        ax.set_xlim([xmin - dx, xmax + dx])
        ax.set_ylim([ymin - dy, ymax + dy])
        self.sc.set_offsets(np.c_[self.x, self.y])
        self.fig.canvas.draw_idle()
        plt.pause(pause)

    def freeze(self):
        plt.waitforbuttonpress()

    def stats(self):
        y = np.array(self.y)
        return np.round(np.mean(y), 2), np.round(np.std(y), 2), np.max(y)

if __name__ == '__main__':
    plot = ScatterPlot("Test", "X-axis", "Y-axis")
    for i in range(1000):
        plot.add_point(i, i)
        sleep(0.01)