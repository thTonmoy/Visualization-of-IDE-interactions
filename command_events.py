import plotly.offline as py
import pandas as pd
import re

data = pd.read_csv('data/transformed_data_2016-05-09_command.csv', header=0, usecols=[0, 2])
#print(data)
n = 50
df = data.groupby(['trigger', 'id']).agg({'id': "count"})
df.rename({'id': 'count'}, axis='columns', inplace=True)
#total = df['count'].sum()
#df['percent'] = df['count']/total*100  # adding a percentage column
df = df.nlargest(n=n, columns='count')
#print(total)
#df.sort_values('percent', axis=0, ascending=False, inplace=True)
df.reset_index(inplace=True)
df.trigger.replace(to_replace='Unknown',value='Other', inplace=True)
df.id.replace(to_replace='{.*}:', value='', regex=True, inplace=True)
#df = df[df['count'] > 100]
#df.sort_values('count', axis=0, ascending=False, inplace=True)
print(df)
df.to_csv(path_or_buf="static/test_comm.csv", index = False)
