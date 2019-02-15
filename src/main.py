import pandas as pd
import scipy as sp
import networkx as nx
import statistics as st

data_frame = pd.read_csv("./res/flavor_ratings.csv")
data = data_frame.to_numpy()

identifiers = data[:, 0]
ratings = data[:, 1:].astype(sp.float64)
(user_count, item_count) = ratings.shape

print("Parsed ratings")

standardized_ratings = sp.empty(ratings.shape)

for index, row in enumerate(ratings):
    standardized_ratings[index] = st.standardize(row)

print("Standardized ratings")

pearson_similarities = []
kendall_similarities = []

for i in range(user_count):
    for j in range(i + 1, user_count):
        r = st.pearson_r(standardized_ratings[i], standardized_ratings[j])
        tau = st.kendall_tau_b(standardized_ratings[i], standardized_ratings[j])
        pearson_similarities.append(r)
        kendall_similarities.append(tau)

print("Computed similarities")

pearson_similarities = st.normalize(pearson_similarities)
kendall_similarities = st.normalize(kendall_similarities)

print("Normalized similarities")

graph = nx.Graph()

index = 0
for i in range(user_count):
    for j in range(i + 1, user_count):
        r = pearson_similarities[index]
        tau = kendall_similarities[index]
        similarity = (r + tau) / 2
        graph.add_edge(i, j, weight=similarity)
        index += 1

print("Created network")

matching = nx.algorithms.matching.max_weight_matching(graph, True)

print("Matched pairs")

print()
for match in matching:
    identifier_1 = identifiers[match[0]]
    identifier_2 = identifiers[match[1]]
    similarity = graph[match[0]][match[1]]["weight"]
    print("%s %s %.3f" % (identifier_1, identifier_2, similarity))
