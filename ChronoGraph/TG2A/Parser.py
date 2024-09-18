import json

class Parser:

    def __init__(self, json_path_file):
        """
        Initializes a Parser.
        """
        self.json_path_file = json_path_file

    def parse(self):

        def read(chemin_fichier):
            with open(chemin_fichier, 'r') as fichier:
                donnees_json = json.load(fichier)
            return donnees_json

        json_data = read(self.json_path_file)

        if json_data["type"] in ["automa", "automatas", "Automata", "Automatas", "automaton", "automatons", "Automaton", "Automatons"]:
            automaton_parser = AutomataParser(json_data)
            return automaton_parser.parse()
        elif json_data["type"] in ["temporal-graph"]:
            temporal_graph_parser = TemporalGraphParser(json_data)
            return temporal_graph_parser.parse()
        else:
            print("Error : type")

class TemporalGraphParser(Parser):

    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def parse(self):
        V = []
        E = []

        for vertice in self.data["nodes"]:
            V.append(vertice["label"])
        
        for edge in self.data["edges"]:
            
            from_to = (edge["from"], edge["to"])
            if isinstance(edge["label"], str) or isinstance(edge["label"], int):
                symbols = edge["label"]
            if isinstance(edge["label"], list):
                symbols = []
                for element in edge["label"]:
                    symbols.append(element)
            E.append([from_to, symbols])
        
        return V, E

class AutomataParser(Parser):

    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def parse(self):
        
        Q = []
        Sigma = []
        delta = []
        q_0 = ""
        F = []


        # states 
        for state in self.data["states"]:
            Q.append(state["name"])
            if state["initial"] == True and q_0 == "":
                q_0 = state["name"]
            # if state["initial"] == True and q_0 != "":
            #     print("Error : multiples initial states.")
            #     return -1
            if state["accepting"] == True:
                F.append(state["name"])
        
        # transitions
        for transition in self.data["transitions"]:
            from_to = (transition["from"], transition["to"])
            # == str
            if isinstance(transition["symbol"], str):
                symbols = [transition["symbol"]]
                if transition["symbol"] not in Sigma:
                    Sigma.append(transition["symbol"])
            if isinstance(transition["symbol"], list):
                symbols = []
                for element in transition["symbol"]:
                    symbols.append(element)
                    if element not in Sigma:
                        Sigma.append(element)
            delta.append([from_to, symbols])
        
        return Q, Sigma, delta, q_0, F


if __name__ == "__main__": 
    pass
