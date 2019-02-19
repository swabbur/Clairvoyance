import networkx as nx
import scipy as sp
import statistics as st


def generate_pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def compute_similarities(ratings, pairs, measures, weights):

    user_count = len(ratings)

    similarities = sp.empty((user_count, user_count))
    similarities[:] = sp.nan

    for (i, j) in pairs:
        measurements = [measure(ratings[i], ratings[j]) for measure in measures]
        similarity = sp.dot(measurements, weights) / sp.sum(weights)
        similarities[i][j] = similarity
        similarities[j][i] = similarity

    for index in range(user_count):
        similarities[index] = st.normalize(similarities[index])

    return similarities


def match_pairs(user_count, pairs, similarities, threshold):

    graph = nx.Graph()
    for (i, j) in pairs:
        if similarities[i][j] > threshold and similarities[j][i] > threshold:
            similarity = (similarities[i][j] + similarities[j][i]) / 2
            graph.add_edge(i, j, weight=similarity)

    graph_matching = nx.algorithms.matching.max_weight_matching(graph, True)

    matching = []
    for (i, j) in graph_matching:
        similarity = min(similarities[i][j], similarities[j][i])
        matching.append(([i, j], similarity))

    if user_count & 1:

        users = set(range(user_count))
        matched_users = {user for (pair, _) in matching for user in pair}
        unmatched_user = (users - matched_users).pop()

        maximum_similarity = 0
        maximum_index = 0

        for index, match in enumerate(matching):

            selection = sorted(match[0] + [unmatched_user])

            similarity = (
                similarities[selection[0]][selection[1]]
                + similarities[selection[1]][selection[0]]
                + similarities[selection[0]][selection[2]]
                + similarities[selection[2]][selection[0]]
                + similarities[selection[1]][selection[2]]
                + similarities[selection[2]][selection[1]]
            ) / 6

            if similarity > maximum_similarity:
                maximum_similarity = similarity
                maximum_index = index

        matching[maximum_index] = (matching[maximum_index][0] + [unmatched_user], maximum_similarity)

    return matching


def print_matching(matching, identifiers):

    matching.sort(key=lambda m: -m[1])

    result = ""
    for index, match in enumerate(matching):

        names = []
        for i in match[0]:
            names.append(identifiers[i])

        similarity = match[1]

        suffix_size = int(6 / len(names))
        group_name = ""
        for name in names:
            group_name += name[-suffix_size:]

        result += "%i.\t%s\t%.2f\t(%s)\n" % (index + 1, group_name, similarity, ", ".join(names))

    return result
