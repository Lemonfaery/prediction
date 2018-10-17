import unittest

from prediction.slope_one import SlopeOne


class TestSlopeOne(unittest.TestCase):
    users = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,
                          "Norah Jones": 4.5, "Phoenix": 5.0,
                          "Slightly Stoopid": 1.5, "The Strokes": 2.5,
                          "Vampire Weekend": 2.0},
             "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5,
                      "Deadmau5": 4.0, "Phoenix": 2.0,
                      "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
             "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0,
                      "Deadmau5": 1.0, "Norah Jones": 3.0,
                      "Phoenix": 5, "Slightly Stoopid": 1.0},
             "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0,
                     "Deadmau5": 4.5, "Phoenix": 3.0,
                     "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                     "Vampire Weekend": 2.0},
             "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0,
                        "Norah Jones": 4.0, "The Strokes": 4.0,
                        "Vampire Weekend": 1.0},
             "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0,
                        "Norah Jones": 5.0, "Phoenix": 5.0,
                        "Slightly Stoopid": 4.5, "The Strokes": 4.0,
                        "Vampire Weekend": 4.0},
             "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0,
                     "Norah Jones": 3.0, "Phoenix": 5.0,
                     "Slightly Stoopid": 4.0, "The Strokes": 5.0},
             "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0,
                          "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                          "The Strokes": 3.0}
             }

    users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
              "Ben": {"Taylor Swift": 5},
              "Clara": {"PSY": 3.5, "Whitney Houston": 4},
              "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

    users3 = dict(alice=dict(squid=1.0, cuttlefish=4.0), bob=dict(squid=1.0,cuttlefish=1.0, octupus=3.0))

    def test_ee(self):
        ratings_g1 = {"1": {"M1": 1.0, "M3": 2.0, "M5": 3.0, "M7": 4},
                      "3": {"M1": 8.0, "M3": 10},
                      "4": {"M5": 12, "M7": 14}}

        ratings_g2 = {"1": {"M1": 1.0, "M7": 4.0},
                      "2": {"M2": 5.0, "M6": 6.0},
                      "3": {"M1": 8.0, "M2": 9.0},
                      "4": {"M4": 11.0, "M7": 14.0}}

        ratings_g3 = {
            "1": {"M1": 1.0, "M3": 2.0},
            "2": {"M2": 5.0, "M6": 7.0},
            "3": {"M1": 8.0, "M2": 9.0, "M3": 10.0},
            "4": {"M6": 13.0}
        }

        data = ratings_g3
        predict_data = data['4']

        # r = recommender(data)
        # r.computeDeviations()
        # print(r.slopeOneRecommendations(predict_data))

        s = SlopeOne(data)
        s.compute_deviations()
        prediction = s.predict(predict_data)
        print(prediction)

    def test_slope_one(self):
        s = SlopeOne(self.users2)
        s.compute_deviations()
        prediction = s.predict(self.users2['Ben'])
        print(prediction)