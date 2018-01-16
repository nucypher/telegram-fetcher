#!/usr/bin/env python3

import os
import sys
import json
from datetime import datetime

names = [f for f in os.listdir() if f.endswith('.json')]
times = [datetime.fromtimestamp(os.path.getmtime(f)) for f in names]

name = max(zip(times, names))[1]

with open(name) as f:
    data = json.load(f)
    for i, l in enumerate(data):
        if l['username'] and l['username'].startswith(sys.argv[1]):
            print(i, l)
