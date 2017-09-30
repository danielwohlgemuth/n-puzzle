
import random
import time
import timeit
import tkinter

from collections import deque
from queue import PriorityQueue


N = 3
# 0 (cero) representa la pieza vacia
goal = [1,2,3,4,5,6,7,8,0]
#initial = [0,2,3,1,4,6,7,5,8]
# initial = [1,3,8,4,2,0,7,6,5]

# Experimento
initial = [2,1,4,3,5,6,7,8,0]
#initial = [6,5,3,0,8,2,7,1,4]
#initial = [0,8,7,6,5,4,3,2,1]

class CONST(object):
    '''
    Guarda los nombres de los métodos para facilitar su modificación
    '''
    H2 = 'A* Manhattan'
    H1 = 'A* Incorrectas'
    BREATH = 'Anchura'

    def __setattr__(self, *_):
        pass

CONST = CONST()


def swap(state, pos_1, pos_2):

    state[pos_1], state[pos_2] = state[pos_2], state[pos_1]
    return state


def misplaced(state):
    '''
    Cuenta las piezas en posiciones incorrectas, excepto el vacio
    '''
    count = 0
    for i in range(N*N):
        if state.index(i) != goal.index(i) and state[state.index(i)] != 0:
            count += 1
    return count


def manhattan(state):
    '''
    Calcula la distancia de Manhattan
    '''
    distance = 0
    for i in range(1, N*N):
        distance += abs(state.index(i)%N - goal.index(i)%N)
        distance += int(abs((state.index(i)-state.index(i)%N)/N - (goal.index(i)-goal.index(i)%N)/N))

    return distance


def is_solvable():
    '''
    Verifica si el problema tiene solucion
    https://stackoverflow.com/a/34570524
    '''

    parity = 0
    grid_width = N
    row = 0
    blank_row = 0

    for i in range(N*N):

        # Cuenta cada columna
        if i % grid_width == 0:
            row += 1

        # Guarda en que fila esta la pieza vacia y continua con la siguiente iteracion
        if initial[i] == 0:
            blank_row = row
            continue

        for j in range(i+1, N*N):
            if initial[j] and initial[i] > initial[j]:
                parity += 1


    if grid_width % 2 == 0:
        if blank_row % 2 == 0:
            return parity % 2 == 0
        else:
            return parity % 2 != 0
    else:
        return parity % 2 == 0


def print_puzzle(state):
    '''
    Imprime el arreglo en forma tabular
    '''
    for i in range(N):
        print(state[i*N:i*N+N])
    print()


def create_puzzle():
    '''
    Genera un puzzle aleatorio válido
    '''
    global initial
    initial = list(goal)

    for _ in range(2):
        random_pos = random.randrange(1, N*N)
        swap(initial, random_pos-1, random_pos)

    while not is_solvable():
        random_pos = random.randrange(1, N*N)
        swap(initial, random_pos-1, random_pos)


def info(method_name, counter, sequence, hashtable, current):
    '''
    Imprime información útil para el debuging como los pasos de solución, 
    la profundidad, nodos explorados, en cola y el total
    '''
    solution = deque()

    # Recorre el arbol desde la solucion hasta el inicio
    while current != 0:
        solution.appendleft(hashtable[current][1])
        current = hashtable[current][0]

    # Imprime el resultado
    # for step in solution:
    #    print_puzzle(step, N)

    print(method_name)
    print('Profundidad:', len(solution)-1)
    unexplored = sequence.qsize() if hasattr(sequence, 'qsize') else len(sequence)
    print('Nodos explorados:', counter - unexplored)
    print('Nodos en cola:', unexplored)
    print('Total de nodos:', counter)
    print()


def a_star_search_manhattan():
    counter = 1
    sequence = PriorityQueue()
    hashtable = {}

    if not is_solvable():
        print('No tiene solucion')
        return()

    sequence.put((manhattan(initial), counter))
    # Cada entrada en hashtable contiene [padre, estado, cambio_anterior, pasos]
    hashtable[counter] = [0, initial, 0, 0]

    while True:

        # Obtiene el siguente estado minimo y extrae sus datos
        _, current = sequence.get()

        state = hashtable[current][1]
        last_change = hashtable[current][2]
        steps = hashtable[current][3]

        # Se encontro la solucion
        if state == goal:
            break

        # Obtiene la posicion del cero, que representa la pieza vacia
        empty_pos = state.index(0)

        # Repetir para cada posible intercambio
        for pos in [empty_pos-1, empty_pos+1, empty_pos-N, empty_pos+N]:
            # Evita revertir al estado anterior
            if pos != last_change:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)
                    counter += 1
                    sequence.put((steps+1 + manhattan(new_state), counter))
                    hashtable[counter] = [current, new_state, empty_pos, steps+1]

    # info(CONST.H2, counter, sequence, hashtable, current)

    return counter - sequence.qsize()


def a_star_search_misplaced():
    # global counter
    counter = 1
    sequence = PriorityQueue()
    hashtable = {}

    if not is_solvable():
        print('No tiene solucion')
        return()

    sequence.put((misplaced(initial), counter))
    # Cada entrada en hashtable contiene [padre, estado, cambio_anterior, pasos]
    hashtable[counter] = [0, initial, 0, 0]

    while True:

        # Obtiene el siguente estado minimo y extrae sus datos
        _, current = sequence.get()

        state = hashtable[current][1]
        last_change = hashtable[current][2]
        steps = hashtable[current][3]

        # Se encontro la solucion
        if state == goal:
            break

        # Obtiene la posicion del cero, que representa la pieza vacia
        empty_pos = state.index(0)

        # Repetir para cada posible intercambio
        for pos in [empty_pos-1, empty_pos+1, empty_pos-N, empty_pos+N]:
            # Evita revertir al estado anterior
            if pos != last_change:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)
                    counter += 1
                    sequence.put((steps+1 + misplaced(new_state), counter))
                    hashtable[counter] = [current, new_state, empty_pos, steps+1]

    # info(CONST.H1, counter, sequence, hashtable, current)

    return counter - sequence.qsize()


def breath_search():
    # global counter
    counter = 1
    hashtable = {}

    if not is_solvable():
        print('No tiene solucion')
        return()

    sequence = deque()
    sequence.append(counter)
    #sequence.put((manhattan(initial), counter))
    # Cada entrada en hashtable contiene [padre, estado, cambio_anterior]
    hashtable[counter] = [0, initial, 0]

    while True:

        # Obtiene el siguente estado minimo y extrae sus datos
        current = sequence.popleft()

        state = hashtable[current][1]
        last_change = hashtable[current][2]

        # Se encontro la solucion
        if state == goal:
            break

        # Obtiene la posicion del cero, que representa la pieza vacia
        empty_pos = state.index(0)

        # Repetir para cada posible intercambio
        for pos in [empty_pos-1, empty_pos+1, empty_pos-N, empty_pos+N]:
            # Evita revertir al estado anterior
            if pos != last_change:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)
                    counter += 1
                    sequence.append(counter)
                    hashtable[counter] = [current, new_state, empty_pos]

    # info(CONST.BREATH, counter, sequence, hashtable, current)

    return counter - len(sequence)


class App(object):
    '''
    Construcción de la interfaz gráfica con Tkinter
    '''

    def __init__(self, master):
        master.title("N-Puzzle")

        tkinter.Label(master, text="N").grid(sticky="W", row=0)
        self.N = tkinter.IntVar()
        self.N.set(3)
        tkinter.Entry(master, text=self.N, width=3).grid(row=0, column=1)
        tkinter.Button(master, text="Actualizar", command=self.update).grid(row=0, column=2)

        self.method = tkinter.StringVar()
        self.method.set(CONST.H2)
        tkinter.Label(master, text="Método").grid(sticky="W", row=1)
        tkinter.OptionMenu(master, self.method, CONST.H2, CONST.H1, CONST.BREATH).grid(row=1, column=1)

        tkinter.Button(master, text="Ejecutar", command=self.callback).grid(row=2, column=1)
        tkinter.Button(master, text="Generar", command=self.generate).grid(row=2, column=2)

        self.tiempo = tkinter.StringVar()
        self.tiempo.set('')
        tkinter.Label(master, text="Tiempo (s)").grid(sticky="W", row=3)
        tkinter.Label(master, textvariable=self.tiempo).grid(row=3, column=1)

        self.explorados = tkinter.StringVar()
        self.explorados.set('')
        tkinter.Label(master, text="Explorados").grid(sticky="W", row=4)
        tkinter.Label(master, textvariable=self.explorados).grid(row=4, column=1)

        self.estado = tkinter.StringVar()
        self.estado.set('')
        tkinter.Label(master, text="Estado").grid(sticky="W", row=5)
        tkinter.Label(master, textvariable=self.estado).grid(row=5, column=1)

        self.f = None
        self.update()

    def callback(self):
        '''
        Ejecuta uno de los métodos con los datos proveídos
        '''
        global initial
        initial = []
        for i in range(N*N):
            initial.append(int(self.grid[i].get()))

        if self.method.get() == CONST.H2:
            method = a_star_search_manhattan
        elif self.method.get() == CONST.H1:
            method = a_star_search_misplaced
        else:
            method = breath_search
        if is_solvable():
            self.tiempo.set('')
            self.explorados.set('')
            self.estado.set('')
            start_time = time.time()
            expanded = method()
            elapsed_time = time.time() - start_time
            self.tiempo.set('{:0.4f}'.format(elapsed_time))
            self.explorados.set(expanded)
        else:
            self.tiempo.set('')
            self.explorados.set('')
            self.estado.set('No tiene solución')

    def update(self):
        '''
        Ajusta el tamaño del puzzle
        '''
        global N, goal
        N = self.N.get()

        if self.f:
            self.f.destroy()

        self.f = tkinter.Frame(padx=1, pady=1)
        self.f.grid(row=6, rowspan=N, columnspan=N)

        self.grid = {}
        for i in range(N):
            for j in range(N):
                self.grid[i*N+j] = tkinter.Entry(self.f, width=3)
                self.grid[i*N+j].insert(0, i*N+j+1)
                self.grid[i*N+j].grid(row=i, column=j)

        goal = []
        for i in range(N*N):
            goal.append(i+1)
        # Asignar a la ultima ficha el espacio vacio
        goal[N*N-1] = 0
        self.grid[N*N-1].delete(0, tkinter.END)
        self.grid[N*N-1].insert(0, 0)

    def generate(self):
        '''
        Genera un puzzle válido aleatorio
        '''
        create_puzzle()
        self.grid = {}
        for i in range(N):
            for j in range(N):
                self.grid[i*N+j] = tkinter.Entry(self.f, width=3)
                self.grid[i*N+j].insert(0, initial[i*N+j])
                self.grid[i*N+j].grid(row=i, column=j)


def main():

    root = tkinter.Tk()
    app = App(root)
    root.mainloop()

    # create_puzzle()
    # print_puzzle(initial)
    # a_star_search_manhattan()

    # Mide el tiempo de ejecucion
    # print(timeit.timeit('a_star_search_manhattan()', number=1))
    # print(timeit.timeit('a_star_search_misplaced()', number=1))
    # print(timeit.timeit('breath_search()', number=1))


def experiment():
    '''
    Imprime el tiempo promedio de ejecución y la cantidad de nodos expandidos de cada método
    '''
    global N, goal, initial
    N = 3
    goal = [1,2,3,4,5,6,7,8,0]
    
    # Precalentamiento
    initial = [2,1,4,3,5,6,7,8,0]
    for _ in range(30):
        a_star_search_manhattan()

    COUNT = 10
    METHODS = [a_star_search_manhattan, a_star_search_misplaced, breath_search]

    for initial in [2,1,4,3,5,6,7,8,0], [6,5,3,0,8,2,7,1,4], [0,8,7,6,5,4,3,2,1]:
        # initial = x
        print(initial)
        for i, method in enumerate(METHODS):
            sum_time = [0, 0, 0]
            sum_expanded = [0, 0, 0]
            try:
                for _ in range(COUNT):
                    start_time = time.time()
                    sum_expanded[i] = method()
                    sum_time[i] += (time.time() - start_time)/COUNT
            except MemoryError:
                pass

            print(method.__name__)
            print('Time: ', sum_time[i])
            print('Expanded: ', sum_expanded[i])


main()
# experiment()
