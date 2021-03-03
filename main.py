import numpy
import pygame
import threading


class Cell:
    def __init__(self, x, y, visitable):
        self.visitable = visitable  # boolean
        self.x = x  # integer
        self.y = y  # integer
        self.g = -1  # integer
        self.h = -1  # integer

    def set_g(self, g):
        self.g = g

    def set_h(self, h):
        self.h = h

    def get_f(self):
        return self.h + self.g



class Map:
    # se le pasa como parametro una matriz de binarios que indica que celdas son "visitables"
    def __init__(self, matrix):

        cell_matrix = []  # Cell[][]
        # crea una matriz compleja de Objetos Cell
        for y, row in enumerate(matrix):
            cell_row = []  # Cell[]
            for x, cell in enumerate(row):
                cell = Cell(x, y, cell)
                cell_row.append(cell)
            cell_matrix.append(cell_row)

        self.matrix = numpy.array(cell_matrix)
        # establece limites de la matriz
        self.y_limit = len(cell_matrix) - 1
        self.x_limit = len(cell_matrix[0]) - 1

    def get_cell_neighbors(self, cell):
        # cell : Cell
        cell_x = cell.x
        cell_y = cell.y

        neighbors = list()

        # top cell
        if cell_y > 0:
            top_cell = self.matrix[cell_y - 1][cell_x]
            if top_cell.visitable == 1:
                neighbors.append(top_cell)

        # right cell
        if cell_y < self.x_limit:
            right_cell = self.matrix[cell_y][cell_x + 1]
            if right_cell.visitable == 1:
                neighbors.append(right_cell)

        # bottom cell
        if cell_y < self.y_limit:
            bottom_cell = self.matrix[cell_y + 1][cell_x]
            if bottom_cell.visitable == 1:
                neighbors.append(bottom_cell)

        # left cell
        if cell_x > 0:
            left_cell = self.matrix[cell_y][cell_x - 1]
            if left_cell.visitable == 1:
                neighbors.append(left_cell)

        return neighbors

    def get_cell(self, x, y):
        return self.matrix[y][x]

    def search(self, origin_coords, target_coords):

        origin_x, origin_y = origin_coords
        target_x, target_y = target_coords
        # obtiene las celdas
        origin_cell = self.get_cell(origin_x, origin_y)
        target_cell = self.get_cell(target_x, target_y)

        # pasos globales
        global_g = 0

        # estructuras set para procesamiento de busqueda
        open_set = list()
        closed_set = list()

        # se agrega la celda de origen al open_set
        open_set.append(origin_cell)

        road = list()

        # renderiza la celda de destino en verde

        # mientras el open_set no esté vacio...
        while len(open_set) != 0:
            # calula costos
            for cell_3 in open_set:
                cell_3.set_g(global_g + 1)
                # calculo de h (heurista)
                x = cell_3.x - target_cell.x
                y = cell_3.y - target_cell.y
                # calcula f
                f = abs(x) + abs(y)
                cell_3.set_h(f)
            # obtiene la celda con menor costo del open set
            winner_cell = min(open_set, key=lambda e: e.get_f())

            # retira las celdas open_set y se pasan a closed_set
            while len(open_set) != 0:
                cell_2 = open_set.pop()
                closed_set.append(cell_2)
            # se obtienen los vecinos de la celda
            neighbors = self.get_cell_neighbors(winner_cell)

            # mientras el vecino no esté en closed_set, se agrega a open_set
            for cell_1 in neighbors:
                if not (cell_1 in closed_set):
                    open_set.append(cell_1)
            # convierte la celda ganadara a la actual
            # suma la cantidad de pasos
            global_g = global_g + 1
            # renderiza la celda actua
            # si la celda ganadora es la que se está buscando la regresa
            road.append(winner_cell)
            if winner_cell == target_cell:
                return road, closed_set, target_cell

        return None


class GameEngine:

    def __init__(self, size, shape_x, shape_y):
        self.size = size
        pygame.init()
        screen = pygame.display.set_mode((shape_x * size, shape_y * size))
        screen.fill((255, 255, 255))
        self.screen = screen
        self.running = False

    def update(self):
        pygame.display.update()

    def loop(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(30)
            self.update()

    def start(self):
        self.running = True
        threading.Thread(target=self.loop).start()

    def quit(self):
        self.running = False
        pygame.quit()

    def wait(self):
        while True:
            events = pygame.event.get()
            step = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        step = True
                        break
            if step:
                break


    def render_map(self, map):
        matrix = map.matrix
        for row in matrix:
            for cell_x in row:
                if cell_x.visitable != 1:
                    self.render_cell(cell_x, (0, 0, 0))
                else:
                    self.render_cell(cell_x, (255, 255, 255))

    def render_road(self, road, color, time):
        for cell in road:
            self.render_cell(cell, color)
            pygame.time.wait(time)

    def render_cell(self, cell_y, color):
        pygame.draw.rect(self.screen, color, (cell_y.x * self.size, cell_y.y * self.size, self.size, self.size), 0)


if __name__ == '__main__':
    # matriz de binarios que representa un mapa
    map_matrix = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Mapa inteligente, recibe como parametro una matriz de binarios
    map = Map(map_matrix)

    # obtiene la ruta hasta el punto deseado
    road, close_set, target_cell = map.search((1, 1), (14, 1))

    # motor de renderizado propio, recibe como parametro el ancho de celda, y el tamaño del mapa
    gameEngine = GameEngine(45, len(map_matrix[0]), len(map_matrix))
    # arranca el motor de renderizado
    gameEngine.start()

    # renderiza el mapa
    gameEngine.render_map(map)
    # renderiza la celda de destino
    gameEngine.render_cell(target_cell, (0, 0, 255))
    gameEngine.wait()

    # renderiza la propagación del algoritmo
    gameEngine.render_road(close_set, (0, 255, 0), 100)
    gameEngine.wait()

    # renderiza la ruta optima a la solución
    gameEngine.render_road(road, (0, 0, 255), 75)

    gameEngine.wait()
    gameEngine.render_map(map)

    road, close_set, target_cell = map.search((14, 1), (1, 1))

    gameEngine.render_cell(target_cell, (0, 0, 255))
    gameEngine.wait()

    gameEngine.render_road(close_set, (0, 255, 0), 75)
    gameEngine.wait()

    gameEngine.render_road(road, (0, 0, 255), 75)
    gameEngine.wait()

    gameEngine.quit()
