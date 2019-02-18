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
        for index, match in enumerate(matching):

            selection = match[0] + [unmatched_user]
            selection.sort()

            average_similarity = (
                similarity_map[(selection[0], selection[1])]
                + similarity_map[(selection[0], selection[2])]
                + similarity_map[(selection[1], selection[2])]
            ) / 3

            if average_similarity > maximum_similarity:
                maximum_similarity = average_similarity
                maximum_index = index

        matching[maximum_index] = (matching[maximum_index][0] + [unmatched_user], maximum_similarity)

    return matching


def print_matching(matching, identifiers):

    matching.sort(key=lambda m: -m[1])

    for index, match in enumerate(matching):

        names = []
        for i in match[0]:
            names.append(identifiers[i])

        similarity = match[1]

        suffix_size = int(6 / len(names))
        group_name = ""
        for name in names:
            group_name += name[-suffix_size:]

        print("%i.\t%s\t%.2f\t(%s)" % (index + 1, group_name, similarity * 2 - 1, ", ".join(names)))
