import unittest

from prediction.movie_lens import MovieLens


class TestMovieLens(unittest.TestCase):

    def test_print(self):
        MovieLens.print('../data-set/ml-latest-small/README.txt')

    def test_load_ratings(self):
        user_ratings = MovieLens.load_ratings('../data-set/ml-latest-least/')
        for key, value in user_ratings.items():
            print(key, value)

    def test_load_movie_genres(self):
        movie_genres, genres_movies = MovieLens.load_movie_genres('../data-set/ml-latest-least/')
        print(movie_genres)
        # print(genres_moviess)
        for key, value in genres_movies.items():
            print(key, value)

    def test_load_movie_tag(self):
        tag_movies, movie_tags = MovieLens.load_movie_tag('../data-set/ml-latest-small/')
        print(tag_movies)
        print(movie_tags)