import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("data/test_events3.csv", header=0, usecols=['event', 'start', 'duration'], parse_dates=[1], date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))
print(data)
#print (data.groupby([data['start'].dt.hour, 'event'])['duration'].sum().unstack()
data.groupby([data['start'].dt.hour, 'event'])['duration'].sum().to_csv("out/d3_dur.csv")
data.groupby([data['start'].dt.hour])['event'].value_counts().to_csv("out/d3_freq.csv")
