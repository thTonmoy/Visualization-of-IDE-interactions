import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.style as mpl_style
import matplotlib.pyplot as plt
import os


def make_dataframe(file_path: str):
    data = pd.read_csv(file_path, header=0)
    df = data.groupby([data['hour'], 'event']).agg({'duration': sum,
                                                    'event': "count"})
    df.rename({'event': 'frequency'}, axis='columns', inplace=True)
    return df


def write_dataframe_to_csv(df: pd.DataFrame, output_path: str):
    df.to_csv(path_or_buf=output_path)


def load_dataframe(file_path: str):
    return pd.read_csv(file_path, index_col=0)


def create_steps_for_slider():
    steps = []
    for i in range(0, 24):
        step = dict(
            method='restyle',
            label=str(i) + ":00- " + str(i + 1) + ":00",
            args=['visible', [False] * 24],
        )
        step['args'][1][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)
    return steps


def create_slider_for_plot():
    steps = create_steps_for_slider()
    sliders = [dict(
        active=0,
        currentvalue={"prefix": "Time: "},
        transition={'duration': 300, 'easing': 'cubic-in-out'},
        pad={"t": 50},
        steps=steps
    )]
    return sliders


def prepare_data_for_plot(df: pd.DataFrame):
    lx = ['ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
          'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
          'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
          'TestRunEvent', 'FindEvent']
    data = [go.Bar(
        visible=False,
        name=str(i) + ":00-" + str(i + 1) + ":00",
        y=(df.loc[[i]])['frequency'][1:],
        x=lx,
        # x=np.arange(0, 15, 1),
        # orientation='h',
        # marker=dict(
        #     color=['red', 'green',
        #            'blue', 'rgba(204,204,204,1)'])
    ) for i in range(0, 24)]
    data[0]['visible'] = True

    return data


def create_layout_for_plot(sliders, withButton: bool):
    updatemenus = []
    if withButton == True:
        updatemenus = [{'type': 'buttons',
                        'buttons': [{'label': 'Play',
                                     'method': 'animate',
                                     'args': [None]}]}]
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
        sliders=sliders,
        updatemenus=updatemenus
    )
    return layout


def prepare_frames_for_animation(df: pd.DataFrame):
    lx = ['ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
          'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
          'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
          'TestRunEvent', 'FindEvent']
    frame = []
    for i in range(0, 24):
        temp = {'data': [{'x': lx, 'y': df.loc[[i]]['frequency'][1:]}],
                'mode': "lines"}
        frame.append(temp)
    return frame


def make_bar_plot(df: pd.DataFrame):
    sliders = create_slider_for_plot()
    layout = create_layout_for_plot(sliders, True)
    data = prepare_data_for_plot(df)
    frame = prepare_frames_for_animation(df)
    fig = dict(data=data, layout=layout, frames=frame)
    py.plot(fig, filename='bar_chart.html')
    return


def get_bar_chart_div(root_path: str):
    file_path = os.path.join(root_path, "data", "fbh.csv")
    df = load_dataframe(file_path)
    sliders = create_slider_for_plot()
    layout = create_layout_for_plot(sliders, False)
    data = prepare_data_for_plot(df)
    fig = dict(data=data, layout=layout)
    plotly_config = {
        'modeBarButtonsToRemove': ['sendDataToCloud', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'lasso2d', 'select2d'],
                                    'displaylogo': False, 'showTips': True}
    return py.plot(fig, include_plotlyjs=False, output_type='div', show_link=False, config=plotly_config)


def get_area_plot():
    df = load_dataframe("data/fbh.csv")
    df = df.groupby([df['event']]).agg({'duration': sum,
                                              'frequency': sum})
    lx = ['ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
          'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
          'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
          'TestRunEvent']
    mpl_style.use('ggplot')
    fig, ax = plt.subplots()
    ax.tick_params(labelrotation=-80)
    fig.subplots_adjust(bottom=0.22)
    ax.stackplot(lx, df['frequency'], df['duration'])
    ax.grid()
    plt.yscale('log')
    plt.ylabel("frequency and duration  [log scale]")
    fig.set_tight_layout(True)
    fig.savefig('static/summary.svg')
    #plt.show()
    # return py.plot_mpl(fig, "hello.html")


def main():
    # df = load_dataframe("data/fbh.csv")
    # print(df.head())
    # make_bar_plot(df)
    # print(get_bar_chart_div())
    get_area_plot()
    return


if __name__ == "__main__":
    main()
