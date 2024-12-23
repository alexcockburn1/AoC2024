import itertools
from collections import defaultdict


def get_input(filename):
    with open(filename, "r") as f:
        return [line.strip().split("-") for line in f.readlines()]


def build_graph(puzzle_input):
    graph = defaultdict(set)
    for node_a, node_b in puzzle_input:
        graph[node_a].add(node_b)
        graph[node_b].add(node_a)
    return graph


def part1(graph):
    t_3_cliques = set()
    for v in graph:
        for n1 in graph[v]:
            for n2 in graph[v] - {n1}:
                if n2 in graph[n1]:
                    if any([node.startswith("t") for node in [v, n1, n2]]):
                        t_3_cliques.add(tuple(sorted([v, n1, n2])))
    print(f"Solution to part 1 is {len(t_3_cliques)}")


def part2(graph):
    clique_size = 1
    current_cliques = {(k,) for k in graph.keys()}
    previous_cliques = None
    while len(current_cliques) != 0:
        print(clique_size)
        # print(cliques)
        next_cliques = set()
        for clique in current_cliques:
            clique_neighbourhood = {neighbour for node in clique for neighbour in graph[node] if neighbour not in clique}
            for clique_neighbour in clique_neighbourhood:
                if all([clique_neighbour in graph[node] for node in clique]):
                    next_clique = tuple(sorted(clique + (clique_neighbour,)))
                    next_cliques.add(next_clique)
        previous_cliques = current_cliques
        current_cliques = next_cliques
        clique_size += 1
    assert len(previous_cliques) == 1
    largest_clique = next(iter(previous_cliques))
    password = ",".join(sorted(largest_clique))
    print(f"Solution to part 2 is {password}")


def main():
    puzzle_input = get_input("test_files/prob23_full_input.txt")
    graph = build_graph(puzzle_input)
    part1(graph)
    part2(graph)


if __name__ == "__main__":
    main()
