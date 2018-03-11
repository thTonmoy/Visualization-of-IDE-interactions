import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
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


def create_slider_for_plot(df: pd.DataFrame):
    steps = []
    for i in range(0, 24):
        step = dict(
            method='restyle',
            label=str(i) + ":00- " + str(i + 1) + ":00",
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
    return sliders


def prepare_data_for_plot(df: pd.DataFrame):

    lx = ['ActivityEvent', 'IDEStateEvent', 'SolutionEvent',
          'EditEvent', 'CommandEvent', 'DocumentEvent', 'WindowEvent', 'BuildEvent',
          'NavigationEvent', 'CompletionEvent', 'DebuggerEvent', 'UserProfileEvent', 'SystemEvent',
          'TestRunEvent', 'FindEvent']

    data = [go.Bar(
        visible=False,
        name= str(i) + ":00-" + str(i+1) + ":00",
        y =(df.loc[[i]])['frequency'][1:],
        x = lx,
        #x=np.arange(0, 15, 1),
        #orientation='h',
        # marker=dict(
        #     color=['red', 'green',
        #            'blue', 'rgba(204,204,204,1)'])
    ) for i in range(0, 24)]
    data[0]['visible'] = True

    return data


def create_layout_for_plot(df: pd.DataFrame, sliders):
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
        sliders=sliders
    )
    return layout


def make_bar_plot(df: pd.DataFrame):
    sliders = create_slider_for_plot(df)
    layout = create_layout_for_plot(df, sliders)
    data = prepare_data_for_plot(df)
    fig = dict(data=data, layout=layout)
    py.plot(fig, filename='bar_chart.html')
    return


def get_bar_chart_div(root_path: str):
    file_path = os.path.join(root_path,"data","fbh.csv")
    print(file_path)
    df = load_dataframe(file_path)
    sliders = create_slider_for_plot(df)
    layout = create_layout_for_plot(df, sliders)
    data = prepare_data_for_plot(df)
    fig = dict(data=data, layout=layout)
    return py.plot(fig, include_plotlyjs=True, output_type='div')


def main():
    df = load_dataframe("data/fbh.csv")
    print(df.head())
    make_bar_plot(df)
    #print(get_bar_chart_div())


if __name__ == "__main__":
    main()
