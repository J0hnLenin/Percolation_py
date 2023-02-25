from collections import namedtuple
from random import random

PROBABILITY = 0.2 # Must be from 0 to 1
M = 4 # Strings i
N = 8 # Сolumns j

class Node(object):
    

    def __init__(self, i: int, j: int):

        Position = namedtuple("Position", "i j")
        self.position = Position(i, j)
        self.links = []
        
    def is_on_border(self) -> bool:
        return i==0 or i==M-1 or j==0 or j==N-1
        
    def is_in_angle(self) -> bool:
        i, j = self.position
        return ( i==0 or i==M-1 ) and ( j==0 or j==N-1)
    
    def is_active(self) -> bool:
        
        for link in self.links:
            if link.is_open:
                return True
        return False
        


class Link(Node):

    def __init__(self, first_node: Node, second_node: Node):

        self.nodes = (first_node, second_node)
        self.is_open = random() <= PROBABILITY
        first_node.links.append(self)
        second_node.links.append(self)
    
    def update(self) -> bool:
        
        self.is_open = random() <= PROBABILITY
        return self.is_open

class Grid(Node):
    

    def __init__(self):

        Size = namedtuple("Size", "M N")
        self.size = Size(M, N)

        nodes_matrix = []
        links_list = []
        
        self.nodes_matrix = nodes_matrix
        self.links_list = links_list
        
        for i in range(M):
            nodes_matrix.append([])
            for j in range(N):
                new_node = Node(i, j)
                nodes_matrix[i].append(new_node)
                
                
        for i in range(M):
            for j in range(N):
                #if nodes_matrix[i][j].is_in_angle():
                #    continue
                
                if i < M-1:
                    new_link = Link(nodes_matrix[i][j], nodes_matrix[i+1][j])
                    links_list.append(new_link)
                if j < N-1:
                    new_link = Link(nodes_matrix[i][j], nodes_matrix[i][j+1])
                    links_list.append(new_link)
    
    def print_grid(self):
        
        for i in range(M):
            for j in range(N):
                if self.nodes_matrix[i][j].is_active():
                    print("●", end="")
                else:
                    print("○", end="")
                
            print()
        print()
        
        for link in self.links_list:
            
            first_node, second_node = link.nodes
            print(first_node.position, end="")
            if link.is_open:
                print("==", end="")
            else:
                print("  ", end="")
            print(second_node.position)
                    
    
def main():
    
    new_grid = Grid()
    new_grid.print_grid()
    
    return 0

if __name__ == "__main__":
    main()
