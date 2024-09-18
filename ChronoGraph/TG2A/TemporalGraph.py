from TG2A.Automaton import Automaton
import string
from TG2A.Parser import Parser
import json

class TemporalGraph:

    def __init__(self, vertices, edges):
        """
        Initializes a dynamic graph.
        """
        self.vertices = vertices
        self.edges = edges

    # def add_vertex(self, vertex):
        """
        Adds a vertex to the graph.
        """
        pass

    # def remove_vertex(self, vertex):
        """
        Removes a vertex and its associated edges from the graph.
        """

    #def add_edge(self, source, target):
        """
        Adds an edge between two vertices in the graph.
        """
        pass

    #def remove_edge(self, source, target):
        """
        Removes an edge between two vertices in the graph.
        """
        pass

    def alphabet_combinations(self):
        # To create a set with all combinations of two letters taken from the alphabet.
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        double_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in alphabet)
        triple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in double_alphabet_set)
        # quadruple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in triple_alphabet_set)
        # cintuple_alphabet_set = set(letter1 + letter2 for letter1 in alphabet for letter2 in quadruple_alphabet_set)
        # Ajouter l'alphabet à la liste
        # sorted_quadruple_alphabet_list = alphabet + sorted(list(double_alphabet_set)) + sorted(list(triple_alphabet_set)) + sorted(list(quadruple_alphabet_set)) + sorted(list(cintuple_alphabet_set))
        sorted_triple_alphabet_list = alphabet + sorted(list(double_alphabet_set)) + sorted(list(triple_alphabet_set))
        return sorted_triple_alphabet_list

    def to_automata(self):
        """
        Converts the temporal graph into a automata.
        """
        # To create a set with all combinations of two letters taken from the alphabet.
        alphabet = self.alphabet_combinations()

        Q = self.vertices

        # Extraction of L : the largest time label
        time_labels = []
        for edge in self.edges:
            if isinstance(edge[1], int):
                time_labels.append(edge[1])
            elif isinstance(edge[1], tuple) or isinstance(edge[1], list):
                for element in edge[1]:
                    time_labels.append(element)
        L = max(time_labels)

        Sigma = []
        Delta = self.edges
        
        alphabet_to_int = dict()

        for i in range(len(Delta)):
            if isinstance(Delta[i][1], int):
                Delta[i][1] = [(alphabet[i], Delta[i][1])]
                Delta.append([ (Delta[i][0][1],Delta[i][0][0]), [(alphabet[i], Delta[i][1])] ])
                alphabet_to_int[alphabet[i]] = Delta[i][1]
            elif isinstance(Delta[i][1], tuple) or isinstance(Delta[i][1], list):
                # print("here")
                new_tuple = []
                for element in Delta[i][1]:
                    # print('element = ',element)
                    new_tuple.append( (alphabet[i], element) )
                    # if new_tuple[-1] not in Sigma:
                    #     Sigma.append(new_tuple[-1])
                Delta[i][1] = new_tuple
                Delta.append([ (Delta[i][0][1],Delta[i][0][0]), new_tuple ])
        q_0 = None
        F = []
        A_s_t = Automaton(Q, Sigma, Delta, q_0, F)

        return A_s_t

    def display(self):
        """
        Displays the components of the dynamic graph.
        """
        print("Vertices:", list(self.vertices))
        print("Edges:", list(self.edges))

    def save(self, filename):
        # Crée une structure de données représentant l'automate
        tg_data = {
        "type": "temporal-graph",
        "nodes": [],
        "edges": []
        }

        # Formatage des transitions pour les ajouter à la structure de données
        for node in self.vertices:
            tg_data["nodes"].append({
                "label": node
            })
        for edges in self.edges:
            tg_data["edges"].append({
                "from": edges[0][0],
                "to": edges[0][1],
                "label": edges[1]
            })
        # Écrit la structure de données dans un fichier JSON
        with open(filename, 'w') as json_file:
            json.dump(tg_data, json_file, indent=4)

if __name__ == "__main__":    
    TG = TemporalGraph(["S","A", "B", "C", "T"],[[("S", "A"), [1,3,5]], [("A", "T"), 2], [("S", "B"), 7], [("S", "C"), 5], [("A", "C"), 6] ])
    TG.save("tg.json")
    # TG_empty = TemporalGraph([], [])
    parser = Parser("tg.json")
    V,E = parser.parse()
    TG_parser = TemporalGraph(V,E)

    # print("\nRandom example : ")
    # TG.display()
    print("\nRandom example (parser) :")
    # TG_parser.display()
    # print("\nEmpty example : ")
    # TG_empty.display()