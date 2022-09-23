import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

from objectes import Indicators

EPSILON_DECAY = 20
SLOPES_DECAY = 0.008

# Create Up vs Down in RSI Indicator 
def CreatUpperDowner():
    df["up"] = np.NaN
    df["down"] = np.NaN
    for i in range(len(df)): 
        if df["RSI"].iloc[i]>73 and df["RSI"].iloc[i]>df["RSI"].iloc[i+1] and df["RSI"].iloc[i]>df["RSI"].iloc[i-1] and df["RSI"].iloc[i]>df["RSI"].iloc[i-2] and df["RSI"].iloc[i]>df["RSI"].iloc[i-3]:
            df["up"].iloc[i] = df["RSI"].iloc[i]
        elif df["RSI"].iloc[i]<30 and df["RSI"].iloc[i]<df["RSI"].iloc[i+1] and df["RSI"].iloc[i]<df["RSI"].iloc[i-1] and df["RSI"].iloc[i]<df["RSI"].iloc[i-2] and df["RSI"].iloc[i]<df["RSI"].iloc[i-3]:
            df["down"].iloc[i] = df["RSI"].iloc[i]

    return df


# Split Up vs Down in RSI Indicator and all subsets from lists
def CalculateSubsetes():
    get_d = []
    for i, val in enumerate(df["down"].notnull()):
        if val:
            get_d.append(i)

    get_u = []
    for i, val in enumerate(df["up"].notnull()):
        if val:
            get_u.append(i)

    sub_d = list(combinations(get_d, 2))
    sub_u = list(combinations(get_u, 2))
    return sub_d, sub_u


# Use lines function that create before
def TrainDataFrame():
    # Get splops and epsilon to remove noises 
    def lines_slops(main_df, point):
        lineـslope = (main_df["RSI"].iloc[point[1]] - main_df["RSI"].iloc[point[0]]) / (point[1] - point[0])
        epsilon = point[1] - point[0]
        return lineـslope, epsilon

    df['Buy'] = np.NaN
    df['Sell'] = np.NaN
    for i in sub_d:
        slopes, epsilon = lines_slops(df, i)
        if slopes>SLOPES_DECAY and epsilon>EPSILON_DECAY:
            if df['RSI'].iloc[i[0]]>df['RSI'].iloc[i[1]] and df['close'].iloc[i[0]]<df['close'].iloc[i[1]]:
                df['Buy'].iloc[i[1]] = df['close'].iloc[i[1]]

    for i in sub_u:
        slopes, epsilon = lines_slops(df, i)
        if slopes>SLOPES_DECAY and epsilon>EPSILON_DECAY:
            if df['RSI'].iloc[i[0]]<df['RSI'].iloc[i[1]] and df['close'].iloc[i[0]]>df['close'].iloc[i[1]]:
                df['Sell'].iloc[i[1]] = df['close'].iloc[i[1]]
    return df


def chandlesPlot(d, o, h, l, c):
    color = []
    for open_p, close_p in zip(o, c):
        if open_p<close_p:
            color.append("g")
        else:
            color.append("r")

    ax.bar(d, height=np.abs(o-c), 
            width=0.8, 
            color=color, 
            bottom=np.min((o, c), axis=0))
    ax.bar(d, height=h-l, width=0.3, color=color, bottom=l)     


df = pd.read_csv("XAUUSD_M30.csv")
df = df[-500:]
df.index = [i for i in range(len(df))]
indicator = Indicators(df["open"], df["low"], df["high"], df["close"])
df["RSI"] = indicator.RSI(periods=14, ema=True)
df = CreatUpperDowner()
sub_d, sub_u = CalculateSubsetes()
df = TrainDataFrame()


fig, (ax, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(32, 20)) 
chandlesPlot(df.index, df["open"], 
             df["high"], df["low"], 
             df["close"])
ax.scatter(df.index, df["Buy"] , color="g", linewidths=11, label="Buy")
ax.scatter(df.index, df["Sell"] , color="r", linewidths=11, label="Sell")
u = [70 for i in range(len(df))]
d = [30 for i in range(len(df))]
ax1.plot(df.index, df.RSI)
ax1.plot(u, linestyle='--')
ax1.plot(d, linestyle='--')
ax1.scatter(df.index, df["up"],linewidths=0.1)
ax1.scatter(df.index, df["down"],linewidths=0.1)
fig.tight_layout()
plt.show()