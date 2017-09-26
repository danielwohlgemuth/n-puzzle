
import timeit

from collections import deque
from queue import PriorityQueue
import heapq
import tkinter
import time


N = 3
# 0 (cero) representa la pieza vacia
goal = [1,2,3,4,5,6,7,8,0]
#initial = [0,2,3,1,4,6,7,5,8]
initial = [1,3,8,4,2,0,7,6,5]
#initial = [0,8,7,6,5,4,3,2,1]
# Sin solucion
#initial = [5,2,7,8,4,0,1,3,6]

#goal = [0,1,2,3,4,5,6,7,8]
#initial = [2,4,0,1,8,5,3,6,7]
#initial = [7,2,4,5,0,6,8,3,1]

#N = 4
#goal = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
#initial = [1,2,3,4,5,6,7,8,9,10,11,12,13,0,14,15]
#initial = [15,8,9,14,5,10,1,0,12,4,3,13,11,2,7,6]
#initial = [1,2,3,4,5,6,7,8,9,12,11,14,0,15,13,10]
#initial = [1,2,3,4,6,7,0,11,5,12,14,8,9,15,13,10]
#initial = [0,6,1,10,11,4,5,13,2,8,7,15,3,14,12,9]
#initial = [2,3,0,13,1,15,10,4,8,9,7,6,11,5,14,12]
#initial = [15,0,8,10,2,1,7,14,13,4,5,3,9,6,12,11]
# Sin solucion
#initial = [13,9,7,15,3,6,8,4,11,10,2,12,5,1,14,0]
#initial = [15,2,1,12,8,5,6,11,4,9,10,7,3,14,13,0]


def swap(state, pos_1, pos_2):

    state[pos_1], state[pos_2] = state[pos_2], state[pos_1]
    return state


def misplaced(state, goal, N):
    '''
    Cuenta las piezas en posiciones incorrectas, excepto el vacio
    '''
    count = 0
    for i in range(N*N):
        if state.index(i) != goal.index(i) and state[state.index(i)] != 0:
            count += 1
    return count


def manhattan(state, goal, N):
    '''
    Calcula la distancia de Manhattan
    '''
    distance = 0
    for i in range(1, N*N):
        distance += abs(state.index(i)%N - goal.index(i)%N)
        distance += int(abs((state.index(i)-state.index(i)%N)/N - (goal.index(i)-goal.index(i)%N)/N))

    return distance


def is_solvable(initial, goal, N):
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


def print_puzzle(state, N):
    '''
    Imprime el arreglo en forma tabular
    '''
    for i in range(N):
        print(state[i*N:i*N+N])
    print()


def a_star_search_manhattan(initial, goal, N):
    counter = 1
    sequence = PriorityQueue()
    hashtable = {}

    if not is_solvable(initial, goal, N):
        print('No tiene solucion')
        exit()

    sequence.put((manhattan(initial, goal, N), counter))
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
            if pos != last_change or True:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)
                    counter += 1
                    sequence.put((steps + manhattan(new_state, goal, N), counter))
                    hashtable[counter] = [current, new_state, empty_pos, steps+1]


    # solution = deque()

    # Recorre el arbol desde la solucion hasta el inicio
    # while current != 0:
    #     solution.appendleft(hashtable[current][1])
    #     current = hashtable[current][0]

    # Imprime el resultado
    #for step in solution:
    #    print_puzzle(step, N)

    # print('Manhattan')
    # print('Cantidad de pasos:', len(solution))
    # print('Nodos explorados:', counter - sequence.qsize())
    # print('Nodos en cola:', sequence.qsize())
    # print('Total de nodos:', counter)
    # print()

    return counter - sequence.qsize()


def a_star_search_misplaced(initial, goal, N):
    # global counter
    counter = 1
    sequence = PriorityQueue()
    hashtable = {}

    if not is_solvable(initial, goal, N):
        print('No tiene solucion')
        exit()

    sequence.put((misplaced(initial, goal, N), counter))
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
            if pos != last_change or True:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)
                    counter += 1
                    sequence.put((steps + misplaced(new_state, goal, N), counter))
                    hashtable[counter] = [current, new_state, empty_pos, steps+1]


    # solution = deque()

    # Recorre el arbol desde la solucion hasta el inicio
    # while current != 0:
    #     solution.appendleft(hashtable[current][1])
    #     current = hashtable[current][0]

    # Imprime el resultado
    #for step in solution:
    #    print_puzzle(step, N)

    # print('Misplaced')
    # print('Cantidad de pasos:', len(solution))
    # print('Nodos explorados:', counter - sequence.qsize())
    # print('Nodos en cola:', sequence.qsize())
    # print('Total de nodos:', counter)
    # print()

    return counter - sequence.qsize()


def breath_search(initial, goal, N):
    # global counter
    counter = 1
    hashtable = {}

    if not is_solvable(initial, goal, N):
        print('No tiene solucion')
        exit()

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
            if pos != last_change or True:
                # Evita el desborde
                if pos >= 0 and pos < N*N:
                    new_state = swap(state.copy(), empty_pos, pos)

                    counter += 1
                    sequence.append(counter)
                    hashtable[counter] = [current, new_state, empty_pos]


    # solution = deque()

    # Recorre el arbol desde la solucion hasta el inicio
    # while current != 0:
    #     solution.appendleft(hashtable[current][1])
    #     current = hashtable[current][0]

    # Imprime el resultado
    # for step in solution:
    #    print_puzzle(step, N)

    # print('Anchura')
    # print('Cantidad de pasos:', len(solution))
    # print('Nodos explorados:', counter - len(sequence))
    # print('Nodos en cola:', len(sequence))
    # print('Total de nodos:', counter)
    # print()

    return counter - len(sequence)


class App:
    def __init__(self, master):

        tkinter.Label(master, text="N").grid(sticky="W", row=0)
        self.N = tkinter.IntVar()
        self.N.set(3)
        tkinter.Entry(master, text=self.N, width=3).grid(row=0, column=1)
        tkinter.Button(master, text="Actualizar", command=self.update).grid(row=0, column=2)

        self.method = tkinter.StringVar()
        self.method.set('A* Manhattan')
        tkinter.Label(master, text="Método").grid(sticky="W", row=1)
        tkinter.OptionMenu(master, self.method, 'A* Manhattan', 'A* Desubicados', 'Anchura').grid(row=1, column=1)

        tkinter.Button(master, text="Ejecutar", command=self.callback).grid(row=2, column=1)

        self.tiempo = tkinter.StringVar()
        self.tiempo.set('')
        tkinter.Label(master, text="Tiempo").grid(sticky="W", row=3)
        tkinter.Label(master, textvariable=self.tiempo).grid(row=3, column=1)

        self.expandidos = tkinter.StringVar()
        self.expandidos.set('')
        tkinter.Label(master, text="Expandidos").grid(sticky="W", row=4)
        tkinter.Label(master, textvariable=self.expandidos).grid(row=4, column=1)

        self.estado = tkinter.StringVar()
        self.estado.set('')
        tkinter.Label(master, text="Estado").grid(sticky="W", row=5)
        tkinter.Label(master, textvariable=self.estado).grid(row=5, column=1)

        self.f = None
        self.update()

    def callback(self):
        global initial
        initial = []
        for i in range(N*N):
            initial.append(int(self.grid[i].get()))

        if self.method.get() == 'A* Manhattan':
            method = a_star_search_manhattan
        elif self.method.get() == 'A* Desubicados':
            method = a_star_search_misplaced
        else:
            method = breath_search

        start_time = time.time()
        expanded = method(initial, goal, N)
        self.tiempo.set(time.time() - start_time)
        self.expandidos.set(expanded)


    def update(self):
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
        # print(goal)


def main():

    root = tkinter.Tk()
    app = App(root)
    root.mainloop()

    # Mide el tiempo de ejecucion
    # print(timeit.timeit('a_star_search_manhattan(initial, goal, N)', number=1))
    # print(timeit.timeit('a_star_search_misplaced(initial, goal, N)', number=1))
    # print(timeit.timeit('breath_search(initial, goal, N)', number=1))

main()
