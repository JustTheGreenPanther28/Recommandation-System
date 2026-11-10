# Movie Recommendation System

A content-based movie recommender built with Python and Streamlit. Pick a movie and get 5 similar suggestions with posters fetched from the TMDB API.

**Live demo:** https://recommandation-system.streamlit.app/

## How it works

1. The TMDB 5000 movies and credits datasets are merged and cleaned in the notebook.
2. For each movie, the genres, keywords, overview, top 3 cast members and the director are combined into a single text "tag". Names are joined into one token (for example `JamesCameron`) so different people with the same first name are not confused.
3. Tags are lowercased and stemmed with NLTK's Porter stemmer, so words like "activity" and "activities" count as the same word.
4. Tags are converted to vectors with scikit-learn's `CountVectorizer` (top 5,000 words, English stop words removed), and cosine similarity is computed between every pair of movies.
5. For a selected movie, the app picks the 5 most similar ones and fetches their posters from the TMDB API.

## Tech stack

- Python
- Pandas, NumPy
- scikit-learn (CountVectorizer and cosine similarity)
- NLTK (Porter stemmer)
- Streamlit (web UI and deployment)
- TMDB API (movie posters)

## Project structure

```
Recommandation System/
├── Recommandation System.ipynb   # data cleaning, feature engineering, similarity matrix
└── Frontend/
    ├── app.py                    # Streamlit app
    ├── requirements.txt
    ├── movies_dict.pkl           # movie titles and ids
    └── similarity.pkl            # similarity matrix (float16 to keep it small)
```

The raw TMDB CSV files are not included in this repo because of their size. You can download them from Kaggle ("TMDB 5000 Movie Dataset").

## Run locally

```bash
git clone https://github.com/JustTheGreenPanther28/Recommandation-System.git
cd Recommandation-System/Frontend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- The similarity matrix is stored as float16 so the file stays under GitHub's 100 MB limit. Rankings are practically unchanged.
- If posters show a "No Poster" placeholder, the TMDB API key in `app.py` may be rate-limited. Replace it with your own free key from https://www.themoviedb.org/settings/api.

## Author

Vedant Maheshwari
GitHub: [JustTheGreenPanther28](https://github.com/JustTheGreenPanther28)<img width="1442" height="796" alt="image" src="https://github.com/user-attachments/assets/fddfe706-20e2-4e66-9233-1d8fb093b166" />
