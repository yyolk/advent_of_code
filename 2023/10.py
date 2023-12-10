from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, TypedDict, NewType


Node = NewType("Node", tuple[int, int])
Tube = NewType("Tube", tuple[Node, str])


@dataclass(frozen=True)
class Edge:
    tube: Tube
    node: Node


@dataclass(frozen=True)
class CurrentEdge:
    edge: Edge
    edges: dict[Node, set[Edge]]
    visited: set[Node]

    def __iter__(self):
        return self

    def __next__(self):
        # This is the start.
        if not self.visited:
            return self.edge

        for edge in self.edges[self.edge.node]:
            if edge.node not in self.visited:
                return edge


def parse_input(serialized_input: str) -> (set[Edge], dict[Node, set[Edge]]):
    edges: dict[Node, set[Edge]] = defaultdict(set[Edge])
    start: Tube

    y = 0
    for line in serialized_input.splitlines():
        x = 0
        for c in line:
            tube: Tube
            if c == "S":
                start = ((y, x), c)
            elif c != ".":
                tube = ((y, x), c)
                match c:
                    case "|":
                        vert_a = (1, 0, -1, 0)
                        vert_b = (-1, 0, 1, 0)
                    case "-":
                        vert_a = (0, 1, 0, -1)
                        vert_b = (0, -1, 0, 1)
                    case "L":
                        vert_a = (-1, 0, 0, 1)
                        vert_b = (0, 1, -1, 0)
                    case "J":
                        vert_a = (-1, 0, 0, -1)
                        vert_b = (0, -1, -1, 0)
                    case "7":
                        vert_a = (1, 0, 0, -1)
                        vert_b = (0, -1, 1, 0)
                    case "F":
                        vert_a = (1, 0, 0, 1)
                        vert_b = (0, 1, 1, 0)
                edges[(y + vert_a[0], x + vert_a[1])].add(
                    Edge(tube, (y + vert_a[2], x + vert_a[3]))
                )
                edges[(y + vert_b[0], x + vert_b[1])].add(
                    Edge(tube, (y + vert_b[2], x + vert_b[3]))
                )
            x += 2
        y += 2
    starts: set[Edge] = set()
    for i in [-1, 1]:
        if edges[(start[0][0] + i, start[0][1])]:
            starts.add(Edge(start, (start[0][0] + i, start[0][1])))
        if edges[(start[0][0], start[0][1] + i)]:
            starts.add(Edge(start, (start[0][0], start[0][1] + i)))
    return starts, edges


def find_path(starts: set[Edge], edges: dict[Node, set[Edge]]) -> list[Edge]:
    for start in starts:
        visited_edges: list[Edge] = list()
        visited_nodes: set[Node] = set()
        current: CurrentEdge = CurrentEdge(start, edges, visited_nodes)
        while next_edge := next(current):
            visited_edges.append(next_edge)
            visited_nodes.add(next_edge.node)
            current = CurrentEdge(next_edge, edges, visited_nodes)

        if sum(1 if s.node in visited_nodes else 0 for s in starts) == 2:
            return visited_edges


def farthest_distance(starts: set[Edge], edges: dict[Node, set[Edge]]) -> int:
    """Part 1"""
    return len(find_path(starts, edges)) // 2


def flood(starts: set[Edge], edges: dict[Node, set[Edge]]):
    """Part 2"""
    path: list[Edge] = find_path(starts, edges)
    visited: set[Node] = set()
    not_visited: set[Node] = set()

    all_nodes = set(p.node for p in path).union(p.tube[0] for p in path)

    max_a = max(n[0] for n in all_nodes)
    max_b = max(n[1] for n in all_nodes)

    for a in (0, max_a):
        for b in range(max_b + 1):
            if (a, b) not in all_nodes:
                not_visited.add((a, b))

    for b in (0, max_b):
        for a in range(max_a + 1):
            if (a, b) not in all_nodes:
                not_visited.add((a, b))

    outside = set()
    while not_visited:
        current = not_visited.pop()
        visited.add(current)
        if current not in all_nodes:
            outside.add(current)
            for i in (-1, 1):
                n = (current[0] + i, current[1])
                if 0 <= n[0] <= max_a and n not in visited:
                    not_visited.add(n)
                n = (current[0], current[1] + i)
                if 0 <= n[1] <= max_b and n not in visited:
                    not_visited.add(n)

    tubes = set((p.tube[0][0] // 2, p.tube[0][1] // 2) for p in path)
    outside_halved = set((o[0] // 2, o[1] // 2) for o in outside)

    max_y = max(max(n[0] for n in tubes), max(n[0] for n in outside_halved))
    max_x = max(max(n[1] for n in tubes), max(n[1] for n in outside_halved))

    not_inside = outside_halved.union(tubes)
    return (max_y + 1) * (max_x + 1) - len(not_inside)


with open("10.txt") as fp:
    puzzle_input = fp.read()
    print(farthest_distance(*parse_input(puzzle_input)))
    print(flood(*parse_input(puzzle_input)))
