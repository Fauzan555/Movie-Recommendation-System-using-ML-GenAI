import pandas as pd

def load_data():
    movies = pd.read_csv(r"C:\PROJECTS\Moview recommendar\Data\tmdb_5000_movies.csv")
    credits = pd.read_csv(r"C:\PROJECTS\Moview recommendar\Data\tmdb_5000_credits.csv")

    credits.rename(columns={"movie_id": "id"}, inplace=True)
    df = movies.merge(credits, on="id")

    return df