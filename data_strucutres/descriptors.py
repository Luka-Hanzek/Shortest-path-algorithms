class Node:
        """Node represents a node in a weighted graph.
        
        Attributes:
            _name (str): Name of the node
            _cost (float): Cost of the total path in node chain which can be reconstructed by itteratively retrieving _prev_node
            _prev_node: Child node in the node chain
        """
        def __init__(self, name: str, cost: float, prev_node: "Node"):
            self.name = name
            self.cost = cost
            self.prev_node = prev_node
        
        def getChainLength(self) -> int:
            return len(self.getChain())

        def getChain(self) -> list["Node"]:
            """Get list of all node names in the chain"""
            node_temp = self
            chain = []

            while(node_temp != None):
                chain.append(node_temp.name)
                node_temp = node_temp.prev_node

            return chain

        def getPath(self) -> str:
            """Gets string representation of chain
            
            Returns:
                str: String of format "str => str => ..."
            """
            s=""
            node_temp = self
            path_list = []
            while(node_temp.prev_node != None):
                path_list.append(node_temp.name)
                node_temp = node_temp.prev_node

            path_list.append(node_temp.name)

            path_list.reverse()

            for name in path_list:
                s += f"{name} => "
            
            return s[:len(s)-3]

        def __ge__(self, __o: 'Node') -> bool:
            if(self.cost == __o.cost):
                return self.name >= __o.name
            return self.cost >= __o.cost

        def __gt__(self, __o: 'Node') -> bool:
            if(self.cost == __o.cost):
                return self.name > __o.name
            return self.cost > __o.cost

        def __le__(self, __o: 'Node') -> bool:
            if(self.cost == __o.cost):
                return self.name <= __o.name
            return self.cost <= __o.cost

        def __lt__(self, __o: 'Node') -> bool:
            if(self.cost == __o.cost):
                return self.name < __o.name
            return self.cost < __o.cost

        def __eq__(self, __o: object) -> bool:
            try:
                if(self.name != __o.name):
                    return False
                if(self.cost != __o.cost):
                    return False
                if(self.prev_node != __o.prev_node):
                    return False
                return True
            except AttributeError as e:
                return False

        def __str__(self) -> str:
            return f"{self._name} {self._cost}"

class StateSpaceDescriptor:
    """Descriptor used to store information about state space
    
    Attributes:
        starting_state: State from which to start search
        ending_sates: States which end the search if found
        transitions: Transition between states and its cost
    """
    def __init__(self):
        self.starting_state = None
        self.ending_states = []
        self.transitions = {}

    def addTransition(self, fromState: str, toState: str, cost: float) -> None:
        """Adds a transition to descriptor
        
        Args:
            fromState (str): State from which to transition
            toState (str): State to which to transition
            cost (float): Cost of the transition
        """
        try:
            self.transitions[fromState].append((toState, cost))
        except KeyError as e:
            self.transitions[fromState] = []
            self.transitions[fromState].append((toState, cost))

    def setTransitions(self, fromState: str, toStates: list[tuple[str, float]]) -> None:
        """Adds a transition to descriptor
        
        Args:
            fromState (str): State from which to transition
            toStates (list[tuple[str, float]]): list of transitions with costs
        """
        self.transitions[fromState] = toStates

    def getStateTransitions(self, state: str) -> list[tuple[str, float]]:
        """Gets all the transitions of the specified state
        
        Args:
            state (str): State from which to transition

        Returns:
            list[tuple[str, float]]: list of transitions with costs
        """
        return self.transitions[state]

    @property
    def states(self):
        states = []
        for state, transitions in self.transitions.items():
            states.append(state)

        return states

    def __str__(self) -> str:
        s="--State space descriptor--\n"
        s+=f"Starting state: {self.starting_state}\n"
        s+=f"Ending states: {self.ending_states.__str__()}\n"
        s+="\n".join([f"{x[0]}->{x[1].__str__()}" for x in self.transitions.items()])

        return s


class HeuristicDescriptor:
    """Descriptor used to store information about state heuristics
    
    Attributes:
        pairs (dict of str: float): Heuristic values of states
    """
    def __init__(self):
        self.pairs = {}

    def addPair(self, state: str, value: float) -> None:
        """Adds heuristic to state
        
        Args:
            state (str): State name
            value (float): Heuristic value
        """
        self.pairs[state] = value

    def __str__(self) -> str:
        s="--Heuristic descriptor--\n"
        for k,v in self.pairs.items():
            s+=f"{k}->{v}\n"

        return s

    def getStateHeuristic(self, state: str) -> float:
        """Gets heuristic value of the specified state
        
        Args:
            state (str): Name of the state

        Returns:
            flaot: Heuristic value of the specified state
        """
        return self.pairs[state]


class SearchResult:
    """Contains data about search result

    Attributes:
            found_solution (bool): True if solution is found, False otherwise
            states_visited (int): Number of states algorithm visited during search
            path_length (int): Number of nodes in shortest path to goal state
            total_cost (float): Total cost of shortest path to goal state
            path (str): String representation of shortest path to goal state
            node (Node): Node representing goal state
    """
    def __init__(self, found_solution: bool, states_visited: int = None, path_length: int = None, total_cost: float = None, path: str = None, node: Node = None):
        self.found_solution = found_solution
        self.states_visited = states_visited
        self.path_length = path_length
        self.total_cost = total_cost
        self.path = path
        self.node = node

    def getFormattedOutput(self) -> str:
        """Returns formatted output of SearchResult
        
        Returns:
            str:
                "[FOUND_SOLUTION]: yes"
                "[STATES_VISITED]: {self._states_visited}"
                "[PATH_LENGTH]: {self._path_length}"
                "[TOTAL_COST]: {self._total_cost}"
                "[PATH]: {self._path}"
                
                if soulution found

                "[FOUND_SOLUTION]: no"

                otherwise
        """
        s=""
        
        if(self.found_solution):
            s += "[FOUND_SOLUTION]: yes\n"
            s += f"[STATES_VISITED]: {self.states_visited}\n"
            s += f"[PATH_LENGTH]: {self.path_length}\n"
            s += f"[TOTAL_COST]: {self.total_cost}\n"
            s += f"[PATH]: {self.path}"
        else:
            s += "[FOUND_SOLUTION]: no"
        
        return s


class ConsistentDescriptor:
    def __init__(self):
        self.entries = {}

    def addEntry(self, state_from, state_to, state_from_h, state_to_h, cost):
        self.entries[(state_from, state_to)] = (state_from_h, state_to_h, cost)

    def getFormattedOutput(self):
        s = ""
        consistent = True
        for states, values in self.entries.items():
            state_from = states[0]
            state_to = states[1]
            state_from_h = values[0]
            state_to_h = values[1]
            cost = values[2]
            entry_result = None
            if(state_from_h <= state_to_h + cost):
                entry_result = "[OK]"
            else:
                entry_result = "[ERR]"
                consistent = False
            s += f"[CONDITION]: {entry_result} h({state_from}) <= h({state_to}) + c: {state_from_h} <= {state_to_h} + {cost}\n"

        s += f"[CONCLUSION]: Heuristic {'is' if consistent is True else 'is not'} consistent."
        
        return s


class OptimisticDescriptor:
    def __init__(self):
        self.entries = {}

    def addEntry(self, state, cost, heuristic):
        self.entries[state] = (cost, heuristic)

    def getFormattedOutput(self):
        s = ""
        optimistic = True
        for state, entry in self.entries.items():
            cost, heuristic = entry
            entry_result = None
            if(entry[1] <= entry[0]):
                entry_result = "[OK]"
            else:
                entry_result = "[ERR]"
                optimistic = False
            s += f"[CONDITION]: {entry_result} h({state}) <= h*: {heuristic} <= {cost}\n"

        s += f"[CONCLUSION]: Heuristic {'is' if optimistic is True else 'is not'} optimistic."

        return s