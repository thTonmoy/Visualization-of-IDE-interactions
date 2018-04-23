from io import BytesIO
from os import path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


def create_top_commands_csv(no_of_top_commands: int, output_file: str):
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
    # print(df)
    df.to_csv(path_or_buf=output_file, index=False)


def get_wordcloud(root_path: str):
    commands = pd.read_csv(path.join(root_path, 'static', 'data', 'test_comm_100.csv'), usecols=[1, 2])
    d = {}
    for a, x in commands.values:
        d[a] = x

    mask = np.array(Image.open(path.join("static", "img", "vs1.png")))
    image_colors = ImageColorGenerator(mask)
    wordcloud = WordCloud(background_color="white", mask=mask, random_state=32, color_func=image_colors)
    wordcloud.generate_from_frequencies(frequencies=d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    img = BytesIO()
    plt.savefig(img)
    img.seek(0)
    return img


def main():
    # create_top_commands_csv(80, 'static/test_comm_80.csv')
    get_wordcloud('')
    return


if __name__ == "__main__":
    main()
