import plotly.offline as py
import pandas as pd
from sklearn.cluster import KMeans


def make_summary_frame():
    data = pd.read_csv('data/cluster_data_lang.csv', header=0)

    df_debug = data[data['type'] == 0]
    df_test_build = data.drop(index=df_debug.index)

    df_debug = df_debug.groupby(data['lang']).agg({'duration': 'mean'})
    #print(df_debug)
    df_test_build = df_test_build.groupby(data['lang']).agg({'success': 'mean', 'fail': 'mean'})
    #print(df_test_build)

    df = pd.merge(df_debug, df_test_build, how='outer',
                  left_index=True, right_index=True)

    df.fillna(0, inplace=True)
    print(df)
    df.to_csv("static/cluster_data.csv")


def make_plot(df):
    mat = df.drop(labels='lang', axis=1).as_matrix()
    #MinMaxScaler(copy=False).fit(mat)

    # Using sklearn
    db = KMeans(n_clusters=4, init='k-means++', max_iter=10).fit(mat)
    labels = db.labels_

    scatter = dict(
        mode="markers",
        type="scatter3d",
        text=df['lang'],
        z=df['fail'], y=df['duration'], x=labels,
        hoverinfo='text',
        marker=dict(
            size=6,
            color=labels,
            colorscale='Viridis',
            opacity=0.85
        )
    )

    layout = dict(
        title='3d point clustering',
        scene=dict(
            xaxis=dict(zeroline=False, showspikes=False, title="group"),
            yaxis=dict(zeroline=False, showspikes=False, title="fails"),
            zaxis=dict(zeroline=False, showspikes=False, title="duration debugging"),
        )
    )
    data= [scatter]
    fig = dict(data=data, layout=layout)

    py.plot(fig, filename='3d point clustering.html')


def main():
    #make_summary_frame()
    make_plot(pd.read_csv("static/cluster_data.csv"))
    return


if __name__ == "__main__":
    main()