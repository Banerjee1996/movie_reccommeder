import streamlit as st
import pandas as pd
import requests

import pickle
movies = pd.read_pickle("./movies.pkl")
movie_list = movies.title.values
similarity = pd.read_pickle("./movie_matrix2.pkl")
st.set_page_config(layout="wide")

def recommend(movie):
    suggest = []
    suggest_pic = []
    index = movies[movies['title'] == movie].index[0]
    
    distances = similarity[index]
    
    movies_list = sorted(list(enumerate(distances)),reverse=True , key =  lambda x  :x[1])
    
    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].id
        suggest.append(movies.iloc[i[0]].title)
        suggest_pic.append(fetch_poster(movie_id))
    
    return [suggest , suggest_pic]

def fetch_poster(movie_id):

    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=30e1c55aebfba67795a73676d6a0b416'.format(movie_id))

    data = response.json()
    #st.text(data)
    return 'https://image.tmdb.org/t/p/w500/' + str(data['poster_path'])


st.title("Movie Recommender System ")
option = st.selectbox(
     'Please select your movie of choice',
     (movie_list))

st.write('You selected:', option)

if st.button('Recommend'):
    movie_name , movie_pic  = recommend(option)
    cols = st.columns(len(movie_name))
    # Use the full page instead of a narrow central column
    

    

    for i in range(0,5) :
    
        with cols[i]:
            st.subheader(movie_name[i])
            st.image(movie_pic[i])