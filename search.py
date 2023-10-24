"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem, TSP
from node import Node
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

    
        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

           
            # Retornar si estamos en un optimo local
            if diff[act] <= 0:
                self.tour = actual.state
                self.value = actual.value
                
                end = time()
                self.time = end-start
                return
            

            # Sino, moverse a un nodo con el estado sucesor
            else:

                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascenso de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con ascenso de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            Un problema de optimización
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        # Contador de veces que no encontramos solucion mejor
        count = 0

        # Guardamos el Minimo Local (Nodito) 
        estadoMin = actual
        
        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el mayor incremento de valor objetivo
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una acción aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un óptimo local
            
            if diff[act] <= 0:
                if estadoMin.value < actual.value:
                    count += 1
                    #print(count)
                    problem.random_reset()  # Reseteamos el problema aleatoriamente
                    actual = Node(problem.init, problem.obj_val(problem.init))

            # Sino, moverse a un nodo con el estado sucesor

            else:
                estadoMin = actual
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1

            if count == 10:
                self.tour = estadoMin.state
                self.value = estadoMin.value
                end = time()
                self.time = end - start
                return
            



class Tabu(LocalSearch):

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()
        
        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        mejor=actual
        print(mejor.value)
        tabu=[]


        while self.niters<500:
            
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)
            
            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)
            
            #si la lista tabu mide 10, se le saca la primer accion guardada
            if len(tabu)==10:
                tabu.pop()
            
           
            # Retornar si estamos en un optimo local
            if (actual.value > mejor.value) and actual.state not in tabu:
                mejor=actual

                self.tour = mejor.state
                self.value = mejor.value
                tabu.append(mejor.state)

                
            # Sino, moverse a un nodo con el estado sucesor
            else:
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                
                self.niters += 1

        end = time()
        self.time = end-start
        return
                

    
        

       
        
        
        
