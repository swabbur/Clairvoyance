import operations as op
import parsers as ps
import statistics as st


(identifiers, ratings) = ps.from_csv("./res/flavor_ratings.csv")
(user_count, _) = ratings.shape

measures = [st.pearson_r, st.kendall_tau_b]
weights = [0.5, 0.5]
threshold = 0.75

pairs = op.generate_pairs(user_count)
similarities = op.compute_similarities(ratings, pairs, measures, weights)
matching = op.match_pairs(user_count, pairs, similarities, threshold)
result = op.print_matching(matching, identifiers)

with open("./res/result.txt", "w") as file:
    file.write(result)
