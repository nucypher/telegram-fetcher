#!/usr/bin/env python3

import json
import os
import pylab
from datetime import datetime
import numpy as np
import matplotlib.dates as mdates


def load():
    names = [f for f in os.listdir() if f.endswith('.json')]
    times = [datetime.fromtimestamp(os.path.getmtime(f)) for f in names]
    N = []
    for name in names:
        with open(name) as f:
            N.append(len(json.load(f)))
    times = np.array(times)
    N = np.array(N)
    order = times.argsort()
    return times[order], N[order]


if __name__ == '__main__':
    fmt = mdates.DateFormatter('%m/%d %H:%M')
    ax = pylab.axes()
    ax.xaxis.set_major_formatter(fmt)
    pylab.title('NuCypher KMS')
    times, N = load()
    pylab.plot(times, N, marker='o', linewidth=2)
    pylab.xlabel('Date')
    pylab.ylabel('Telegram users')
    pylab.show()
