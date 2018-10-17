import datetime
import os
import shutil
import time

from prediction import config
from prediction.movie_lens import MovieLens
from prediction.predict import Predict


def main():
    start_time = datetime.datetime.now()

    # 创建工作目录：程序运行中间结果将会保存到该目录下
    workspace_dir = os.path.join(config.workspace_path, time.strftime("%Y%m%d%H%M%S", time.localtime()))
    if os.path.exists(workspace_dir):
        shutil.rmtree(workspace_dir)
    os.makedirs(workspace_dir)

    # step 1: slope one
    # 解析 用户（userID) 与 评分
    user_ratings = MovieLens.load_ratings(os.path.join(config.movielens_path, 'ratings.csv'))
    print('参与评分用户总数：', len(user_ratings))

    # 解析 电影（movieID) 与 电影类别（genres)
    movie_genres, genres_movies = MovieLens.load_movie_genres(config.movielens_path)
    print('电影总数：', len(movie_genres))
    print('类别总数：', len(genres_movies))

    predict = Predict(user_ratings, movie_genres, genres_movies)
    predict.save_compute_deviations(os.path.join(config.movielens_path, 'ratings.csv'),
                                    workspace_dir + '/ratings')
    predict.save_predict(os.path.join(workspace_dir, 'slope_one_ratings.csv'))

    end_time = datetime.datetime.now()
    print('程序运行时间：', (end_time - start_time).seconds, '秒')


if __name__ == '__main__':
    main()
