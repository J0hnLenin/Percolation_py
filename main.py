from collections import namedtuple
from random import random
import pygame
from queue import Queue

#Если у Вас не установлена библиотека pygame откройте cmd и введите pip install pygame

PROBABILITY = 0.1 # Вероятность того, что связь будет открытая
M = 5000 # Число строк i
N = 5000 # Число колонок j

DRAW_MODE = False

DISTANSE = 2 # Расстояние между узлами
INDENT = 10 # Отступ от края окна
LINK_SCALE = 1 # Размер связи
NODE_SCALE = 0 # Размер узла

WINDOW_WIDTH = 2*INDENT + (N-1) * DISTANSE # Ширина окна 
WINDOW_HEIGHT = 2*INDENT + (M-1) * DISTANSE # Высота окна

ACTIVE_COLOR = (255, 91, 71) # Цвет активного узла и активной связи RGB
PASSIVE_COLOR = (65, 105, 255) # Цвет пассивного узла и пассивной связи в RGB
BACKGROUND_COLOR = (200, 200, 200) # Цвет фона в RGB


class Grid:
    """Класс Сетка"""

    def __init__(self):
        """Инициализация"""

        adjacency_list = [] # Список смежности
        for i in range(N*M):
            adjacency_list.append([])

        for i in range(N*M):
            if((i%N != N-1) and (random() <= PROBABILITY)):
                adjacency_list[i].append(i+1)
                adjacency_list[i+1].append(i)
            if((i//N != M-1) and (random() <= PROBABILITY)):
                adjacency_list[i].append(i+N)
                adjacency_list[i+N].append(i)  

        self.adjacency_list = adjacency_list   

    def cluster_search(self):  
        for j in range(M):
            if bfs(self, N*j):
                return True  
        return False

            
        

def position(i: int) -> tuple:
    return (INDENT + DISTANSE*(i%N), INDENT + DISTANSE*(i//N))

def bfs(grid: Grid, i: int) -> bool:

    left_infinity, right_infinity = False, False

    is_visited = set()
    queue = Queue()
    queue.put(i)

    while not queue.empty():
        i = queue.get()
        is_visited.add(i)

        if i%N == 0:
            left_infinity = True
        
        if i%N == N-1:
            right_infinity == True

        if right_infinity and left_infinity:
            return True

        for j in grid.adjacency_list[i]:
            if not j in is_visited:
                queue.put(j)
        
     
            
def main():
    
    new_grid = Grid()
    print(new_grid.cluster_search())

    if DRAW_MODE:

        # Инициализация окна
        pygame.init()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Percolation")
        window.fill(BACKGROUND_COLOR)

        running = True
        while running:
            # Цикл обновления экрана

            for event in pygame.event.get():
                # Проверка: закрыто ли окно
                if event.type == pygame.QUIT:
                    running = False
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     new_grid.update()

            for i in range(N*M):

                if new_grid.adjacency_list[i]:
                    pygame.draw.circle(window, ACTIVE_COLOR, position(i), NODE_SCALE)

                    for j in new_grid.adjacency_list[i]:
                        pygame.draw.line(window, ACTIVE_COLOR, position(i), position(j), LINK_SCALE)
                
                else:
                    pygame.draw.circle(window, PASSIVE_COLOR, position(i), NODE_SCALE)            
            
            # Обновление экрана
            pygame.display.flip()

        # Закрытие окна
        pygame.quit()
    

if __name__ == "__main__":
    main()
