from TG2A.Parser import Parser
import json
import networkx as nx

class Automaton:    

    def __init__(self, Q, Sigma, delta, q_0, F):
        """
        Initializes the automate with an 5-tuple :
            - Q : finite set of states.
            - Sigma : a finite alphabet.
            - delta : a transition funcion.
            - q_0 : the initial state.
            - F : a set of finals state.
        """
        self.states = Q
        self.alphabet = Sigma
        self.transitions = delta
        self.initial_state = q_0
        self.finals_states = F
    
    def to_graph(self):
        graph = nx.Graph()
        edges_labels_multiples = dict()
        edges_labels = dict()
        for state in self.states:
            graph.add_node(state[0][0])
        if len(self.transitions) > 0:
            for i in range(len(self.transitions)):
                node_from = self.transitions[i][0][0][0][0]
                node_to = self.transitions[i][0][1][0][0]
                if not (node_from, node_to) in graph.edges:
                    graph.add_edge(node_from, node_to)
                    edges_labels_multiples[(node_from, node_to)] = ""

            for i in range(len(self.transitions)):
                node_from = self.transitions[i][0][0][0][0]
                node_to = self.transitions[i][0][1][0][0]
                first_label = self.transitions[i][0][1][0][1]
                second_label = self.transitions[i][0][1][1][1]
                if (node_from, node_to) in edges_labels_multiples.keys():
                    edges_labels_multiples[(node_from, node_to)] += f" {first_label} {second_label}"
                elif (node_to, node_from) in edges_labels_multiples.keys():
                    edges_labels_multiples[(node_to, node_from)] += f" {first_label} {second_label}"

            for key in edges_labels_multiples.keys():
                labels = edges_labels_multiples[key].split(" ")
                _ = labels.pop(0)
                new_list = []
                for element in labels:
                    if element not in new_list:
                        new_list.append(element)
                str_labels = ""
                for element in new_list:
                    str_labels += element
                    str_labels += ","
                str_labels = str_labels[0:-1]
                edges_labels[key] = str_labels

        return graph, edges_labels

    def reverse(self):
        '''
        A^r = A with reversed transitions
        '''
        Q = self.states
        Sigma = self.alphabet
        q_0 = self.finals_states[0]
        F = [self.initial_state]

        # reversed transitions

        transitions = []

        for i in range(len(self.transitions)):
            state_1 = self.transitions[i][0][0]
            state_2 = self.transitions[i][0][1]
            caract = self.transitions[i][1]
            curr_transition = [(state_2, state_1), caract]
            transitions.append(curr_transition)
        
        return Automaton(Q, Sigma, transitions, q_0, F)

    def set_initial_state(self, q_0):
        self.initial_state = q_0

    def set_final_state(self, F):
        if isinstance(F, str):
            print("Need a [].")
            return -1
    
        for element in F:
            self.finals_states.append(element)

    def display(self):
        print(f"Automata : \nQ = {self.states}\nSigma = {self.alphabet}\nq_0 = {self.initial_state}\nF = {self.finals_states}")
        # print("\nDelta = ", self.transitions)
        print("Transitions : ")
        if len(self.transitions) > 0:
            for i in range(len(self.transitions)):
                print(f"{self.transitions[i][0][0]} <--> {self.transitions[i][0][1]} : {self.transitions[i][1]}")
        print("\n------------------------------")
        print("\n")

    def intersection(self, A2):
        '''
        Intersection beetween 2 automatas.
        '''
        # self.states = Q
        # self.alphabet = Sigma
        # self.transitions = delta
        # self.initial_state = q_0
        # self.finals_states = F

        ## Q
        new_states = []

        for state in self.states:
            for state_A2 in A2.states:
                new_states.append((state, state_A2))

        ## Sigma
        new_sigma = set(self.alphabet) & set(A2.alphabet)

        ## delta
        delta = []
        for transition in self.transitions:
            state_from = transition[0][0]
            state_to = transition[0][1]
            caracts = transition[1]
            for transitions_A2 in A2.transitions:
                state_from_A2 = transitions_A2[0][0]
                state_to_A2 = transitions_A2[0][1]
                caracts_A2 = transitions_A2[1]
                if caracts[0] == caracts_A2[0]:
                    delta.append( [ ( (state_from, state_from_A2), (state_to, state_to_A2)), [ caracts[0] ] ] )

        ## q_0
        new_initial = (self.initial_state, A2.initial_state)

        ## F

        new_final = []

        for final in self.finals_states:
            for final_A2 in A2.finals_states:
                new_final.append((final, final_A2))
        
        return Automaton(new_states, new_sigma, delta, new_initial, new_final)

    def clear2(self):
        """
        Optimizes a finite automaton by removing states that are not reachable
        or do not lead to a final state.

        return : 
        - optimized_automaton : The optimized automaton.
        """

        reachable_states_from_finals = set()
        queue = []
        for element in self.finals_states:
            queue.append(element)
        cleared_transitions_reach = []

        while queue:
            current_state = queue.pop(0)
            # Traversing transitions to find the next reachable states
            for transition in self.transitions:
                from_state = transition[0][0]
                to_state = transition[0][1]
                
                # Check if the current state matches the arrival state of the transition
                if to_state == current_state:
                    if transition not in cleared_transitions_reach:
                        cleared_transitions_reach.append(transition)
                    reachable_states_from_finals.add(current_state)
                    next_state = from_state
                    reachable_states_from_finals.add(next_state)
                    queue.append(next_state)
        
        reachable_states = set()
        queue = [self.initial_state]
        reachable_states.add(self.initial_state)
        cleared_transitions = []

        while queue:
            current_state = queue.pop(0)
            
            # Traversing transitions to find the next reachable states
            for transition in self.transitions:
                from_state = transition[0][0]
                to_state = transition[0][1]
                
                # Check if the current state matches the starting state of the transition
                if from_state == current_state:
                    if transition not in cleared_transitions:
                        cleared_transitions.append(transition)
                    next_state = to_state
                    reachable_states.add(next_state)
                    queue.append(next_state)
        
        cleared_reachables_states = reachable_states & reachable_states_from_finals
        cleared_transitions_final = [item for item in cleared_transitions_reach if item in cleared_transitions]

        cleared_alphabet = []
        for item in cleared_transitions_final:
            for element in item[1]:
                cleared_alphabet.append(element)

        self.alphabet = set(cleared_alphabet)
        self.finals_states = set([item for item in self.finals_states if item in cleared_reachables_states])

        self.states = set(cleared_reachables_states)
        self.transitions = cleared_transitions_final

    def clear(self):
        """
        Optimizes a finite automaton by removing states that are not reachable
        or do not lead to a final state.

        return : 
        - optimized_automaton : The optimized automaton.
        """

        # print(" -------------------------------------- ")

        reachable_states_from_finals = set()
        queue = list(self.finals_states)
        cleared_transitions_reach = []
        state_already_seen = []

        # Find states that are not reachables from finals
        while queue:
            current_state = queue.pop(0)
            reachable_states_from_finals.add(current_state)
            # Stoping condition
            if current_state in state_already_seen:
                continue
            state_already_seen.append(current_state)

            for transition in self.transitions:
                from_state, to_state = transition[0]
                # Check if the current state matches the arrival state of the transition
                if to_state == current_state:
                    cleared_transitions_reach.append(transition)
                    next_state = from_state
                    queue.append(next_state)
        
        reachable_states = set()
        queue = [self.initial_state]
        cleared_transitions = []
        state_already_seen = []

        # Do not lead to finals
        while queue:
            current_state = queue.pop(0)
            reachable_states.add(current_state)
            # Stoping condition
            if current_state in state_already_seen:
                continue
            state_already_seen.append(current_state)
            # Traversing transitions to find the next reachable states
            for transition in self.transitions:
                from_state, to_state = transition[0]
                # Check if the current state matches the starting state of the transition
                if from_state == current_state:
                    cleared_transitions.append(transition)
                    next_state = to_state
                    queue.append(next_state)
        
        cleared_transitions_final = [item for item in cleared_transitions_reach if item in cleared_transitions]
        cleared_alphabet = [element for _, alphabet in cleared_transitions_final for element in alphabet]

        self.alphabet = set(cleared_alphabet)
        self.finals_states = set(self.finals_states) & reachable_states & reachable_states_from_finals
        # States: reachable and reachable from a state
        self.states = set(reachable_states & reachable_states_from_finals)
        self.transitions = cleared_transitions_final

    def save(self, filename):

        automate_data = {
        "type": "automaton",
        "states": [],
        "transitions": []
        }

        # Formatting transitions to add them to the data structure
        for transition in self.transitions:
            from_state = transition[0][0]
            to_state = transition[0][1]
            symbol = transition[1]
            automate_data["transitions"].append({
                "from": from_state,
                "to": to_state,
                "symbol": symbol
            })
        for state in self.states:
            if state == self.initial_state:
                initial = True
            else:
                initial = False
            if state in self.finals_states:
                final = True
            else:
                final = False
            automate_data["states"].append({
                "name": state,
                "initial": initial,
                "accepting": final
            })
        # Writes the data structure to a JSON file
        with open(filename, 'w') as json_file:
            json.dump(automate_data, json_file, indent=4)

if __name__ == "__main__":    
    # Automata = Automaton(["A", "B", "C"], ["a", "b", "c"], [[("A", "B"), ["a", "b", "c"]], [("B", "C"), ["b"]]], q_0="A", F=["C"])
    # Automata.save("automataa.json")
    # Automata_empty = Automaton([], [], [], q_0="", F=[])
    parser = Parser("Automata.json")
    Q, Sigma, delta, q_0, F = parser.parse()
    Automata_parser = Automaton(Q, Sigma, delta, q_0, F)

    # print("\nRandom example : ")
    # Automata.display()
    print("\nRandom example (parser) :")
    # Automata_parser.display()
    # print("\nEmpty example : ")
    # Automata_empty.display()