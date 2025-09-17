import streamlit as st
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

# --------------------------
# Load TMDB API key
# --------------------------
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    st.error("TMDB_API_KEY not found in .env file")
    st.stop()

# --------------------------
# Load movies
# --------------------------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = [movie['title'] for movie in movies_dict]

# --------------------------
# Compute TF-IDF similarity
# --------------------------
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform([movie['overview'] for movie in movies_dict])
similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

# --------------------------
# Recommendation function
# --------------------------
def recommend(movie_title, top_n=5):
    idx = movies.index(movie_title)
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    recommended = [movies_dict[i[0]] for i in sim_scores]
    return recommended

# --------------------------
# Get poster from TMDB
# --------------------------
def get_poster(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w200{poster_path}"  # smaller width for side-by-side
    return None

# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(layout="wide")
st.title("Movie Recommender")

selected_movie = st.selectbox("Choose a movie:", movies)

# Display detailed description of selected movie
movie_index = movies.index(selected_movie)
movie_data = movies_dict[movie_index]
st.subheader(selected_movie)
st.write(movie_data['overview'])

# Show recommendations
if st.button("Recommend"):
    recommendations = recommend(selected_movie, top_n=5)
    cols = st.columns(len(recommendations))
    for idx, rec in enumerate(recommendations):
        brief_desc = rec['overview'][:120] + "..." if len(rec['overview']) > 120 else rec['overview']
        with cols[idx]:
            st.markdown(f"""
            <div style="
                border:1px solid #ddd;
                border-radius:10px;
                padding:10px;
                text-align:center;
                transition: transform 0.3s, box-shadow 0.3s;
            " onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='5px 5px 15px rgba(0,0,0,0.3)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                <img src="{get_poster(rec['poster_path'])}" style="width:100%; border-radius:10px;">
                <h4>{rec['title']}</h4>
                <p><b>Rating:</b> {rec['vote_average']}</p>
                <p>{brief_desc}</p>
            </div>
            """, unsafe_allow_html=True)
