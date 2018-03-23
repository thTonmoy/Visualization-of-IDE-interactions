import plotly.offline as py
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/transformed_data_2016-05-09_edit.csv', usecols=[1, 2, 3], header=0)
print(df.head())
df = df.sample(frac=0.24)

dataset_array = df.values
# Convert DataFrame to matrix
mat = df.as_matrix()

# Using sklearn
db = KMeans(n_clusters=5, init='k-means++', max_iter= 10).fit(mat)
labels = db.labels_

scatter = dict(
    mode="markers",
    name="y",
    type="scatter3d",
    z=df['duration'] / 60, y=df['location'], x=df['size'],
    marker=dict(
        size=5,
        color=labels,
        colorscale='Viridis',
        opacity=0.8
    )
)

layout = dict(
    title='3d point clustering',
    scene=dict(
        xaxis=dict(zeroline=False, title="size"),
        yaxis=dict(zeroline=False, title="no of places"),
        zaxis=dict(zeroline=False, title="duration [minute]"),
    )
)
fig = dict(data=[scatter], layout=layout)

py.plot(fig, filename='3d point clustering.html')
