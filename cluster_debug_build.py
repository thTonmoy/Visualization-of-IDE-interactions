import plotly.offline as py
import pandas as pd
from sklearn.cluster import KMeans
from os import path


def make_summary_frame():
    data = pd.read_csv('data/cluster_data_lang.csv', header=0)

    df_debug = data[data['type'] == 0]
    df_test_build = data.drop(index=df_debug.index)
    df_debug = df_debug.groupby(data['lang']).agg({'duration': 'mean'})
    # print(df_debug)
    df_test_build = df_test_build.groupby(data['lang']).agg({'success': 'mean', 'fail': 'mean'})
    df = pd.merge(df_debug, df_test_build, how='outer',
                  left_index=True, right_index=True)
    df.fillna(0, inplace=True)
    print(df)
    return df


def apply_clustering(df: pd.DataFrame, no_cluster: int = 4):
    df.reset_index(inplace=True)
    mat = df.drop(labels='lang', axis=1).as_matrix()
    db = KMeans(n_clusters=no_cluster, init='k-means++', max_iter=10).fit(mat)
    labels = db.labels_
    df['cluster'] = labels
    df.to_csv("static/cluster_data.csv", index=False)


def get_cluster_viz_dv(root_path: str):
    file_path = path.join(root_path, 'static', 'data', 'cluster_data.csv')
    df = pd.read_csv(file_path)

    scatter = dict(
        mode="markers",
        type="scatter3d",
        text=df['lang'],
        z=df['fail'], y=df['duration'], x=df['cluster'],
        hoverinfo='text',
        marker=dict(
            size=6,
            color=df['cluster'],
            colorscale='Viridis',
            opacity=0.85
        )
    )

    layout = dict(
        title='Programming Languages clustered on debugging ease and failure rate',
        scene=dict(
            xaxis=dict(zeroline=False, showspikes=False, title="group"),
            yaxis=dict(zeroline=False, showspikes=False, title="fails"),
            zaxis=dict(zeroline=False, showspikes=False, title="duration debugging"))
    )
    data = [scatter]
    fig = dict(data=data, layout=layout)
    plotly_config = {
        'modeBarButtonsToRemove': ['sendDataToCloud', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
                                   'hoverCompareCartesian', 'lasso2d', 'select2d'],
        'displaylogo': False, 'showTips': True}
    return py.plot(fig, include_plotlyjs=True, output_type='div', show_link=False, config=plotly_config)


def main():
    df = make_summary_frame()
    apply_clustering(df)
    return


if __name__ == "__main__":
    main()