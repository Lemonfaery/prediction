import os
import shutil
import time

from prediction.movie_lens import MovieLens
from prediction.slope_one import SlopeOne


class Predict(object):

    def __init__(self, user_ratings, movie_genres, genres_movies):
        self.genres_slope_ones = dict()
        self.user_ratings = user_ratings
        self.movie_genres = movie_genres
        self.genres_movies = genres_movies

    @staticmethod
    def save_ratings_by_genres(genres_movies, ratings_path, save_path, show_progress=True):
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)

        save_ratings_paths = dict()
        index, total_count = 0, len(genres_movies.keys())
        for genres, movies in genres_movies.items():
            index += 1
            genres_file_path = os.path.join(save_path, genres + '.csv')
            genres_file = open(genres_file_path, 'w')
            if show_progress:
                print('生成进度：', index, '/', total_count, genres_file_path)
            with open(ratings_path, 'r') as ratings_file:
                header = next(ratings_file)  # skip header row
                genres_file.writelines(header)

                for line in ratings_file:
                    movie_id = line.split(',')[1]
                    if movie_id in movies:
                        genres_file.writelines(line)
            save_ratings_paths[genres] = genres_file_path
        return save_ratings_paths

    def save_compute_deviations(self, ratings_path, save_path, show_progress=True):
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)

        if show_progress:
            print('开始根据类型计算差异值...')

        index, total = 0, len(self.genres_movies.keys())
        for genres, movies in self.genres_movies.items():
            index += 1
            genres_file_path = os.path.join(save_path, genres + '.csv')

            if show_progress:
                print('生成类型评分：', index, '/', total, genres_file_path)
            genres_file = open(genres_file_path, 'w')
            with open(ratings_path, 'r') as ratings_file:
                header = next(ratings_file)  # skip header row
                genres_file.writelines(header)

                for line in ratings_file:
                    movie_id = line.split(',')[1]
                    if movie_id in movies:
                        genres_file.writelines(line)
            genres_file.close()

            if show_progress:
                print('生成项目差异录：', index, '/', total)
            user_ratings = MovieLens.load_ratings(genres_file_path)
            slope_one = SlopeOne(user_ratings)
            slope_one.compute_deviations()
            self.genres_slope_ones[genres] = slope_one

        if show_progress:
            print('根据类型计算差异值完成')

    def save_predict(self, path, show_progress=True):
        print('开始生成用户评分...')
        # 根据slope one进行评分
        slope_one_ratings_file = open(path, 'w')
        slope_one_ratings_file.writelines('userId,movieId,rating,timestamp\n')
        movies_list = list(self.movie_genres.keys())
        index, total = 0, len(self.user_ratings.items())
        for user, ratings in self.user_ratings.items():
            index += 1
            if show_progress:
                print('生成用户评分：', index, '/', total, user)
            user_ratings_list = list(ratings.keys())
            user_not_rating_movies = list(set(movies_list).difference(set(user_ratings_list)))  # 用户未评分的电影条目集合
            for _, not_rating_movie_id in enumerate(user_not_rating_movies):
                predict_rate = self.predict(user, not_rating_movie_id)
                predict_rate = 0 if predict_rate < 0 else predict_rate
                if show_progress:
                    print('生成用户评分：', index, '/', total, user, not_rating_movie_id, predict_rate)
                slope_one_ratings_file.writelines(
                    '%s,%s,%s,%s\n' % (user, not_rating_movie_id, predict_rate, int(time.time())))
        slope_one_ratings_file.close()
        print('生成用户评分结束')

    def predict(self, user, movie_id):
        user_ratings_list = list(self.user_ratings[user].keys())
        # 用户u评分过的属于类型中任意一种类型的项目数量的综合
        user_rated_genres = set()
        for _, rated_movie_id in enumerate(user_ratings_list):
            user_rated_genres |= set(self.movie_genres[rated_movie_id])
        user_rated_movie_genres_movie_count = 0
        for genres in user_rated_genres:
            tem = list(self.genres_movies[genres])
            tem_list =  [i for i in user_ratings_list if i in tem]
            user_rated_movie_genres_movie_count += len(tem_list)
        #
        rating = 0
        for _, genres in enumerate(self.movie_genres[movie_id]):
            slope_one = self.genres_slope_ones[genres]
            if user in slope_one.data:
                # 用户u评分过的属于类型的项目的数量
                genres_movie_list = list(self.genres_movies[genres])
                user_rated_in_genres = [i for i in user_ratings_list if i in genres_movie_list]

                predict = slope_one.predict(slope_one.data[user])
                if movie_id in predict:
                    rating += predict[movie_id] * (len(user_rated_in_genres) / user_rated_movie_genres_movie_count)
        return rating
