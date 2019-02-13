import scipy
import scipy.sparse as sparse
from decorators import cache, timer


# noinspection PyShadowingNames
@timer
@cache(name="normalized")
def normalize(ratings):

    (user_count, item_count) = ratings.shape
    mean = ratings.sum() / (ratings != 0).sum()

    user_baselines = scipy.zeros((user_count, 1))
    for index, row in enumerate(ratings):
        if index % 500 == 0:
            print("User " + str(index) + "/" + str(user_count))
        nnz = (row != 0).sum()
        if nnz > 0:
            user_baselines[index] = (row.sum() / nnz) - mean

    item_baselines = scipy.zeros((item_count, 1))
    for index in range(0, item_count):
        if index % 500 == 0:
            print("Item " + str(index) + "/" + str(item_count))
        column = ratings.getcol(index)
        nnz = (column != 0).sum()
        if nnz > 0:
            item_baselines[index] = ((column - user_baselines).sum() / nnz) - mean

    normalized_ratings = ratings.copy()

    for user_index in range(0, 4):
        if user_index % 500 == 0:
            print("User " + str(user_index) + "/" + str(user_count))
        for item_index in range(0, 4):
            rating = ratings[user_index, item_index]
            if rating != 0:
                user_baseline = user_baselines[user_index]
                item_baseline = item_baselines[item_index]
                normalized_rating = rating - mean - user_baseline - item_baseline
                normalized_ratings[user_index, item_index] = normalized_rating

    return normalized_ratings


if __name__ == '__main__':

    ratings = sparse.load_npz("./res/books.npz")
    normalized_ratings = normalize(ratings)

    print(ratings)
    print(normalized_ratings)
