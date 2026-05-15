import streamlit as st
from data_loader import load_data
from feature_engineering import create_features
from recommender import MovieRecommender
from explain import generate_explanation

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Cinematic AI Recommender",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* --- GLOBAL THEME --- */
    /* UPDATED: Removed pure black. Used a subtle linear gradient for depth */
    .stApp {
        background: linear-gradient(to bottom, #1f1f1f 0%, #0a0a0a 100%);
        background-attachment: fixed; /* Ensures gradient fills full scroll */
        color: #f0f0f0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* --- TYPOGRAPHY --- */
    h1 {
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    h2, h3 {
        font-weight: 600;
        color: #e5e5e5;
    }
    p {
        color: #b3b3b3;
        line-height: 1.6;
    }

    /* --- HEADER STYLING --- */
    .header-subtitle {
        text-align: center;
        color: #E50914; /* Cinematic Red */
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
    }

    /* --- INPUT SECTION --- */
    .stSelectbox label {
        color: #ffffff !important;
        font-weight: bold;
    }
    /* Style the selectbox container */
    div[data-baseweb="select"] > div {
        background-color: #2b2b2b; /* Slightly lighter than bg */
        color: white;
        border: 1px solid #444;
        border-radius: 8px;
    }
    /* Dropdown menu items */
    ul[data-baseweb="menu"] {
        background-color: #2b2b2b !important;
    }

    /* --- BUTTON STYLING --- */
    .stButton > button {
        width: 100%;
        background-color: #E50914;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(0,0,0, 0.3);
    }
    .stButton > button:hover {
        background-color: #ff0f1f;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4);
    }

    /* --- MOVIE CARD CONTAINER --- */
    .movie-card {
        background: linear-gradient(135deg, #252525 0%, #1a1a1a 100%);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid #333;
        /* Enhanced shadow for depth against the gradient bg */
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .movie-card:hover {
        transform: translateY(-3px);
        border-color: #555;
    }
    .movie-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 10px;
        color: #fff;
    }
    .movie-overview {
        font-size: 0.95rem;
        color: #cccccc;
        margin-bottom: 15px;
        font-weight: 300;
    }

    /* --- EXPLANATION BOX (ST.INFO) --- */
    .stAlert {
        background-color: #222;
        color: #e0e0e0;
        border: 1px solid #444;
        border-left: 5px solid #E50914;
        border-radius: 8px;
    }
    .stAlert > div > div > div > span {
        color: #E50914;
    }

    /* Remove top padding */
    .block-container {
        padding-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. APP LOGIC
# -----------------------------------------------------------------------------

st.markdown("<h1>🎬 Explainable Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>AI-Powered Personalization</p>", unsafe_allow_html=True)

with st.spinner("Loading library..."):
    df = load_data()
    df = create_features(df)
    recommender = MovieRecommender(df)

st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    movie = st.selectbox("Select a movie you love:", df['original_title'])
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_clicked = st.button("Get Recommendations")

# -----------------------------------------------------------------------------
# 4. RESULTS DISPLAY
# -----------------------------------------------------------------------------
if recommend_clicked:
    results = recommender.recommend(movie)

    st.markdown(
        "<br><h3 style='text-align: center; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 10px;'>Top Picks For You</h3>",
        unsafe_allow_html=True)

    for _, row in results.iterrows():
        with st.container():
            # Card HTML
            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title">{row['original_title']}</div>
                <div class="movie-overview">{row['overview']}</div>
            </div>
            """, unsafe_allow_html=True)

            # AI Explanation
            st.info(f"**Why this movie?** \n\n {generate_explanation(movie, row['original_title'], row['overview'])}")

            # Spacer
            st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)