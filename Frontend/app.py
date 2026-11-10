import os
import pickle as pkl
import pandas as pd
import streamlit as st
import requests

BASE = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER = "https://placehold.co/500x750?text=No+Poster"
HERE = os.path.dirname(os.path.abspath(__file__))
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"


@st.cache_resource
def load_data():
    movies = pd.DataFrame(pkl.load(open(os.path.join(HERE, 'movies_dict.pkl'), 'rb')))
    similarity = pkl.load(open(os.path.join(HERE, 'similarity.pkl'), 'rb'))
    return movies, similarity


movies, similarity = load_data()

ID_COL = next((c for c in ('movie_id', 'id') if c in movies.columns), None)
if ID_COL is None:
    st.error(f"No TMDB id column found. Columns available: {list(movies.columns)}")
    st.stop()

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox('Select a movie', movies['title'].values)


@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}',
            params={'api_key': API_KEY, 'language': 'en-US'},
            timeout=10,
        )
        response.raise_for_status()
        path = response.json().get('poster_path')
        if path:
            return BASE + path
    except requests.RequestException:
        pass
    return PLACEHOLDER


def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    top_5 = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    names, posters = [], []
    for idx, _ in top_5:
        row = movies.iloc[idx]
        names.append(row['title'])
        posters.append(fetch_poster(row[ID_COL]))
    return names, posters


if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])