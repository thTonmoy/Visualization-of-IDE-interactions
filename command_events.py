import pandas as pd


def create_top_commands_csv(no_of_top_commands:int, output_file:str):
    # merge  sed 1d transformed_data*.csv > merged.csv
    data = pd.read_csv('data/merged.csv', header=0, usecols=[0, 2])
    data.id.replace(to_replace='{.*:', value='', regex=True, inplace=True)
    data.id.replace(to_replace=['VsAction:1:', 'TextControl.', 'Edit.', 'Debug.', 'File.'],
                    value='', regex=True, inplace=True)
    df = data.groupby(['trigger', 'id']).agg({'id': "count"})
    df.rename({'id': 'count'}, axis='columns', inplace=True)
    # total = df['count'].sum()
    # df['percent'] = df['count']/total*100  # adding a percentage column
    df = df.nlargest(n=no_of_top_commands, columns='count')
    df.reset_index(inplace=True)
    df.trigger.replace(to_replace='Unknown', value='Other', inplace=True)
    #print(df)
    df.to_csv(path_or_buf=output_file, index=False)


def get_wordcloud():
    bag = pd.read_csv('static/test_comm_100.csv', usecols=[1,2])
    d = {}
    for a, x in bag.values:
        d[a] = x

    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    wordcloud = WordCloud()
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def main():
    #create_top_commands_csv(80, 'static/test_comm_80.csv')
    get_wordcloud()
    return


if __name__ == "__main__":
    main()
