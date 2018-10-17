class SlopeOne(object):

    def __init__(self, data):
        self.data = data
        self.frequencies = {}
        self.deviations = {}

    def compute_deviations(self):
        for ratings in self.data.values():
            # for each item & rating in that set of ratings:
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                # for each item2 & rating2 in that set of ratings:
                for (item2, rating2) in ratings.items():
                    if item != item2:
                        # add the difference between the ratings to our
                        # computation
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0.0)
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating - rating2

        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]

    def predict(self, user_ratings):
        recommendations = {}
        frequencies = {}
        # for every item and rating in the user's recommendations
        for (userItem, user_rating) in user_ratings.items():
            # for every item in our dataset that the user didn't rate
            for (diff_item, diff_ratings) in self.deviations.items():
                if diff_item not in user_ratings and \
                        userItem in self.deviations[diff_item]:
                    freq = self.frequencies[diff_item][userItem]
                    recommendations.setdefault(diff_item, 0.0)
                    frequencies.setdefault(diff_item, 0)
                    # add to the running sum representing the numerator
                    # of the formula
                    recommendations[diff_item] += (diff_ratings[userItem] + user_rating) * freq
                    # keep a running sum of the frequency of diffitem
                    frequencies[diff_item] += freq
        # recommendations = [(k, v / frequencies[k]) for (k, v) in recommendations.items()]
        # # finally sort and return
        # recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        # # I am only going to return the first 50 recommendations
        predicts = dict()
        for k, v in recommendations.items():
            predicts[k] = v / frequencies[k]
        return predicts


