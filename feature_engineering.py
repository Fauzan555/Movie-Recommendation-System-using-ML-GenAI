import ast

import ast

def extract_names(text):
    try:
        return " ".join([i['name'] for i in ast.literal_eval(text)])
    except:
        return ""

def create_features(df):
    df = df[['original_title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    df.dropna(inplace=True)

    for col in ['genres', 'keywords', 'cast', 'crew']:
        df[col] = df[col].apply(extract_names)

    df['content'] = (
        df['overview'] + " " +
        df['genres'] + " " +
        df['keywords'] + " " +
        df['cast'] + " " +
        df['crew']
    )

    return df