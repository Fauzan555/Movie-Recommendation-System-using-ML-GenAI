from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, df):
        self.df = df

        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(df['content'])
        self.similarity = cosine_similarity(self.tfidf_matrix)

    def recommend(self, title, top_n=5):
        idx = self.df[self.df['original_title'] == title].index[0]
        scores = list(enumerate(self.similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

        return self.df.iloc[[i[0] for i in scores]][['original_title', 'overview']]