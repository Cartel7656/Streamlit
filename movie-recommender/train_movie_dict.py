# train_movie_dict.py

import requests
import pandas as pd
import pickle
from dotenv import load_dotenv
import os

# ----------------------
# Load TMDB API key from .env
# ----------------------
load_dotenv()  # load environment variables from .env
API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise ValueError("TMDB_API_KEY not found in .env file. Make sure .env exists in the same folder and contains TMDB_API_KEY=your_key_here")

# ----------------------
# Configuration
# ----------------------
NUM_PAGES = 5  # Number of pages to fetch from TMDB (20 movies per page)

# ----------------------
# Functions
# ----------------------
def fetch_movies_from_tmdb(api_key, num_pages=5):
    """
    Fetch movies from TMDB popular endpoint.
    Returns a pandas DataFrame.
    """
    all_movies = []

    for page in range(1, num_pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=en-US&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for movie in data['results']:
            all_movies.append({
                "id": movie['id'],
                "title": movie['title'],
                "overview": movie['overview'],
                "poster_path": movie['poster_path'],
                "release_date": movie.get('release_date', ''),
                "vote_average": movie['vote_average'],
                "vote_count": movie['vote_count']
            })

    df = pd.DataFrame(all_movies)
    return df

def make_movies_dict(df):
    """
    Convert DataFrame to dictionary usable by app.
    """
    return df.to_dict(orient="records")

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    print("Fetching movies from TMDB...")
    movies_df = fetch_movies_from_tmdb(API_KEY, NUM_PAGES)
    print(f"Fetched {len(movies_df)} movies.")

    movies_dict = make_movies_dict(movies_df)

    # Save pickle file
    with open("movies_dict.pkl", "wb") as f:
        pickle.dump(movies_dict, f)

    print("Saved movies_dict.pkl successfully!")
