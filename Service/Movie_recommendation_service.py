import numpy as np 
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from Resources.Movie import Movie
import copy
import os
import dill as pickle
import time

class Movie_recommendation_service():

    def __init__(self, movie_name):
        self.filepath = "mymoviedb.csv"
        self.movie_name = movie_name
        self.selected_features = ["Title", "Overview", "Genre"]
        self.combiend_feature = pd.DataFrame()
        with open('similarity.npy', 'rb') as f:
            self.similarity = np.load(f)



    def data_process(self):
        self.movie_data = pd.read_csv("%s" % self.filepath, lineterminator='\n')
        for feature in self.selected_features:
            self.movie_data[feature] = self.movie_data[feature].fillna("")
        self.combined_features = self.movie_data['Title'] + self.movie_data['Overview'] + self.movie_data['Genre']
        # self.movie_data['combined_features'] = self.combined_features
        # self.movie_data.to_csv("processed.csv")
    def get_similarity(self):
        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(self.combined_features)
        self.similarity = cosine_similarity(feature_vectors)
        # with open('similarity.npy', 'wb') as f:
        #     np.save(f, self.similarity)
        # print(type(self.similarity))
        # f = open("similarity", 'wb')
        # f.write(self.similarity)
        # f.close()


    def find_close_match(self):
        list_of_all_titles = self.movie_data["Title"].tolist()
        find_close_match = difflib.get_close_matches(self.movie_name, list_of_all_titles)
        self.close_match = find_close_match[0]

    def get_similar_movies(self):
        index_of_movie = self.movie_data[self.movie_data.Title == self.close_match]
        index_of_movie = index_of_movie.index.tolist()[0]
        similarity_score = list(enumerate(self.similarity[index_of_movie]))
        sorted_similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similar_movies = []
        i = 1
        for movie in sorted_similarity_score:
            index = movie[0]
            title = self.movie_data[self.movie_data.index == index]["Title"].values[0]
            overview = self.movie_data[self.movie_data.index == index]["Overview"].values[0]
            vote_average = self.movie_data[self.movie_data.index == index]["Vote_Average"].values[0]
            poster_url = self.movie_data[self.movie_data.index == index]["Poster_Url"].values[0][36:]
            release_date = self.movie_data[self.movie_data.index == index]["Release_Date"].values[0]
            if (i < 21):
                movie = Movie(title,
                              overview,
                              vote_average,
                              poster_url,
                              release_date)
                similar_movies.append(copy.copy(movie.__dict__))
                i += 1
            else:
                break
        return json.dumps(similar_movies)

    def get_recommendation(self):
        self.data_process()
        # t1 = time.time()
        # self.get_similarity()
        # t2 = time.time()
        # print(t2-t1)
        self.find_close_match()
        movies = self.get_similar_movies()
        return movies
if __name__ == "__main__":
    movie_recommendation_service = Movie_recommendation_service("iron man")
    movies = movie_recommendation_service.get_recommendation()
# #
# print(json.dumps(movies))

# movie_name = "iron man"
#
#
# def data_processing(filepath):
#     movie_data = pd.read_csv("%s"%filepath, lineterminator='\n')
#     return movie_data
#
#
# movie_data= data_processing("../mymoviedb.csv")
#
# selected_features = ["Title","Overview","Genre"]
#
# for feature in selected_features:
#     movie_data[feature] = movie_data[feature].fillna("")
#
# combined_features = movie_data['Title'] + movie_data['Overview'] + movie_data['Genre']
#
# vectorizer = TfidfVectorizer()
# feature_vectors = vectorizer.fit_transform(combined_features)
#
# similarity = cosine_similarity(feature_vectors)
#
# list_of_all_titles = movie_data["Title"].tolist()
# find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
# close_match = find_close_match[0]
#
# index_of_movie = movie_data[movie_data.Title==close_match]
# index_of_movie = index_of_movie.index.tolist()[0]
# similarity_score = list(enumerate(similarity[index_of_movie]))
# sorted_similarity_score = sorted(similarity_score, key = lambda x:x[1], reverse = True)
# i = 1
# for movie in sorted_similarity_score:
#     index = movie[0]
#     title = movie_data[movie_data.index == index]["Title"].values[0]
#     if (i < 30):
#         print(i, title)
#         i += 1