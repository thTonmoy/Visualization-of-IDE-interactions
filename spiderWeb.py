from math import pi

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

## Reading the data:
from pip._vendor.html5lib._trie import py

hackerRank_codebook = pd.read_csv('data/HackerRank-Developer-Survey-2018-Codebook.csv')
hackerRank_numericMapping = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv')
hackerRank_numeric = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric.csv')
hackerRank_values = pd.read_csv('data/HackerRank-Developer-Survey-2018-Values.csv')

# hackerRank_codebook.head()
# for ix,item in hackerRank_codebook.iterrows():
#     print('{0}: {1}\n'.format(item[0], item[1]))
#
# for ix,item in hackerRank_numericMapping.iterrows():
#     print('{0}: {1} : {2}\n'.format(item[0], item[1], item[2]))

## Selecting the female respondents:
#dataset = hackerRank_values[hackerRank_values['q3Gender'] == 'Female']
dataset = hackerRank_values


## Attributes of interest:
attributes = ['q1AgeBeginCoding', 'q2Age', 'q3Gender', 'q4Education', 'q0004_other',
       'q5DegreeFocus', 'q0005_other', 'q6LearnCodeUni',
       'q6LearnCodeSelfTaught', 'q6LearnCodeAccelTrain',
       'q6LearnCodeDontKnowHowToYet', 'q6LearnCodeOther', 'q0006_other',
       'q8JobLevel', 'q0008_other', 'q8Student', 'q9CurrentRole',
       'q0009_other', 'q10Industry', 'q0010_other', 'q12JobCritPrefTechStack',
       'q12JobCritCompMission', 'q12JobCritCompCulture',
       'q12JobCritWorkLifeBal', 'q12JobCritCompensation',
       'q12JobCritProximity', 'q12JobCritPerks', 'q12JobCritSmartPeopleTeam',
       'q12JobCritImpactwithProduct', 'q12JobCritInterestProblems',
       'q12JobCritFundingandValuation', 'q12JobCritStability',
       'q12JobCritProfGrowth', 'q0012_other', 'q27EmergingTechSkill',
       'q0027_other', 'q28LoveC', 'q28LoveCPlusPlus', 'q28LoveJava',
       'q28LovePython', 'q28LoveRuby', 'q28LoveJavascript', 'q28LoveCSharp',
       'q28LoveGo', 'q28LoveScala', 'q28LovePerl', 'q28LoveSwift',
       'q28LovePascal', 'q28LoveClojure', 'q28LovePHP', 'q28LoveHaskell',
       'q28LoveLua', 'q28LoveR', 'q28LoveRust', 'q28LoveKotlin',
       'q28LoveTypescript', 'q28LoveErlang', 'q28LoveJulia', 'q28LoveOCaml',
       'q28LoveOther']

dataset = dataset[attributes]

#print(dataset.info())
dataset[dataset['q4Education'] == 'Other (please specify)']
## Checking the 'q4Education' values:
dataset['q4Education'].unique()

## Dropping the 'q4Education' #NULL values:
ixNull = dataset[dataset['q4Education']=='#NULL!'].index
dataset = dataset.drop(labels=ixNull)

## Dropping the 'Other education level' column:
dataset = dataset.drop('q0004_other', axis=1)

dataset['q8JobLevel'].unique()
dataset['q0008_other'].unique()

## Counting the different employment levels:
q0008_total = dataset['q0008_other'].count()
q0008_unique = len(dataset['q0008_other'].unique())
#print('From {0} different employment levels, {1} are unique.'.format(q0008_total, q0008_unique))

## Dropping down these instances:
q0008_indexes = dataset[dataset['q8JobLevel'] == dataset['q8JobLevel'].unique()[3]]['q0008_other'].index
dataset = dataset.drop(labels=q0008_indexes)
dataset = dataset.drop('q0008_other', axis=1)

indexq8JobLevel = dataset[dataset['q8JobLevel'] == 'Student'].index  #float64 type
indexq8Student = dataset[dataset['q8Student'] == 'Students'].index  #float64 type

np.unique(indexq8JobLevel == indexq8Student)

def clean_null(dataset):
    for col in dataset.columns:
        if '#NULL!' in dataset[col].unique():
            ixNull = dataset[dataset[col]=='#NULL!'].index
            dataset = dataset.drop(labels=ixNull)
            print('It was cleaned {0} null instances from {1}'.format(len(ixNull), col))
    return dataset

dataset = clean_null(dataset)

def map_q8JobLevel(ix):
    temp = hackerRank_numericMapping[(hackerRank_numericMapping['Data Field']=='q8JobLevel')&(hackerRank_numericMapping['Value']==ix)]['Label']
    temp = temp.values
    return temp[0]

def map_q4Education(ix):
    temp = hackerRank_numericMapping[(hackerRank_numericMapping['Data Field']=='q4Education')&(hackerRank_numericMapping['Value']==ix)]['Label']
    temp = temp.values
    return temp[0]
## Student - Under college:
education = [map_q4Education(1), map_q4Education(2)]
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Category'] = 'Student'
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Profile'] = 'Under college'

## Student - College:
education = [map_q4Education(3), map_q4Education(4), map_q4Education(5)]
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Category'] = 'Student'
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Profile'] = 'College'

## Student - Graduate:
education = [map_q4Education(6), map_q4Education(7)]
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Category'] = 'Student'
dataset.loc[(dataset['q8JobLevel']=='Student') & (dataset['q4Education'].isin(education)), 'Profile'] = 'Graduate'

## Professional - Junior:
joblevel = [map_q8JobLevel(2), map_q8JobLevel(4)]
dataset.loc[(dataset['q8JobLevel'].isin([2,4])), 'Category'] = 'Professional'
dataset.loc[(dataset['q8JobLevel'].isin([2,4])), 'Profile'] = 'Junior'


## Professional - Senior:
joblevel = [map_q8JobLevel(5), map_q8JobLevel(6), map_q8JobLevel(7), map_q8JobLevel(8)]
dataset.loc[(dataset['q8JobLevel'].isin(joblevel)), 'Category'] = 'Professional'
dataset.loc[(dataset['q8JobLevel'].isin(joblevel)), 'Profile'] = 'Senior'

## Professional - Freelancer:
dataset.loc[(dataset['q8JobLevel']==map_q8JobLevel(3)), 'Category'] = 'Professional'
dataset.loc[(dataset['q8JobLevel']==map_q8JobLevel(3)), 'Profile'] = 'Freelancer'

## Professional - Executive:
joblevel = [map_q8JobLevel(9), map_q8JobLevel(10)]
dataset.loc[(dataset['q8JobLevel'].isin(joblevel)), 'Category'] = 'Professional'
dataset.loc[(dataset['q8JobLevel'].isin(joblevel)), 'Profile'] = 'Executive'


def df_row_normalize(dataframe):
    '''Normalizes the values of a given pandas.Dataframe by the total sum of each line.
    Algorithm based on https://stackoverflow.com/questions/26537878/pandas-sum-across-columns-and-divide-each-cell-from-that-value'''
    return dataframe.div(dataframe.sum(axis=1), axis=0)

language = dataset[['q28LoveC', 'q28LoveCPlusPlus',
       'q28LoveJava', 'q28LovePython', 'q28LoveRuby', 'q28LoveJavascript',
       'q28LoveCSharp', 'q28LoveGo', 'q28LoveScala', 'q28LovePerl',
       'q28LoveSwift', 'q28LovePascal', 'q28LoveClojure', 'q28LovePHP',
       'q28LoveHaskell', 'q28LoveLua', 'q28LoveR', 'q28LoveRust',
       'q28LoveKotlin', 'q28LoveTypescript', 'q28LoveErlang', 'q28LoveJulia',
       'q28LoveOCaml', 'q28LoveOther', 'Category']]

## Replacing all "hate" and "NaN" values by zero (we're interestede just in the languages they love, for while)
lovelanguage = language.replace('Hate',0)
lovelanguage = lovelanguage.replace('Love', 1)

## Replacing all "Love" and "NaN" values by zero (we're now interested just in the languages they hate)
hatelanguage = language.replace('Love',0)
hatelanguage = hatelanguage.replace('Hate', 1)

lovelanguage = lovelanguage.groupby('Category').sum()
lovelanguage = df_row_normalize(lovelanguage)*100
lovelanguage.reset_index(inplace=True)

hatelanguage = hatelanguage.groupby('Category').sum()
hatelanguage = df_row_normalize(hatelanguage)*100
hatelanguage.reset_index(inplace=True)

## Adjusting the columns names:
lovelanguage.columns
lovelanguage.columns = ['group','C', 'C++', 'Java', 'Python','Ruby', 'Javascript', 'C#', 'Go',
       'Scala', 'Perl', 'Swift', 'Pascal','Clojure', 'PHP', 'Haskell', 'Lua','R', 'Rust',
       'Kotlin', 'Typescript','Erlang', 'Julia', 'OCaml']
hatelanguage.columns = lovelanguage.columns

def get_spidy(root:str):
    #From: https://python-graph-gallery.com/391-radar-chart-with-several-individuals/
    categories = list(lovelanguage)[1:]
    N = len(categories)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    # Initialise the spider plot
    fig3 = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    plt.title('Which programming language do people love the most?', fontsize=14, fontweight='bold')

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([5, 10, 15], ["5%", "10%", "15%"], color="grey", size=12)
    plt.ylim(0, 15)

    # Plot each individual = each line of the data
    # Ind1
    values = lovelanguage.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Professional(Love)")
    ax.fill(angles, values, 'b', alpha=0.1)
    # Ind2
    values = lovelanguage.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, linestyle='solid', label="Students(Love)")
    ax.fill(angles, values, 'r', alpha=0.1)
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    #plt.savefig('static/lovewWeb.png')

    ####HATE HATE   HATE HATE HATE
    categories1 =list(hatelanguage)[1:]
    N = len(categories1)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    # Initialise the spider plot
    fig3 = plt.figure(figsize=(8,8))
    bx = plt.subplot(111, polar=True)
    plt.title('Which programming language do people hate the most?', fontsize=14, fontweight='bold')
    # If you want the first axis to be on top:
    bx.set_theta_offset(pi / 2)
    bx.set_theta_direction(-1)
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories)
    # Draw ylabels
    bx.set_rlabel_position(0)
    plt.yticks([3,6,9], ["3%","6%","9%"], color="red", size=12)
    plt.ylim(0,9)
    # Plot each individual = each line of the data
    # Ind1
    values=hatelanguage.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    bx.plot(angles, values, linewidth=1, linestyle='solid', label="Professional(Hate)")
    bx.fill(angles, values, 'b', alpha=0.1)
    # Ind2
    values=hatelanguage.loc[1].drop('group').values.flatten().tolist()
    values += values[:1]
    bx.plot(angles, values, linewidth=1, linestyle='solid', label="Students(Hate)")
    bx.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.show()
    #return py.plot(fig3, include_plotlyjs=False, output_type='div', show_link=False)

def main():
    get_spidy("")
    return

if __name__ == "__main__":
    main()
