import operations as op
import parsers as pr
import statistics as st


(identifiers, ratings) = pr.from_csv("./res/flavor_ratings.csv")
(user_count, item_count) = ratings.shape

measures = [st.pearson_r, st.kendall_tau_b]
threshold = 0.6

pairs = op.generate_pairs(user_count)
similarities = op.compute_similarities(ratings, pairs, measures)
matching = op.match_pairs(user_count, pairs, similarities, threshold)

matching.sort(key=lambda m: -m[1])

for index, match in enumerate(matching):
    names = []
    for i in match[0]:
        names.append(identifiers[i])

    match_similarity = match[1]
    print("%i.\t%.2f\t%s" % (index + 1, match_similarity, tuple(names)))

# TODO: Format output
# 1.  oonger  1.00    (Boon, Jager)
# 2.  sonung  0.91    (Larson, Hung)
# 3.  eraiou  0.91    (Cabrera, Demetriou)
# 4.  linese  0.40    (Palin, Cleese)
# 5.  mandle  -0.45   (Chapman, Idle)
