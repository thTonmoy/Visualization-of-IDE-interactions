from plotly.offline import init_notebook_mode, plot
from IPython.display import display, HTML

import pandas as pd

init_notebook_mode(connected=True)

url = 'out/d2_combined.csv'
dataset = pd.read_csv(url)

years = list(range(0, 24))
# make list of continents
times = []
for time in dataset['time']:
     if time not in times:
         times.append(time)
# make figure
figure = {
    'data': [],
    'layout': {},
    'frames': []
}

# fill in most of layout
figure['layout']['xaxis'] = {'range': [0, 23], 'title': 'Time of Day'}
figure['layout']['yaxis'] = {'title': 'Frequency'}
figure['layout']['hovermode'] = 'closest'
figure['layout']['sliders'] = {
    'args': [
        'transition', {
            'duration': 400,
            'easing': 'cubic-in-out'
        }
    ],
    'initialValue': '0',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}
figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                                  'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 300, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}

# make data
year = 0
for time in times:
    dataset_by_year = dataset[dataset['event'] == year]
    dataset_by_year_and_cont = dataset_by_year[dataset_by_year['event'] == event]

    data_dict = {
        'x': list(dataset_by_year_and_cont['frequency']),
        'y': list(dataset_by_year_and_cont['event']),
        'mode': 'markers',
        #'text': list(dataset_by_year_and_cont['country']),
        'marker': {
            'sizemode': 'area',
            'sizeref': 200000,
            'size': 100
        },
        'name': event
    }
    figure['data'].append(data_dict)

# make frames
for year in years:
    frame = {'data': [], 'name': str(year)}
    for event in events:
        dataset_by_year = dataset[dataset['time'] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[dataset_by_year['event'] == event]

        data_dict = {
            'x': list(dataset_by_year_and_cont['frequency']),
            'y': list(dataset_by_year_and_cont['event']),
            'mode': 'markers',
            #'text': list(dataset_by_year_and_cont['country']),
            'marker': {
                'sizemode': 'area',
                'sizeref': 200000,
                'size': 100
            },
            'name': event
        }
        frame['data'].append(data_dict)

    figure['frames'].append(frame)
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
         'transition': {'duration': 300}}
    ],
        'label': year,
        'method': 'animate'}
    sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]

#plotly.offline.plot(data, include_plotlyjs=False, output_type='div')
#plot(figure, include_plotlyjs=False, output_type='div')
plot(figure, filename='file.html')