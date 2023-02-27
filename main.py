from collections import namedtuple
from random import random
import pygame

PROBABILITY = 0.2 # Must be from 0 to 1
M = 6 # Strings i
N = 8 # Сolumns j


DISTANSE = 100
INDENT = 50
WINDOW_WIDTH = 2*INDENT + (N-1) * DISTANSE  
WINDOW_HEIGHT = 2*INDENT + (M-1) * DISTANSE

ACTIVE_COLOR = (255, 91, 71)
PASSIVE_COLOR = (65, 105, 255)
BACKGROUND_COLOR = (220, 220, 220)

class Node(object):
    

    def __init__(self, i: int, j: int):

        Index = namedtuple("Index", "i j")
        self.index = Index(i, j)
        self.links = []
        self.position = (INDENT + DISTANSE*j, INDENT + DISTANSE*i)
        
    def is_on_border(self) -> bool:
        i, j = self.index
        return i==0 or i==M-1 or j==0 or j==N-1
        
    def is_in_angle(self) -> bool:
        i, j = self.index
        return ( i==0 or i==M-1 ) and ( j==0 or j==N-1)
    
    def is_active(self) -> bool:
        
        for link in self.links:
            if link.is_open:
                return True
        return False

    def get_color(self):
        if self.is_active():
            return ACTIVE_COLOR
        else:
            return PASSIVE_COLOR
        


class Link(Node):

    def __init__(self, first_node: Node, second_node: Node):

        self.nodes = (first_node, second_node)
        self.is_open = random() <= PROBABILITY
        first_node.links.append(self)
        second_node.links.append(self)
        self.position = (first_node.position, second_node.position)
    
    def update(self) -> bool:
        
        self.is_open = random() <= PROBABILITY
        return self.is_open
        
    def get_color(self):
        if self.is_open:
            return ACTIVE_COLOR
        else:
            return PASSIVE_COLOR

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
                if nodes_matrix[i][j].is_on_border():
                    continue
                if i == 1:
                    new_link = Link(nodes_matrix[i][j], nodes_matrix[i-1][j])
                    links_list.append(new_link)
                if j == 1:
                    new_link = Link(nodes_matrix[i][j], nodes_matrix[i][j-1])
                    links_list.append(new_link)
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
            print(first_node.index, end="")
            if link.is_open:
                print("==", end="")
            else:
                print("  ", end="")
            print(second_node.index)
                    
    
def main():
    
    new_grid = Grid()
    new_grid.print_grid()

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Percolation")
    window.fill(BACKGROUND_COLOR)

    running = True
    while running:

        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
 
        for link in new_grid.links_list:
                
            pygame.draw.line(window, link.get_color(), link.position[0], link.position[1], 5)

        for i in range(M):
            for j in range(N):
                if new_grid.nodes_matrix[i][j].is_in_angle():
                    continue

                pygame.draw.circle(window, new_grid.nodes_matrix[i][j].get_color(), new_grid.nodes_matrix[i][j].position, 5)
        
        pygame.display.flip()
    
    pygame.quit()
    

if __name__ == "__main__":
    main()
