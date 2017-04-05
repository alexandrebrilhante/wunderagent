
# coding: utf-8

# In[13]:

# Alexandre Brilhante

import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns

import datetime

get_ipython().magic('matplotlib inline')

db = 'database.sqlite'
connect = sqlite3.connect(db)
query = "SELECT name FROM sqlite_master WHERE type = 'table';"


# In[46]:

# Initialization
query = "SELECT * FROM player"
players_df = pd.read_sql(query, connect)
query = "SELECT * FROM player_attributes"
player_stats_df = pd.read_sql(query, connect)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 151)


# In[47]:

# Merge the player and player_attribute data
df = players_df.merge(player_stats_df, how='inner', on='player_api_id')

# Date adjusting
df['date'] = pd.to_datetime(df['date'])

# Unnecessary columns
df.drop(['id_x', 'id_y', 'player_fifa_api_id_x', 'player_fifa_api_id_y'], 1, inplace=True)
ratings_df = df[['player_api_id', 'player_name', 'date', 'overall_rating', 'potential']]

# Drop players without any rating
ratings_df = ratings_df.drop(ratings_df[ratings_df['overall_rating'].isnull()].index)

# Sorting by rating
ratings_df.sort_values(['player_name', 'overall_rating'],
                       ascending=[True, False], inplace=True)

# Change the date to just the year
ratings_df['date'] = ratings_df['date'].apply(lambda x: x.year)


# In[48]:

# Grouping the players by the year
group = ratings_df.groupby('date')


# In[49]:

# Ranking players based on overall ratings, removing duplicates first
data = group.apply(lambda x: x.drop_duplicates(subset='player_api_id', keep='first').
                   sort_values(by=['overall_rating'], ascending=[False]).
                   reset_index(drop=True).
                   head(15))


# In[51]:

# Best team possible for each year
data


# In[7]:

# Bonus: the best team is 2007
data.groupby('date').sum().sort_values(['overall_rating'], ascending=[False])


# In[55]:

# Bonus: player evolution
players = data.sort_values('overall_rating', ascending=[False])
best_players = players[['player_api_id','player_name']].head(150)
ids = tuple(best_players.player_api_id.unique())

query = "SELECT player_api_id, date, overall_rating, potential FROM player_attributes WHERE player_api_id in %s"%(ids,)

evolution = pd.read_sql(query, connect)
evolution = pd.merge(evolution, best_players)
evolution['year'] = evolution.date.str[:4].apply(int)
evolution = evolution.groupby(['year','player_api_id','player_name']).overall_rating.mean()
evolution = evolution.reset_index()


# In[56]:

# Not a very clear graph but Tableau could be used for presentation
sns.factorplot(data=evolution[evolution.player_api_id.isin(ids[0:-1])],
               x='year', y='overall_rating', hue='player_name', size=10, aspect=2)


# In[ ]:



