from flask import Flask
from flask_cors import CORS
import sys
sys.path.append("..")
app = Flask(__name__)
CORS(app)
# import Service.Movie_recommendation_service
from Service.Movie_recommendation_service import Movie_recommendation_service

@app.route("/<movie_name>")
def hello_world(movie_name):
    return  movie_name

@app.route("/get_recommendations/<movie_name>")
def get_recommendations(movie_name):
    movie_recommendation_service = Movie_recommendation_service (movie_name)
    movies = movie_recommendation_service.get_recommendation()
    return movies

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)