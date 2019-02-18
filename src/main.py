import operations as op
import parsers as ps
import statistics as st


(identifiers, ratings) = ps.from_csv("./res/flavor_ratings.csv")
(user_count, item_count) = ratings.shape

measures = [st.pearson_r, st.kendall_tau_b]
threshold = 0.6

pairs = op.generate_pairs(user_count)
similarities = op.compute_similarities(ratings, pairs, measures)
matching = op.match_pairs(user_count, pairs, similarities, threshold)

op.print_matching(matching, identifiers)
