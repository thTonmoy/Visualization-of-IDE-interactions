import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("../data/test_hbar.csv", header=None)
print(df.head())

updatemenus = [{'type': 'buttons',
                'buttons': [{'label': 'Play',
                             'method': 'animate',
                             'args': [None]}]}]

frame = [{'data': [{'x': [1, 2], 'y': [1, 2]}]},
         {'data': [{'x': [1, 4], 'y': [1, 4]}]},
         {'data': [{'x': [3, 4], 'y': [3, 4]}],
          'layout': {'title': 'End Title'}}]

steps = []
for i in range(0, 3):
    step = dict(
        method='restyle',
        args=['visible', [False] * 3],
    )
    step['args'][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time: "},
    pad={"t": 50},
    steps=steps
)]

l = []

for i in range(2005, 2007):
    l.append(df[df[0] == i][2])
    print(l)
layout = dict(sliders=sliders, updatemenus=updatemenus)

data = [go.Bar(
    visible=False,
    name='𝜈 = ' + str(i),
    x=l[i],
    y=df[1],
    orientation='h',
    marker=dict(
        color=['red', 'green',
               'blue', 'rgba(204,204,204,1)'])
) for i in range(0, 2)]
data[0]['visible'] = True

fig = dict(data=data, layout=layout)

py.plot(fig, filename='horizontal-bar.html')
