import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

def plot_with_plotly(df):
    trace1 = go.Bar(
        x=df['start'],
        y=df['size'],
        name='Size'
    )
    trace2 = go.Bar(
        x=df['start'],
        y=df['location'],
        name='Location'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        yaxis=dict(
            range=[0, 1000]
        )
    )

    fig = dict(data=data, layout=layout)
    py.plot(fig, filename="stacked-bar.html")
    return


def plot_with_matplotlib(df):
    df.set_index('start', inplace=True)
    plt.figure()
    print(df.head())
    df.plot(kind= "line")
    # plt.plot(df['location'], '-', linewidth=1)
    # plt.plot(df['size'], '-', linewidth=1)
    plt.show()
    return


df = pd.read_csv("../data/transformed_data_2016-05-09_edit.csv",
                   header=0,
                   usecols=['start', 'duration', 'location', 'size'],
                   parse_dates=['start'],
                   date_parser=lambda epoch: pd.to_datetime(epoch, unit='s'))

plot_with_matplotlib(df= df[['start', 'location']][2000:9000])
