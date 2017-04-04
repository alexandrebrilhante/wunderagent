
# coding: utf-8

# In[35]:

# Alexandre Brilhante

import sqlite3
import pandas as pd
import numpy as np
import datetime

db = 'database.sqlite'
connect = sqlite3.connect(db)
query = "SELECT name FROM sqlite_master WHERE type = 'table';"
pd.read_sql(query, connect)


# In[36]:

# Initialize

query = "SELECT * FROM player;"
players_df = pd.read_sql(query, connect)

query = "SELECT * FROM player_attributes"
player_stats_df = pd.read_sql(query, connect)

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_rows', 200)


# In[37]:

# Merge the player and player_attribute data
df = players_df.merge(player_stats_df, how='inner', on='player_api_id')

df['date'] = pd.to_datetime(df['date'])

# Unnecessary columns
df.drop(['id_x', 'id_y', 'player_fifa_api_id_x', 'player_fifa_api_id_y'], 1, inplace=True)
ratings_df = df[['player_api_id', 'player_name', 'date', 'overall_rating', 'potential']]

# Drop players without any rating
ratings_df = ratings_df.drop(ratings_df[ratings_df['overall_rating'].isnull()].index)

# Sorting by rating rather than age
ratings_df.sort_values(['player_name', 'player_api_id', 'overall_rating'],
                       ascending=[True, True, False], inplace=True)

# Change the date to just the year
ratings_df['date'] = ratings_df['date'].apply(lambda x: x.year)


# In[44]:

# Grouping the players by the year
group = ratings_df.groupby('date')

# Dropping the duplicate player entries per year
ratings_df_unique = group.apply(lambda x: x.drop_duplicates(subset = 'player_api_id', keep = 'first'))

# Grouping the df again into another df group object
group = ratings_df_unique.groupby('date')


# Ranking players based on overall ratings

# In[50]:

data = group.apply(lambda x: x.sort_values(by='overall_rating', ascending=[False]).sort_values(
    by=['overall_rating'], ascending=[False]).reset_index(drop=True).head(15))


# In[51]:

""" Best team possible for each year. """

data


# In[49]:

data.groupby('date').sum().sort_values(['overall_rating'], ascending=[False])


# In[48]:

""" The best team is 2007. """


# In[ ]:



