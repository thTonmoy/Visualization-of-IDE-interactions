# from plotly.offline import init_notebook_mode, plot
import numpy as np
import pandas as pd
#
#
# dataset = pd.read_csv('out/d2_combined.csv')
# data2 = [dict()]
# data = [dict(
#         visible = False,
#         line=dict(color='00CED1', width=6),
#         name = '𝜈 = '+str(step),
#         x = np.arange(0,10,0.01),
#         y = np.sin(step*np.arange(0,10,0.01))) for step in np.arange(0,5,0.1)]
# data[10]['visible'] = True
#
# steps = []
# for i in range(len(data)):
#     step = dict(
#         method = 'restyle',
#         args = ['visible', [False] * len(data)],
#     )
#     step['args'][1][i] = True # Toggle i'th trace to "visible"
#     steps.append(step)
#
# sliders = [dict(
#     active = 10,
#     currentvalue = {"prefix": "Frequency: "},
#     pad = {"t": 50},
#     steps = steps
# )]
#
# layout = dict(sliders=sliders)
#

# fig = dict(data=data, layout=layout)
# file = open("testfile22.txt", "w")
#
# file.write(plot(fig, include_plotlyjs=False, output_type='div'))
# file.close()
#
# #py.iplot(fig, filename='Sine Wave Slider')

from plotly.offline import plot
import plotly.graph_objs as go

dataset = pd.read_csv('out/d2_combined.csv')
x = []
y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 1]
for i in range(14):
    x.append(i)

print(x)
print(y)

# trace0 = go.Bar(
#     x=['Feature A', 'Feature B', 'Feature C',
#        'Feature D', 'Feature E'],
#     y=[20, 14, 23, 25, 22]
# )

trace0 = go.Bar(
    x=x,
    y=y
)
data = [trace0]

data = [dict(
        visible = False,
        name = '𝜈 = '+str(step),
        x = np.arange(0,10,0.01),
        y = np.sin(step*np.arange(0,10,0.01))) for step in np.arange(0,5,0.1)]
data[10]['visible'] = True

steps = []
for i in range(0,24):
    step = dict(
        method = 'restyle',
        args = ['visible', [False] * 24],
    )
    step['args'][1][i] = True # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active = 10,
    currentvalue = {"prefix": "Frequency: "},
    pad = {"t": 50},
    steps = steps
)]

layout = go.Layout(
    title='Least Used Feature',
    sliders = sliders
)

fig = go.Figure(data=data, layout=layout)
plot(fig, filename='color-bar.html')
