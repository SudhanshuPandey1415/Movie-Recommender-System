import streamlit as st
import pickle
import pandas as pd
import requests
import gzip
# Set page config for a premium cinematic layout
st.set_page_config(
    page_title="CineMatch - AI Movie Recommender",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Custom CSS for modern glassmorphism, responsive grids, and fluid hover effects
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Global styles */
    .stApp {
        background: linear-gradient(135deg, #09090e 0%, #14121f 50%, #0d0c13 100%);
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
    }
    
    /* Header styling */
    .app-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #ff3366, #ff9933);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    
    .app-subtitle {
        text-align: center;
        color: #b0aebc;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    /* Glassmorphic card styling for selected movie details */
    .hero-container {
        position: relative;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 3rem;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        display: flex;
        gap: 2.5rem;
        overflow: hidden;
    }
    .hero-backdrop {
        position: absolute;
        top: 0;
        right: 0;
        width: 60%;
        height: 100%;
        background-size: cover;
        background-position: center;
        opacity: 0.15;
        mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);
        -webkit-mask-image: linear-gradient(to left, rgba(0,0,0,1) 0%, rgba(0,0,0,0) 100%);
        pointer-events: none;
    }
    .hero-poster {
        width: 220px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        z-index: 1;
        flex-shrink: 0;
    }
    .hero-details {
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    .hero-meta {
        display: flex;
        gap: 1rem;
        align-items: center;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
        color: #d1ceda;
    }
    .rating-badge {
        background: #ffcc00;
        color: #000000;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: bold;
    }
    .genre-tag {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
    }
    .hero-overview {
        color: #b0aebc;
        line-height: 1.6;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    /* Recommendations Grid styling */
    .recs-heading {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        color: #ffffff;
        border-left: 4px solid #ff3366;
        padding-left: 0.75rem;
    }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 3rem;
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        display: flex;
        flex-direction: column;
    }
    .movie-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 51, 102, 0.4);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.4), 0 0 15px rgba(255, 51, 102, 0.1);
    }
    .card-img-wrapper {
        position: relative;
        width: 100%;
        padding-top: 150%; /* 2:3 aspect ratio */
        background-color: #1a1a24;
    }
    .card-img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-info {
        padding: 0.9rem;
        display: flex;
        flex-direction: column;
        flex-grow: 1;
        justify-content: space-between;
    }
    .card-title {
        font-size: 0.72rem;
        font-weight: 600;
        margin: 0 0 0.4rem 0;
        color: #ffffff;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2;
    }
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.72rem;
        color: #b0aebc;
        margin-top: auto;
    }
    .card-rating {
        display: flex;
        align-items: center;
        gap: 3px;
        color: #ffcc00;
        font-weight: 600;
    }
    /* Style Streamlit components to match the custom theme */
    div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }
    .stSelectbox label {
        color: #b0aebc !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)
# 1. Load Data with Caching
@st.cache_data
def load_data():
    with open('movies.pkl', 'rb') as f:
        movies_df = pickle.load(f)
    with gzip.open('similarity.pkl.gz', 'rb') as f:
        similarity_matrix = pickle.load(f)
    return movies_df, similarity_matrix
try:
    movies, similarity = load_data()
except Exception as e:
    st.error(f"Error loading data files: {e}")
    st.stop()
# 2. TMDB API Helper Function
API_KEY = st.secrets.get("TMDB_API_KEY", "")
if not API_KEY:
    st.error("TMDB API Key not found. Please set 'TMDB_API_KEY' in your `.streamlit/secrets.toml` file or Streamlit deployment secrets.")
    st.stop()
@st.cache_data
def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            backdrop_path = data.get('backdrop_path')
            return {
                'poster': f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&q=80&w=500",
                'backdrop': f"https://image.tmdb.org/t/p/original{backdrop_path}" if backdrop_path else "",
                'overview': data.get('overview', 'No description available.'),
                'rating': round(data.get('vote_average', 0.0), 1),
                'release_year': data.get('release_date', '').split('-')[0] if data.get('release_date') else 'N/A',
                'genres': [g['name'] for g in data.get('genres', [])][:3]
            }
    except Exception:
        pass
    return {
        'poster': "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&q=80&w=500",
        'backdrop': "",
        'overview': "No description available.",
        'rating': 0.0,
        'release_year': 'N/A',
        'genres': []
    }
# 3. Recommendation Function
def get_recommendations(movie_title):
    try:
        index = movies[movies['title'] == movie_title].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recs = []
        # Get top 6 recommendations (excluding itself)
        for i in distances[1:7]:
            recs.append(movies.iloc[i[0]])
        return recs
    except Exception as e:
        st.error(f"Error computing recommendations: {e}")
        return []
# --- Header ---
st.markdown('<div class="app-title">CineMatch</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Discover your next cinematic adventure with AI-powered suggestions</div>', unsafe_allow_html=True)
# --- Selection Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie_title = st.selectbox(
        "Choose a movie you love:",
        movies['title'].values,
        index=0
    )
st.markdown("<br>", unsafe_allow_html=True)
# --- Active Movie Hero Display ---
if selected_movie_title:
    # Find active movie details
    active_movie = movies[movies['title'] == selected_movie_title].iloc[0]
    active_details = fetch_movie_details(active_movie['movie_id'])
    
    genres_html = "".join([f'<span class="genre-tag">{g}</span>' for g in active_details['genres']])
    
    hero_html = f"""
    <div class="hero-container">
        <div class="hero-backdrop" style="background-image: url('{active_details['backdrop']}');"></div>
        <img class="hero-poster" src="{active_details['poster']}" alt="{selected_movie_title}">
        <div class="hero-details">
            <h2 class="hero-title">{selected_movie_title}</h2>
            <div class="hero-meta">
                <span class="rating-badge">★ {active_details['rating']}</span>
                <span>📅 {active_details['release_year']}</span>
                {genres_html}
            </div>
            <p class="hero-overview">{active_details['overview']}</p>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)
    
    # --- Recommendations Section ---
    st.markdown('<div class="recs-heading">Recommended Movies For You</div>', unsafe_allow_html=True)
    
    recs = get_recommendations(selected_movie_title)
    
    if recs:
        grid_html = '<div class="grid-container">'
        for rec in recs:
            rec_details = fetch_movie_details(rec['movie_id'])
            card_html = f"""
            <div class="movie-card">
                <div class="card-img-wrapper">
                    <img class="card-img" src="{rec_details['poster']}" alt="{rec['title']}">
                </div>
                <div class="card-info">
                    <h3 class="card-title">{rec['title']}</h3>
                    <div class="card-footer">
                        <span>📅 {rec_details['release_year']}</span>
                        <span class="card-rating">★ {rec_details['rating']}</span>
                    </div>
                </div>
            </div>
            """
            # Clean formatting to avoid Markdown block-code parsing issues
            grid_html += card_html.replace('\n', '').strip()
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
