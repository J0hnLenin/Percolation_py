from collections import namedtuple
from random import random
import pygame
from queue import Queue

#Если у Вас не установлена библиотека pygame откройте cmd и введите pip install pygame

PROBABILITY = 0.5 # Вероятность того, что связь будет открытая
M = 100 # Число строк i
N = 100 # Число колонок j


DISTANSE = 2 # Расстояние между узлами
INDENT = 50 # Отступ от края окна
LINK_SCALE = 1 # Размер связи
NODE_SCALE = 0 # Размер узла

WINDOW_WIDTH = 2*INDENT + (N-1) * DISTANSE # Ширина окна 
WINDOW_HEIGHT = 2*INDENT + (M-1) * DISTANSE # Высота окна

ACTIVE_COLOR = (255, 91, 71) # Цвет активного узла и активной связи RGB
PASSIVE_COLOR = (65, 105, 255) # Цвет пассивного узла и пассивной связи в RGB
BACKGROUND_COLOR = (200, 200, 200) # Цвет фона в RGB

class Node:
    """Класс Узел"""

    def __init__(self, i: int, j: int):
        """Инициализация"""

        Index = namedtuple("Index", "i j")
        self.index = Index(i, j) # Индекс узла в матрице
        self.links = [] # Список связей узла
        self.position = (INDENT + DISTANSE*j, INDENT + DISTANSE*i) # Положение узла на экране
        self.cluster = None # Кластер, к которому принадлежит узел
        
    def is_on_border(self) -> bool:
        """Проверка: является ли узел крайним (он на границе)"""

        i, j = self.index
        return i==0 or i==M-1 or j==0 or j==N-1
        
    def is_in_angle(self) -> bool:
        """Проверка: является ли узел угловым"""

        i, j = self.index
        return ( i==0 or i==M-1 ) and ( j==0 or j==N-1)
    
    def is_active(self) -> bool:
        """Проверка: является ли узел активным"""
        # Узел активный, если у него есть хотя бы одна активная связь

        for link in self.links:
            if link.is_active:
                return True
        return False

    def get_color(self):
        """Функция возвращает цвет узла"""
        if self.is_active():
            return ACTIVE_COLOR
        else:
            return PASSIVE_COLOR
        


class Link:
    """Класс Связь"""

    def __init__(self, first_node: Node, second_node: Node):
        """Инициализация"""

        self.nodes = (first_node, second_node) # Кортеж из двух вершин, которые соединяет связь
        self.is_active = random() <= PROBABILITY # Определение открытости связи

        # Добавление связи в список связей
        first_node.links.append(self) 
        second_node.links.append(self) 

        self.position = (first_node.position, second_node.position) # Расположение связи на экране
    
    def update(self) -> bool:
        """Обновляет значение активности связи, присваивая новое значение"""
        self.is_active = random() <= PROBABILITY
        return self.is_active
        
    def get_color(self):
        """Функция возвращает цвет связи"""
        if self.is_active:
            return ACTIVE_COLOR
        else:
            return PASSIVE_COLOR

    def get_other_node(self, node: Node) -> Node:
        """Функция возвращает вершину связи, отличную от введённой или None, если исходная вершина не найдена"""
        if node == self.nodes[0]:
            return self.nodes[1]
        if node == self.nodes[1]:
            return self.nodes[0]
        
        return None

class Cluster:
    """Класс Кластер"""

    def __init__(self):
        """Инициализация"""

        self.nodes_list = [] # Список узлов кластера
        self.links_list = [] # Список связей кластера
        self.is_left_infinity = False # Имеет ли кластер узлы на левой границе
        self.is_right_infinity = False # Имеет ли кластер узлы на правой границе
        self.is_infinity = False # Является ли кластер бесконечным

class Grid:
    """Класс Сетка"""

    def __init__(self):
        """Инициализация"""

        Size = namedtuple("Size", "M N")
        self.size = Size(M, N) # Размер сетки

        nodes_matrix = [] # Матрица узлов
        links_list = [] # Список связей 
        
        self.nodes_matrix = nodes_matrix
        self.links_list = links_list
        
        # Создание узлов 
        for i in range(M):
            nodes_matrix.append([])
            for j in range(N):
                new_node = Node(i, j)
                nodes_matrix[i].append(new_node)

        # Создание связей
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

        # Поиск кластеров
        self.clusters_list = []
        self.find_clusters()
            
    
    def print_grid(self):
        """Процедура вывода сетки в консоль"""
        
        # # Вывод узлов
        # for i in range(M):
        #     for j in range(N):
        #         if self.nodes_matrix[i][j].is_active():
        #             print("●", end="")
        #         else:
        #             print("○", end="")
                
        #     print()
        # print()
        
        # # Вывод связей
        # for link in self.links_list:
        #     first_node, second_node = link.nodes
        #     print(first_node.index, end="")
        #     if link.is_active:
        #         print("==", end="")
        #     else:
        #         print("--", end="")
        #     print(second_node.index)
        # print()

        # Вывод кластеров
        counter = 0
        for cluster in self.clusters_list:
            
            if cluster.is_infinity:
                counter += 1
            
            
        print(f"Число бесконечных кластеров в сетке: {counter}")
            

    def find_clusters(self):
        """Процедура поиска кластеров в сетке"""
        
        j = 0
        for i in range(M):
            
            node = self.nodes_matrix[i][j]
            if node.is_active() and node.cluster is None:
                new_cluster = Cluster()
                bfs(node, new_cluster)

                new_cluster.is_infinity = new_cluster.is_left_infinity and new_cluster.is_right_infinity
                    
                self.clusters_list.append(new_cluster)
        
        

    def update(self):
        """Процедура обновления сетки"""
        for link in self.links_list:
            link.update()
        self.clusters_list = []
        self.find_clusters()


def dfs(node: Node, cluster: Cluster) -> None:
    """Рекурсивный поиск в глубину по активным узлам"""
    cluster.nodes_list.append(node)
    node.cluster = cluster 
    
    if node.index.j == 0:
        cluster.is_left_infinity = True
    if node.index.j == N - 1:
        cluster.is_right_infinity = True

    for link in node.links:
        other_node = link.get_other_node(node)
        if (other_node is not None) and (link.is_active):
            if other_node.cluster is None:
                cluster.links_list.append(link)
                dfs(other_node, cluster)


def bfs(node: Node, cluster: Cluster) -> None:
    """Циклический поиск в ширину по активным узлам"""
    
    queue = []
    queue.append(node)

    while(len(queue) != 0):
        
        node = queue.pop(0)

        cluster.nodes_list.append(node)
        node.cluster = cluster 
        
        if node.index.j == 0:
            cluster.is_left_infinity = True
        if node.index.j == N - 1:
            cluster.is_right_infinity = True
        if  cluster.is_left_infinity and cluster.is_right_infinity:
            break

        for link in node.links:
            other_node = link.get_other_node(node)
            if (other_node.cluster is None) and (link.is_active):
                
                cluster.links_list.append(link)
                queue.append(other_node)
            
            
def main():
    
    new_grid = Grid()
    new_grid.print_grid()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                new_grid.update()

        for link in new_grid.links_list:
            # Отрисовка связей    
            pygame.draw.line(window, link.get_color(), link.position[0], link.position[1], LINK_SCALE)

        for i in range(M):
            # Отрисовка узлов
            for j in range(N):
                if new_grid.nodes_matrix[i][j].is_in_angle():
                    # Угловые узлы не рисуем для удобства
                    continue

                pygame.draw.circle(window, new_grid.nodes_matrix[i][j].get_color(), new_grid.nodes_matrix[i][j].position, NODE_SCALE)
        
        
        # Обновление экрана
        pygame.display.flip()

    # Закрытие окна
    pygame.quit()
    

if __name__ == "__main__":
    main()
