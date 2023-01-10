from Service.Movie_recommendation_service import Movie_recommendation_service
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

filepath = "mymoviedb.csv"
movie_data = pd.read_csv("%s" %filepath, lineterminator='\n')
movie_data = movie_data[:1000]
combined_features = movie_data['Title'] + movie_data['Overview'] + movie_data['Genre']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)
with open('similarity.npy', 'wb') as f:
    np.save(f, similarity)