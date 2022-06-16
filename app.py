import streamlit as st
import pickle
import pandas as pd
import requests
st.title('Recommendation System')
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
option = st.selectbox(
    'Enter the name of the movie',
    movies['title'].values
)
similarity = pickle.load(open('cos_sim.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    recommended_movies = []
    movies_posters = []
    for i in top_movies:
        movie_id = movies.iloc[i[0]].movie_id
        movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,movies_posters

if st.button('Recommend'):
    recommendations,poster = recommend(option)
    for i in recommendations:
         col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(poster[0])
    with col2:
        st.text(recommendations[1])
        st.image(poster[1])

    with col3:
        st.text(recommendations[2])
        st.image(poster[2])
    with col4:
        st.text(recommendations[3])
        st.image(poster[3])
    with col5:
        st.text(recommendations[4])
        st.image(poster[4])




