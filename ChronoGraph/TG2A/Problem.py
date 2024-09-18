from abc import ABC, abstractmethod
from TG2A.TemporalGraph import TemporalGraph
from TG2A.Automaton import Automaton
import string
import copy
from random import *
import networkx as nx
from itertools import product
from iteration_utilities import unique_everseen, duplicates

class Problem(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def solve(self):
        pass

class BidirectionalPathProblem(Problem):

    def __init__(self, name, nodes, edges, start, target, key):
        super().__init__(name)
        self.graph = TemporalGraph(nodes, edges)
        self.start = start
        self.target = target
        self.key = key

        if self.key == False:
            self.key_impact = 0
        else:
            self.key_impact = 1

    def solve(self):

        def alphabet_combinations():
            # To create a set with all combinations of two letters taken from the alphabet.
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            double_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in alphabet)
            triple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in double_alphabet_set)
            quadruple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in triple_alphabet_set)
            # Ajouter l'alphabet à la liste
            sorted_quadruple_alphabet_list = alphabet + sorted(list(double_alphabet_set)) + sorted(list(triple_alphabet_set)) + sorted(list(quadruple_alphabet_set))
            return sorted_quadruple_alphabet_list

        def L_extraction(graph):
            # Extraction of L : the largest time label
            time_labels = []
            for edge in graph.edges:
                if isinstance(edge[1], int):
                    time_labels.append(edge[1])
                elif isinstance(edge[1], tuple):
                    for element in edge[1]:
                        time_labels.append(element)
                elif isinstance(edge[1], str):
                    time_labels.append(edge[1])
                elif isinstance(edge[1], list):
                    for element in edge[1]:
                        time_labels.append(element)
            L = max(time_labels)
            return L

        def create_A_time_incr(graph):
            L = L_extraction(graph)
            sorted_double_alphabet_list = alphabet_combinations()
            Q = [str(i) for i in range(L+1)]
            Sigma = []
            # delta
            transitions = []
            for i in range(len(Q)):
                # +0 key non strict
                for j in range(int(Q[i])+self.key_impact, len(Q)):
                    new_tuple = []
                    for element in sorted_double_alphabet_list[:len(graph.edges)]:
                        new_tuple.append( (element, int(Q[j])) )
                        # if new_tuple[-1] not in Sigma:
                        #     Sigma.append(new_tuple[-1])
                    transitions.append([(Q[i], Q[j]), new_tuple ])
            A_time_incr = Automaton(Q, Sigma, transitions, Q[0], Q)
            return A_time_incr

        def create_A_time_decr(graph):
            '''
            Create A_time_decr.
            '''
            L = L_extraction(graph)
            sorted_double_alphabet_list = alphabet_combinations()
            Q = [str(i) for i in range(L+2)[::-1]]
            Sigma = []
            # delta
            transitions_r = []
            for i in range(len(Q)+ 1)[::-1]:
                # + 1 non strict
                for j in range(i+1-self.key_impact)[::-1]:
                    new_tuple_r = []
                    for element in sorted_double_alphabet_list[:len(graph.edges)]:
                        new_tuple_r.append( (element, j ))
                        # if new_tuple_r[-1] not in Sigma:
                        #     Sigma.append(new_tuple_r[-1])
                    transitions_r.append([(str(i), str(j)), new_tuple_r ])

            A_time_decr = Automaton(Q, Sigma, transitions_r, Q[0], Q)
            return A_time_decr

        def intersection_opti(A1,A2):
            '''
            Intersection beetween 2 automatas with optimisations.
            '''
            # self.states = Q
            # self.alphabet = Sigma
            # self.transitions = delta
            # self.initial_state = q_0
            # self.finals_states = F

            new_states = []
            new_sigma = []

            ## delta
            delta = []
            for transition in A1.transitions:
                state_from = transition[0][0]
                state_to = transition[0][1]
                caracts = transition[1]
                for one_caract in caracts:
                    for transitions_A2 in A2.transitions:
                        
                        ## Opti
                        if isinstance(one_caract,tuple) and one_caract[1] != int(transitions_A2[0][1]):
                            # Imposible path
                            continue

                        state_from_A2 = transitions_A2[0][0]
                        state_to_A2 = transitions_A2[0][1]

                        delta.append( [ ( (state_from, state_from_A2), (state_to, state_to_A2)), [ one_caract ] ] )

                        if (state_from, state_from_A2) not in new_states:
                            new_states.append((state_from, state_from_A2))
                        if (state_to, state_to_A2) not in new_states:
                            new_states.append((state_to, state_to_A2))
                        if one_caract not in new_sigma:
                            new_sigma.append(one_caract)

            ## q_0
            new_initial = (A1.initial_state, A2.initial_state)

            ## F

            new_final = []

            for final in A1.finals_states:
                for final_A2 in A2.finals_states:
                    new_final.append((final, final_A2))
            
            cleared_new_final = [item for item in new_final if item in new_states]
            
            return Automaton(new_states, new_sigma, delta, new_initial, cleared_new_final)

        def apply_h_on_automata(automata):
            Q = automata.states
            # for symbol in automata.alphabet:
                # print("symbol = ", symbol)
            # print("automata.alphabet = ", automata.alphabet)
            Sigma = set([symbol[0] for symbol in automata.alphabet])
            q_0 = automata.initial_state
            F = automata.finals_states
            delta = []
            for transition in automata.transitions:
                from_to = transition[0]
                new_symbols = []
                for tuple in transition[1]:
                    new_symbols.append(tuple[0])
                delta.append([from_to, new_symbols])
            return Automaton(Q, Sigma, delta, q_0, F)

        def find_paths(automata, current_state, visited, path, solution):
            # Marquer l'état actuel comme visité
            visited.append(current_state[0][0])

            # Ajouter l'état actuel au chemin
            path.append(current_state)

            # Vérifier si nous avons atteint l'état cible
            if current_state in automata.finals_states:
                solution.append(path)
            else:
                # Parcourir les transitions partant de l'état actuel
                for transition in automata.transitions:
                    from_state = transition[0][0]
                    to_state = transition[0][1]

                    # Si l'état de départ de la transition correspond à l'état actuel
                    if from_state == current_state:
                        # Vérifier si l'état suivant n'a pas été visité
                        # print("to_state = ", to_state)
                        if to_state[0][0] not in path and to_state[0][0] not in visited:
                            # Récursion pour explorer le chemin suivant
                            find_paths(automata, to_state, visited[:], path[:], solution)  # Passer des copies de visited et path

        # print("Copy...")
        TG = copy.deepcopy(self.graph)
        # print("Copied !")

        print(f"Solving {self.name} using automata's représentation : \n")
        # print("A_s_t...\n")
        A_s_t = self.graph.to_automata()
        print("A_s_t...\n")
        # A_s_t.display()
        A_s_t.set_initial_state(self.start)
        A_s_t.set_final_state(self.target)

        # print("A_s_t :\n")
        # A_s_t.display()
        A_s_t.clear()
        # print("A_s_t.clear :\n")
        # A_s_t.display()

        A_time_incr = create_A_time_incr(TG)
        # A_time_incr = create_A_time_incr(self.graph)
        print("A_time_incr...\n")
        A_time_incr.display()
        # A_time_incr.clear()
        # print("A_time_incr.clear :\n")
        # A_time_incr.display()


        A_time_decr = create_A_time_decr(TG)
        print("A_time_decr...\n")
        # A_time_decr.display()

        A_time_decr.clear()
        # print("A_time_decr.clear :\n")
        # A_time_decr.display()

        A_s_t_time = intersection_opti(A_s_t, A_time_incr)
        print("A_s_t_time...\n")
        # A_s_t_time.display()
        A_s_t_time.clear()
        # print("A_s_t_time.clear :\n")
        # A_s_t_time.display()

        A_t_s_time = intersection_opti(A_s_t, A_time_decr)
        print("A_t_s_time...\n")
        # A_t_s_time.display()    
        A_t_s_time.clear()
        # print("A_t_s_time.clear :\n")
        # A_t_s_time.display()  

        # ## Homomorphism

        h_A_s_t_time = apply_h_on_automata(A_s_t_time)
        print("h_A_s_t_time...\n")
        # h_A_s_t_time.display()

        h_A_t_s_time = apply_h_on_automata(A_t_s_time)
        print("h_A_t_s_time...\n")
        # h_A_t_s_time.display()

        # ### A_s_t_bi
        A_s_t_bi = h_A_s_t_time.intersection(h_A_t_s_time)
        # A_s_t_bi = intersection_opti(h_A_s_t_time, h_A_t_s_time)
        print("A_s_t_bi...\n")
        # A_s_t_bi.display()
        A_s_t_bi.clear()
        # print("A_s_t_bi.clear :\n")
        # A_s_t_bi.display()

        return A_s_t_bi

def create_temporal_graph(n, nb_labels, max_label, prob):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    double_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in alphabet)
    triple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in double_alphabet_set)
    quadruple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in triple_alphabet_set)
    # Ajouter l'alphabet à la liste
    sorted_quadruple_alphabet_list = alphabet + sorted(list(double_alphabet_set)) + sorted(list(triple_alphabet_set)) + sorted(list(quadruple_alphabet_set))
    # print("size = ", len(sorted_quadruple_alphabet_list))

    if n > 475250:
        print("Please choose a numbef of nodes lower than 475520.")
        return -1
    
    nodes = []
    edges = []

    for i in range(n):
        nodes.append(sorted_quadruple_alphabet_list[i])

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if random() < prob:
                continue
            liste = []
            for _ in range(nb_labels):
                liste.append(randint(1, max_label))
            edges.append( [(nodes[i], nodes[j]), (liste)] )
    
    return nodes, edges

if __name__ == "__main__":   
    print("Creation...")
    nodes, edges = create_temporal_graph(50, 1, 4, 0.5)
    print('Created !')
    TG = TemporalGraph(nodes, edges)
    print("TG Created !")
    # TG = TemporalGraph(["S","A", "B", "C", "T"],[[("S", "A"), (1,3)], [("A", "T"), (2)], [("S", "B"), 7], [("S", "C"), 5], [("A", "C"), 6] ])
    # TG = TemporalGraph(["S", "B", "C", "D", "E", "T"],[ [("S", "B"), (1,3)], [("B", "T"), (2,5,6)], [("S", "D"), (1,10)], [("D", "E"), (2,9)], [("E", "F"), (3,8)], [("F", "B"), (4,7)]  ])
    # TG = TemporalGraph(["S","A", "T"],[[("S", "A"), (1,10)], [("A", "T"), (10,1)]])
    # TG = TemporalGraph(["S", "B", "C", "D", "T", "F", "G"],[ [("S", "B"), (4,1)], [("B", "C"), (2,3)], [("C", "D"), (2,3)], [("D", "T"), (4,1) ], [("S", "F"), (4,1)], [("F", "G"), (2,3)], [("G", "D"), (3,2)] ])

    # TG.display()
    bpp = BidirectionalPathProblem("Bidirectional Path Problem",TG, start="a", target=["b"] )
    print("bpp created !")
    bpp.solve()

    # problems = [graph_coloring_problem, traveling_salesman_problem]
    # for problem in problems:
    #     problem.solve()
