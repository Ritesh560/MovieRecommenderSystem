import streamlit as st
from movie_recommender import recommend
st.title("Movies Recommendation System")

movie_list= recommend('Avatar')
for i in movie_list:
  st.title(i)