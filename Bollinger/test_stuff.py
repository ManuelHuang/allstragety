from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader.analyzers as btanalyzers
import datetime, time
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
import backtrader as bt



i = 00
if i in range(0,60,5):
    print(i)