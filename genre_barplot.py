# this is a copy of ipython notebook which for the monent does not load matplotlib

import sys,codecs,os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/home/masha/RusLTC/update_Aug2017/all_texts-by-genre2.csv')
# выглядит таблица так
# genre	num_of_texts	total_size
# academic 	28	49834
# advertisement 	7	2993
# educational 	50	122740
# essay 	126	112519

pd.to_numeric(df['num_of_texts'])

# sort df by num_of_texts column
df = df.sort_values(['num_of_texts']).reset_index(drop=True) #вращаем таблицу так, чтоб в строке заголовка (в индексе, ключах словаря, оказалось кол-во текстов)

sns.set_style("whitegrid")
sns.set_context('paper')
plt.figure(figsize=(12,8))

# plot barh chart with index as x values
ax = sns.barplot(df.index, df.num_of_texts) #, color = 'blue'
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x)))) # вот это не понимаю
ax.set(xlabel="genres", ylabel='number of sources')
ax.set_title('Number of source texts in both languages by genre')


# add proper genre values as x labels
ax.set_xticklabels(df.genre)
for item in ax.get_xticklabels(): item.set_rotation(45)
for i, v in enumerate(df["num_of_texts"].iteritems()):        
    ax.text(i ,v[1], "{:,}".format(v[1]), color='black', va ='bottom', rotation=45)
plt.tight_layout()
plt.show()

#this is how produce the basic plot from the tidy long-table (different input!), and not the summary of data used above
#df1 = pd.read_csv('/home/masha/RusLTC/update_Aug2017/all_texts-by-genre.csv')
#plt.figure(figsize=(15,10))
#sns.countplot(x='genre', data=df1, palette="Greens_d")