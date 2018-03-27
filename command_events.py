import pandas as pd

# merge  sed 1d transformed_data*.csv > merged.csv
data = pd.read_csv('data/merged.csv', header=0, usecols=[0, 2])
data.id.replace(to_replace='{.*:', value='', regex=True, inplace=True)
data.id.replace(to_replace=['VsAction:1:', 'TextControl.', 'Edit.', 'Debug.', 'File.'], value='', regex=True, inplace=True)
n = 80
df = data.groupby(['trigger', 'id']).agg({'id': "count"})
df.rename({'id': 'count'}, axis='columns', inplace=True)
#total = df['count'].sum()
#df['percent'] = df['count']/total*100  # adding a percentage column
df = df.nlargest(n=n, columns='count')
#print(total)
#df.sort_values('percent', axis=0, ascending=False, inplace=True)
df.reset_index(inplace=True)
df.trigger.replace(to_replace='Unknown',value='Other', inplace=True)
# df.id.replace(to_replace='{.*:', value='', regex=True, inplace=True)
# df.id.replace(to_replace=['VsAction:1:', 'TextControl.'], value='', regex=True, inplace=True)
# df.id.replace(to_replace=['Edit.', 'Debug.', 'File.'], value='', regex=True, inplace=True)  # Too aggressive
#df = df[df['count'] > 100]
#df.sort_values('count', axis=0, ascending=False, inplace=True)
print(df)
df.to_csv(path_or_buf="static/test_comm.csv", index=False)
