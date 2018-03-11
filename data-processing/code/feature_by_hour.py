import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


def make_dataframe(file_path: str):
    data = pd.read_csv(file_path, header=0)
    # print(data.head())
    # print(data.describe())
    # freq_series = data.groupby([data['hour']])['event'].value_counts()
    # print(freq_series)
    # print(data.groupby([data['hour'], 'event'])['duration'].sum())
    # print(type(summary_df))
    df = data.groupby([data['hour'], 'event']).agg({'duration': sum,
                                                    'event': "count"})
    df.rename({'event': 'frequency'}, axis='columns', inplace=True)
    return df


def write_dataframe_to_csv(df: pd.DataFrame, output_path: str):
    df.to_csv(path_or_buf=output_path)


def make_plot(df: pd.DataFrame):
    steps = []
    for i in range(0, 24):
        step = dict(
            method='restyle',
            label=str(i) + ":00- " + str(i+1) + ":00",
            args=['visible', [False] * 24],
        )
        step['args'][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Time: "},
        transition={'duration': 300, 'easing': 'cubic-in-out'},
        pad={"t": 50},
        steps=steps
    )]

    lx = []
    # ly = ['VersionControlEvent', 'ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
    #       'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
    #       'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
    #       'TestRunEvent', 'FindEvent']
    ly = ['ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
          'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
          'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
          'TestRunEvent', 'FindEvent']


    for i in range(0, 24):
        temp = df.loc[[i]]
        temp.reset_index(level='event', inplace=True)
        lx.append(temp['frequency'][1:])

    #layout = dict(sliders=sliders)

    layout = go.Layout(
        title='IDE Events by time of day',
        yaxis=dict(
            title='Frequency',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        sliders = sliders
    )

    data = [go.Bar(
        visible=False,
        name= str(i) + ":00-" + str(i+1) + ":00",
        y=lx[i],
        x = ly,
        #x=np.arange(0, 15, 1),
        #orientation='h',
        # marker=dict(
        #     color=['red', 'green',
        #            'blue', 'rgba(204,204,204,1)'])
    ) for i in range(0, 24)]
    data[0]['visible'] = True

    fig = dict(data=data, layout=layout)

    py.plot(fig, filename='bar_chart.html')
    return


def main():
    file_path = "../data/test_events_h.csv"
    make_plot(make_dataframe(file_path))


if __name__ == "__main__":
    main()
