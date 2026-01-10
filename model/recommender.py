import pandas as pd
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    def __init__(self, movies_path, credits_path):
        movies = pd.read_csv(movies_path)
        credits = pd.read_csv(credits_path)

        # merge datasets
        movies = movies.merge(credits, on="title")

        # select useful columns
        movies = movies[['title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        movies.dropna(inplace=True)

        # convert stringified lists to real lists
        movies['genres'] = movies['genres'].apply(self._convert)
        movies['keywords'] = movies['keywords'].apply(self._convert)
        movies['cast'] = movies['cast'].apply(self._convert_cast)
        movies['crew'] = movies['crew'].apply(self._convert_director)

        # combine everything into one tag
        movies['tags'] = (
            movies['overview'] + " " +
            movies['genres'] + " " +
            movies['keywords'] + " " +
            movies['cast'] + " " +
            movies['crew']
        )

        self.movies = movies[['title', 'tags']]
        self.movies['tags'] = self.movies['tags'].str.lower()

        # vectorization
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
        self.vectors = self.vectorizer.fit_transform(self.movies['tags'])

        # similarity matrix
        self.similarity = cosine_similarity(self.vectors)

    def _convert(self, obj):
        L = []
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return " ".join(L)

    def _convert_cast(self, obj):
        L = []
        for i in ast.literal_eval(obj)[:5]:  # top 5 actors
            L.append(i['name'])
        return " ".join(L)

    def _convert_director(self, obj):
        L = []
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                L.append(i['name'])
        return " ".join(L)

    def recommend(self, movie, n=5):
        movie = movie.lower()
        titles = self.movies['title'].str.lower()

        if movie not in titles.values:
            return []

        index = titles[titles == movie].index[0]
        distances = self.similarity[index]

        movies_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:n+1]

        return [self.movies.iloc[i[0]].title for i in movies_list]
