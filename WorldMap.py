import pandas as pd
import plotly.offline as py
import os


def basic_details(df):
    print('Number of rows {} and columns {}'.format(df.shape[0], df.shape[1]))
    k = pd.DataFrame()
    k['dtype'] = df.dtypes
    k['Number of unique value'] = df.nunique()
    k['Missing_value'] = df.isnull().sum()
    k['% missing_value'] = df.isnull().sum() / df.shape[0]
    return k


def get_map(root:str):
    hacker_qna = pd.read_csv(os.path.join('data','HackerRank-Developer-Survey-2018-Codebook.csv'))
    df = pd.read_csv(os.path.join('data','HackerRank-Developer-Survey-2018-Values.csv'),
                     na_values='#NULL!', low_memory=False)
    # print('Number of rows and columns in Hacker value data set', df.shape)

    hacker_qna = hacker_qna.set_index('Data Field')
    hacker_qna.head()
    # print(df.head())

    #basic_details(df).T
    # print(df.tail())

    # Count by country
    poo = df['CountryNumeric2'].value_counts()

    # plotly
    data = [dict(
        type='choropleth',
        locations=poo.index,
        locationmode='country names',
        z=poo.values,
        text=('Count' + '<br>'),
        colorscale='hot',
        reversescale=False,
        marker=dict(line=dict(color='rgb(180,180,180)', width=0.5)),

        colorbar=dict(title='Response count')
    )]
    layout = dict(title='Responsive Programmers throughout the world - Number of response by country',
                  geo=dict(showframe=False,
                           showcoastlines=True,
                           projection=dict(type='Mercator')))
    fig = dict(data=data, layout=layout)
    return py.plot(fig, include_plotlyjs=False, output_type='div', show_link=False)