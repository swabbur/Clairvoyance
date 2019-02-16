import statistics as st
import networkx as nx


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


def match_pairs(pairs, similarities, threshold=0.5):

    graph = nx.Graph()

    for (i, j), similarity in zip(pairs, similarities):
        if similarity > threshold:
            graph.add_edge(i, j, weight=similarity)

    matching = nx.algorithms.matching.max_weight_matching(graph, True)

    return [((match[0], match[1]), graph[match[0]][match[1]]["weight"]) for match in matching]
