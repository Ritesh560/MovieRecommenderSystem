# %%
import numpy as np
import pandas as pd

# %%
creadits = pd.read_csv('tmdb_5000_credits.csv')
movies = pd.read_csv('tmdb_5000_movies.csv')


# %%
# creadits.head()
movies.head()

# %%
movies= movies.merge(creadits, on='title')

# %%
movies= movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

# %%
movies.isnull().sum()

# %%
movies.dropna(inplace=True)

# %%
movies.duplicated().sum()


# %%
# now we need to append the data of different collumns to create tags

# %%
# function to convert the string of list of objects of a column to a list of name in each object.
import ast
def fetchNamesList(list_string):
  L=[]
  for i in ast.literal_eval(list_string):
    L.append(i['name'])
  return L

def fetchTop3CastNames(list_string):
  L=[]
  count=0
  for i in ast.literal_eval(list_string):
    if count<3:
      L.append(i['name'])
      count+=1
    else: return L
  return L

def fetchDirector(list_string):
  L=[]
  for i in ast.literal_eval(list_string):
    if i['job']=="Director":
      L.append(i['name'])
      break
    
  return L

# %%
# filter all the columns to get only the required values

movies['genres']= movies['genres'].apply(fetchNamesList)
movies['keywords']= movies['keywords'].apply(fetchNamesList)
movies['cast']= movies['cast'].apply(fetchTop3CastNames)
movies['crew']= movies['crew'].apply(fetchDirector)

# %%
# remove space between words of names

movies['genres']= movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x ])
movies['keywords']= movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x ])
movies['cast']= movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x ])
movies['crew']= movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x ])

# %%
movies['overview'] = movies['overview'].apply(lambda x:x.split())

# %%
# merging all the columns to create a single column called tags
movies['tags']= movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

# %%
new_movies= movies[['movie_id', 'title', 'tags']]

# %%
new_movies['tags']= new_movies['tags'].apply(lambda x: " ".join(x))

# %%
# removing similar workds like action and actions 
# for that we use this posterstremmer that will make all the similar words to their root
# like making actions-> action

# %%
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()

# %%
def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

# %%
new_movies['tags']= new_movies['tags'].apply(stem)


# %%
# convert the tags into vectors so that we can plot it on axis and 
# plot them to find nearest of their neighbours

# %%
from sklearn.feature_extraction.text import CountVectorizer
cv= CountVectorizer(max_features=5000, stop_words="english")

# %%
vectors= cv.fit_transform(new_movies['tags']).toarray()

# %%
# now finding the difference between any two movies in data frame of movies

# %%
from sklearn.metrics.pairwise import cosine_similarity

# %%
similarities= cosine_similarity(vectors)

# %%
def recommend(movie):
  movie_index= new_movies[new_movies['title']==movie].index[0]
  distance= similarities[movie_index]
  movie_list = sorted(list(enumerate(distance)), reverse=True, key= lambda x: x[1])[1:6]

  return movie_list
  # for i in movie_list:
    # print(new_movies.iloc[i[0]]['title'])

# %%
# recommend('Avatar')


