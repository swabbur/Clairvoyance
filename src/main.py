import operations as op
import parsers as pr
import statistics as st


(identifiers, ratings) = pr.from_csv("./res/flavor_ratings.csv")
(user_count, item_count) = ratings.shape

pairs = op.generate_pairs(user_count)
measures = [st.pearson_r, st.kendall_tau_b]

similarities = op.compute_similarities(ratings, pairs, measures)

matching = op.match_pairs(pairs, similarities, 0.608)

for match in matching:
    identifier_1 = identifiers[match[0][0]]
    identifier_2 = identifiers[match[0][1]]
    match_similarity = match[1]
    print("%s %s %.2f" % (identifier_1, identifier_2, match_similarity))

# TODO: Format output
# 1.  oonger  1.00    (Boon, Jager)
# 2.  sonung  0.91    (Larson, Hung)
# 3.  eraiou  0.91    (Cabrera,Demetriou)
# 4.  linese  0.40    (Palin, Cleese)
# 5.  mandle  -0.45   (Chapman, Idle)
