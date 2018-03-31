import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas.tools.plotting
import seaborn as sns
import matplotlib
import squarify

plt.style.use('seaborn')

codebook = pd.read_csv('data/HackerRank-Developer-Survey-2018-Codebook.csv')
numeric_mapping = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv')
numeric = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric.csv', na_values=['#NULL!', 'nan'])
values = pd.read_csv('data/HackerRank-Developer-Survey-2018-Values.csv', na_values=['#NULL!', 'nan'])

codebook.head()
numeric_mapping.head()
numeric.head()
values.head()

codebook.columns = ['fieldname', 'question', 'notes']
codebook.set_index('fieldname', inplace=True);
numeric_mapping.set_index('Data Field', inplace=True)

numeric.q1AgeBeginCoding = numeric.q1AgeBeginCoding.astype(float)
numeric.q2Age = numeric.q2Age.astype(float)
numeric = numeric.fillna(-1)

values = values.fillna('Not provided')
print(values.columns.ravel())

columns = [i for i in values.columns.ravel() if 'q28' in i]
langs_known = [i for i in values.columns.ravel() if 'q25' in i]
columns = columns[:-1]
langs_known = langs_known[:-1]

plt.figure(figsize=(16, 5))

plt.subplot(121)
love_height = []
hate_height = []

for i, j in enumerate(zip(columns, langs_known)):
    love = len(numeric[(numeric[j[1]] >= 1) & (values[j[0]] == 'Love')]) / (len(numeric[numeric[j[1]] >= 1]))
    plt.bar(i, love, color='green')
    plt.text(i, love - 0.05, '%i' % int(love * 100), horizontalalignment='center', size=10, color='white')

    hate = len(numeric[(numeric[j[1]] >= 1) & (values[j[0]] == 'Hate')]) / (len(numeric[numeric[j[1]] >= 1]))
    plt.bar(i, -hate, color='orange')
    plt.text(i, -hate + 0.01, '%i' % int(hate * 100), horizontalalignment='center', size=10, color='white')

    love_height.append(love)
    hate_height.append(hate)

custom_lines = [matplotlib.patches.Patch(color='green', lw=1),
                matplotlib.patches.Patch(color='orange', lw=1),
                matplotlib.lines.Line2D([0], [0], color='red')]

plt.legend(custom_lines, ['Love', 'Hate', 'Overall reputation'])
plt.plot([(i - j) / 2 for i, j in zip(love_height, hate_height)], color='red')

plt.gca().set_xticks(range(len(columns)))
plt.gca().set_xticklabels([j.split('Love')[-1] for j in columns], rotation='vertical');
plt.gca().set_title('Reputation of languages that developers know or will learn');
plt.gca().set_yticklabels(['%i%%' % abs(i * 100) for i in plt.yticks()[0]]);
plt.ylabel('Percentage of users');

plt.subplot(122)
love_height = []
hate_height = []

for i, j in enumerate(zip(columns, langs_known)):
    love = len(numeric[(numeric[j[1]] == 0) & (values[j[0]] == 'Love')]) / (len(numeric[numeric[j[1]] >= 1]))
    plt.bar(i, love, color='green')
    plt.text(i, love - 0.02, '%i' % int(love * 100), horizontalalignment='center', size=10, color='white')

    hate = len(numeric[(numeric[j[1]] == 0) & (values[j[0]] == 'Hate')]) / (len(numeric[numeric[j[1]] >= 1]))
    plt.bar(i, -hate, color='orange')
    plt.text(i, -hate + 0.01, '%i' % int(hate * 100), horizontalalignment='center', size=10, color='white')

    love_height.append(love)
    hate_height.append(hate)

plt.plot([(i - j) / 2 for i, j in zip(love_height, hate_height)], color='red')

plt.gca().set_xticks(range(len(columns)))
plt.gca().set_xticklabels([j.split('Love')[-1] for j in columns], rotation='vertical')
plt.gca().set_title('Reputation of languages that developers did not nor will not learn')
plt.gca().set_yticklabels(['%i%%' % abs(i * 100) for i in plt.yticks()[0]])
plt.ylabel('Percentage of users')
plt.show()
plt.savefig('static/languages_reputation.png')
