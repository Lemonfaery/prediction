import csv
import os


class MovieLens:

    @staticmethod
    def print(file_url):
        with open(file_url, 'r') as f:
            data = csv.reader(f)
            for row in data:
                print(row)

    @staticmethod
    def load_ratings(path):
        user_ratings = dict()
        with open(path, 'r') as f:
            data = csv.reader(f)
            next(data)  # skip header row
            for line in data:
                user_id, movie_id, rating = line[0], line[1], float(line[2])

                if user_id in user_ratings:
                    ratings = user_ratings[user_id]
                else:
                    ratings = dict()
                    user_ratings[user_id] = ratings
                ratings[movie_id] = rating

        return user_ratings

    @staticmethod
    def load_movie_genres(path):
        movie_genres = dict()
        genres_movies = dict()
        with open(os.path.join(path, 'movies.csv'), 'r') as f:
            data = csv.reader(f)
            next(data)  # skip header row
            for line in data:
                movie_id, genres_s = line[0], line[2]
                genres_s_list = genres_s.split('|')

                movie_genres[movie_id] = genres_s_list

                for _, genres in enumerate(genres_s_list):
                    if genres in genres_movies:
                        movies = genres_movies[genres]
                    else:
                        movies = set()
                        genres_movies[genres] = movies
                    movies.add(movie_id)

        return movie_genres, genres_movies

    @staticmethod
    def load_movie_tag(path):
        tag_movies = dict()
        movie_tags = dict()
        with open(os.path.join(path, 'tags.csv'), 'r') as f:
            data = csv.reader(f)
            next(data)  # skip header row
            for line in data:
                movie_id, tag = line[1], line[2]

                # 解析tag_movies
                if tag in tag_movies:
                    movies = tag_movies[tag]
                else:
                    movies = set()
                    tag_movies[tag] = movies
                movies.add(movie_id)

                # 解析movie_tags
                if movie_id in movie_tags:
                    tags = movie_tags[movie_id]
                else:
                    tags = set()
                    movie_tags[movie_id] = tags
                tags.add(tag)
        return tag_movies, movie_tags



