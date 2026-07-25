# 🍿 CineMatch — AI Movie Recommender System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CineMatch** is a premium, AI-powered movie recommendation web application built with Streamlit. It uses content-based filtering (cosine similarity) on the TMDB 5000 Movies dataset to suggest films similar to the ones you love. The app dynamically fetches live movie posters, backdrops, overview details, ratings, and genres in real-time from the TMDB API.

---

## ✨ Features

- **Modern UI/UX**: Cinematic dark mode layout featuring glassmorphism cards, responsive recommendation grids, fluid hover scales, and smooth transitions.
- **Content-Based Filtering**: Recommends top movies based on tag similarities computed from movie genres, keywords, cast, crew, and overview descriptions.
- **TMDB API Integration**: Dynamically pulls the latest poster, backdrop, release date, rating, and genres for the selected movie and all recommended options.
- **High Performance**: Employs Streamlit caching (`@st.cache_data`) for instantaneous data loading and API requests.
- **GitHub Ready**: The massive 184.7 MB float64 similarity matrix has been optimized (converted to `float32` and gzipped) to a lightweight **36.5 MB** file, ensuring fast cloning and compatibility with GitHub's file size limits without requiring Git LFS.

---

## 🛠️ Project Structure

```text
├── .gitignore               # Excludes large files, cache, and virtual environments
├── app.py                   # Streamlit web application code (UI & logic)
├── movies.pkl               # Pickled pandas DataFrame containing cleaned movie metadata
├── similarity.pkl.gz        # Gzipped float32 similarity matrix (36.5 MB)
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```

---

## 🚀 Setup & Installation

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/movie-recommender-system.git
cd movie-recommender-system
```

### 2. Create and Activate a Virtual Environment (Optional but recommended)
- **Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
This will spin up a local development server and open the app in your default web browser (usually at `http://localhost:8501`).

---

## ⚙️ TMDB API Configuration (Optional)
The application comes preconfigured with a developer API key to fetch posters and metadata. If you wish to use your own TMDB API key:
1. Obtain an API key from [The Movie Database (TMDB)](https://www.themoviedb.org/).
2. Open `app.py` and replace the value of `API_KEY` on line 229:
   ```python
   API_KEY = "your_tmdb_api_key_here"
   ```

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
