import streamlit as st
from movie_recommender import recommend, new_movies
import pandas as pd
import requests

st.title("Movies Recommendation System")

movies_collection= new_movies['title'].values

movie= st.selectbox('Enter a movie name...',movies_collection)

def fetchPoster(movie_id):
  response= requests.get("https://api.themoviedb.org/3/movie/{}?api_key=b41014ccce63dd9505d8d5c6d847d979&language=en-US".format(movie_id))
  poster_id= response.json()['poster_path']
  return "https://image.tmdb.org/t/p/w500" + poster_id

if st.button('Recommend'):
  recommended_movies= recommend(movie)
  col1, col2, col3, col4, col5= st.columns(5) 
  columns= [col1, col2, col3, col4, col5]
  ind=0
  for i in recommended_movies:
    movie_index= i[0]
    movie_id= new_movies.iloc[movie_index]['movie_id']
    recommended_movies_name= new_movies.iloc[movie_index]['title']
    recommended_movies_poster= fetchPoster(movie_id)

    with columns[ind]:
      st.text(recommended_movies_name)
      st.image(recommended_movies_poster)

    ind+=1



