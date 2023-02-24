from collections import namedtuple
from random import random

PROBABILITY = 0.2 # Must be from 0 to 1
M = 4 # Strings i
N = 5 # Сolumns j

class Node(object):
    

    def __init__(self, i: int, j: int):

        Position = namedtuple("Position", "i j")
        self.position = Position(i, j)
        is_on_border = i == 0 or i == M - 1 or j == 0 or j == N - 1


class Link(Node):

    def __init__(self, first_node: Node, second_node: Node):

        self.nodes = (first_node, second_node)
        self.is_open = random() <= PROBABILITY


class Grid(Node):
    

    def __init__(self):

        Size = namedtuple("Size", "M N")
        self.size = Size(M, N)

        self.nodes_matrix = []
        self.links_list = []
        for i in range(M):
            self.nodes_matrix.append([])
            for j in range(N):
                new_node = Node(i, j)
                self.nodes_matrix[i].append(new_node)
                self.links_list.append([new_node, []])

        
        for i in range(M):
            for j in range(N):
                if i != M - 1:
                    new_link = Link()


def main():
    
    new_grid = Grid(4, 5)

    for i in range(4):
        print("[", end="")
        for j in range(5):
            print(new_grid.nodes_matrix[i][j].position, end=" ")
        print("]")

    return 0


if __name__ == "__main__":
    main()
