import networkx as nx
import statistics as st


def generate_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def compute_similarities(ratings, pairs, measures):

    similarities = []

    for measure in measures:
        sub_similarities = []
        for (i, j) in pairs:
            similarity = measure(ratings[i], ratings[j])
            sub_similarities.append(similarity)
        similarities.append(sub_similarities)

    for index in range(len(similarities)):
        similarities[index] = st.normalize(similarities[index])

    averaged_similarities = []
    for index in range(len(pairs)):
        total = 0
        for similarity in similarities:
            total += similarity[index]
        averaged_similarities.append(total / len(similarities))

    return averaged_similarities


def match_pairs(user_count, pairs, similarities, threshold=0.5):

    graph = nx.Graph()
    for (i, j), similarity in zip(pairs, similarities):
        if similarity > threshold:
            graph.add_edge(i, j, weight=similarity)
    graph_matching = nx.algorithms.matching.max_weight_matching(graph, True)

    matching = []
    for match in graph_matching:
        i = match[0]
        j = match[1]
        similarity = graph[i][j]["weight"]
        matching.append(([i, j], similarity))

    if user_count & 1:

        users = set(range(user_count))
        matched_users = {user for (pair, similarity) in matching for user in pair}
        unmatched_user = (users - matched_users).pop()

        similarity_map = {pair: similarity for (pair, similarity) in zip(pairs, similarities)}

        maximum_similarity = 0
        maximum_index = 0
        for index, (pair, similarity_1) in enumerate(matching):

            if pair[0] < unmatched_user:
                similarity_2 = similarity_map[(pair[0], unmatched_user)]
            else:
                similarity_2 = similarity_map[(unmatched_user, pair[0])]

            if pair[1] < unmatched_user:
                similarity_3 = similarity_map[(pair[1], unmatched_user)]
            else:
                similarity_3 = similarity_map[(unmatched_user, pair[1])]

            average_similarity = (similarity_1 + similarity_2 + similarity_3) / 3

            if average_similarity > maximum_similarity:
                maximum_similarity = average_similarity
                maximum_index = index

        matching[maximum_index] = (matching[maximum_index][0] + [unmatched_user], maximum_similarity)

    return matching
