from os import path

import pandas as pd
import plotly.offline as py
import plotly.tools as tls


def filter_refactoring_edits(file: str, output_file: str, min_location: int = 6, save_as_csv: bool = False):
    df = pd.read_csv(file, header=0)
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    rows = df.shape[0]
    df.drop(df[(df.location < min_location)].index, inplace=True)
    # print("dropped rows based on location : " + str((rows-df.shape[0])/rows))
    df['speed'] = df['size'] / df['duration']
    df.drop(df[(df.speed < 10)].index, inplace=True)
    print("Kept records: " + str(df.shape[0]) + " percentage: " + str(df.shape[0] * 100 / rows))
    # df.sort_values('date', inplace=True, ascending= False)
    # print(df.head(20))
    fin = df.groupby(['date'], as_index=False).agg({'speed': "count", 'size': sum})
    fin.rename({'speed': 'no_of_occurrence'}, axis='columns', inplace=True)
    min = fin['no_of_occurrence'].min()
    max = fin['no_of_occurrence'].max()
    fin['normalized_occurrence'] = (fin['no_of_occurrence'] - min) / (max - min)
    # fin['normalized']=(fin['size']- min)/(max-min)
    if save_as_csv:
        fin.to_csv(path_or_buf=output_file, index=False)
    return fin


def make_dataframe_testing(file: str):
    return pd.read_csv(file, header=0, usecols=[0, 2, 3])


def load_refactoring_dataframe(file: str):
    return pd.read_csv(file)


def make_dataframe_build(file: str):
    df3 = pd.read_csv(file, header=0)
    df3.drop(df3[(df3.fail_rate == 0)].index, inplace=True)
    df3['date'] = pd.to_datetime(df3['date'], format="%Y-%m-%d")
    df3['fail_rate'] = df3['fail_rate'] * -1
    return df3


def get_plotly_fig(df_refactor: pd.DataFrame, df_tests: pd.DataFrame, df_build: pd.DataFrame, add_slider: bool):
    fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True, print_grid=False)
    fig.append_trace({'x': df_refactor.date, 'y': df_refactor['size'], 'type': 'scatter',
                      'name': "refactored bytes", 'mode': 'lines', 'line': dict(color='rgb(114, 186, 59)'),
                      'fill': 'tozeroy', 'fillcolor': 'rgba(114, 186, 59, 0.5)'}, 1, 1)
    fig.append_trace({'x': df_tests.date, 'y': df_tests['fail_rate'], 'type': 'bar', 'name': "failed test"}, 2, 1)
    fig.append_trace({'x': df_refactor.date, 'y': df_refactor['normalized_occurrence'], 'type': 'scatter',
                      'name': "refactoring count normalized"}, 2, 1)
    fig.append_trace({'x': df_build.date, 'y': df_build['fail_rate'], 'type': 'bar', 'name': "failed build"}, 2, 1)
    if (add_slider):
        add_range_slider(fig)
    return fig


def add_range_slider(fig):
    fig['layout'].update(xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1 month',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6 months',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='1y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
    )

    return fig


def get_plot(fig):
    py.plot(fig, filename='pandas-time-series.html')


def get_div_for_plot(root_path: str, id: int = 1):
    if id == 1:
        df_tests = make_dataframe_testing(path.join(root_path, 'data', '2016-05-09_tests.csv'))
        df_refactor = load_refactoring_dataframe(path.join(root_path, 'data', 'user1_refactoring.csv'))
        df_build = make_dataframe_build(path.join(root_path, 'data', '2016-05-09_FailedBuild.csv'))

    else:
        df_tests = make_dataframe_testing(path.join(root_path, 'data', '2016-05-10_tests.csv'))
        df_refactor = load_refactoring_dataframe(path.join(root_path, 'data', 'user2_refactoring.csv'))
        df_build = make_dataframe_build(path.join(root_path, 'data', '2016-05-10_FailedBuild.csv'))

    fig = get_plotly_fig(df_refactor=df_refactor, df_build=df_build, df_tests=df_tests, add_slider=True)
    plotly_config = {
        'modeBarButtonsToRemove': ['sendDataToCloud', 'autoScale2d', 'resetScale2d',
                                   'hoverClosestCartesian', 'hoverCompareCartesian',
                                   'lasso2d', 'select2d'], 'displaylogo': False, 'showTips': True}
    return py.plot(fig, include_plotlyjs=False, output_type='div', show_link=False, config=plotly_config)


def main():
    df_refactor = filter_refactoring_edits('data/csv_data_2016-05-10_edit.csv',
                                           save_as_csv=True, output_file='data/user2_refactoring.csv')
    # df_tests = make_dataframe_testing('data/csv_data_2016-05-09_test.csv')
    # df_build = make_dataframe_build('data/2016-05-09_FailedBuild.csv')
    # fig = get_plotly_fig(df_refactor=df_refactor, df_build=df_build, df_tests=df_tests)
    # get_plot(fig)
    return


if __name__ == "__main__":
    main()
