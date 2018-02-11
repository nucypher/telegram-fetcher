#!/usr/bin/env python3

import json
import pylab
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates

list_name = 'nucypher_telegram.json'
date_format = r"%Y-%m-%dT%H:%M:%S"
dates = []
users = set()
n_points = 1000


with open(list_name) as f:
    current_list = json.load(f)

for d, u in current_list:
    users.add(u['id'])
    dates.append(datetime.strptime(d, date_format))

L = len(dates)
print('Total users:', L)

dates = np.array(sorted(dates), dtype='M8[us]')
dt = (dates[-1] - dates[0]) // n_points
X = np.arange(dates[0], dates[-1] + dt, dt)
Y = np.array([(dates <= x).sum() for x in X])

fmt = mdates.DateFormatter('%m/%d')
ax = pylab.axes()
ax.xaxis.set_major_formatter(fmt)
pylab.title('NuCypher KMS')
# pylab.semilogy(X.astype(datetime), Y, linewidth=2)
pylab.plot(X.astype(datetime), Y, linewidth=2)
pylab.xlabel('Date')
pylab.ylabel('Telegram users')
pylab.show()
