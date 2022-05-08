from data_strucutres.descriptors import SearchResult, Node
from data_strucutres.priority_queue import PriorityQueue
import queue


class UCS:
    @staticmethod
    def search(starting_state: str, ending_states: list[str], transitions: dict) -> SearchResult:
        """Finds shortest path
        
        Returns:
            SearchResult: Information about search
        """
        states_visited = set()
        p_q = queue.PriorityQueue()
        starting_node = Node(starting_state, 0.0, None)
        p_q.put((starting_node.cost, starting_node))

        while(not p_q.empty()):
            current_node = p_q.get()[1]
            states_visited.add(current_node.name)
            #found solution
            if(current_node.name in ending_states):
                return SearchResult(True, len(states_visited), current_node.getChainLength(), current_node.cost, current_node.getPath(), current_node)
            neighbour_states = transitions[current_node.name]
            next_nodes = UCS.expand(neighbour_states, current_node, states_visited)
            for node in next_nodes:
                p_q.put((node.cost, node))

            

        return SearchResult(False)

    @staticmethod
    def expand(transitions: list[tuple[str, float]], current_node: Node, states_visited) -> list[Node]:
        """Creates Node objects from all the states that are neighbours to current_node
        
        Returns:
            list[Node]: list of neigbouring nodes
        """
        new_nodes = []
        for next_state, cost in transitions:
            #don't make cycles
            if(next_state not in states_visited):
                x = Node(next_state, current_node.cost + cost, current_node)
                new_nodes.append(x)
        
        return new_nodes
            
class BFS:
    """Breadth first search used to find shortest path in graph with constant weight edges"""
    @staticmethod
    def search(starting_state: str, ending_states: list[str], transitions: dict) -> SearchResult:
        """Finds shortest path
        
        Returns:
            SearchResult: Information about search
        """
        starting_node = Node(starting_state, 0.0, None)
        states_visited = set()
        q = queue.Queue()
        q.put(starting_node)

        while(not q.empty()):
            current_node = q.get()
            states_visited.add(current_node.name)
            neighbour_states = transitions[current_node.name]
            if(current_node.name in ending_states):
                return SearchResult(True, len(states_visited), len(current_node.getChain()), current_node.cost, current_node.getPath(), current_node)
            next_nodes = BFS.expand(neighbour_states, current_node, states_visited)
            for node in next_nodes:
                q.put(node)
            

        return SearchResult(False)

    @staticmethod
    def expand(transitions: list[tuple[str, float]], current_node: Node, states_visited: list[str]) -> list[Node]:
        """Creates Node objects from all the states that are neighbours to current_node
        
        Returns:
            list[Node]: list of neigbouring nodes
        """
        new_nodes = []
        for next_state, cost in transitions:
            #don't make cycles
            if(next_state not in states_visited):
                x = Node(next_state, current_node.cost + cost, current_node)
                new_nodes.append(x)
        
        return new_nodes
    


class A_STAR:
    """"A* shortest path algorithm"""
    @staticmethod
    def search(starting_state: str, ending_states: list[str], transitions: dict, heuristic: dict):
        """Finds shortest path
        
        Returns:
            SearchResult: Information about search
        """
        open = PriorityQueue(optimization_key_extractor=lambda x: x.name)
        closed = {}
        starting_node = Node(starting_state, 0.0, None)
        open.insert(starting_node, heuristic[starting_state])

        while(not open.empty()):    
            current_node = open.get()
            if current_node.name in ending_states:
                return SearchResult(True, len(closed), current_node.getChainLength(), current_node.cost, current_node.getPath(), current_node)
            closed[current_node.name] = current_node

            for node in A_STAR.expand(transitions[current_node.name], current_node):
                #search "open" for nodes with same state name
                #if we find existing node in "open" we don't need to search "closed"
                existing_node = open.getElement(node)
                if(existing_node != None):
                    if(existing_node.cost > node.cost):
                        #we found shorter path -> modify node in "open"
                        open.modifyElement(element = node, new_element=node, new_priority=node.cost + heuristic[node.name])
                else:
                    #search "closed" for nodes with same state name
                    try:
                        existing_node = closed[node.name]
                    except KeyError as e:
                        #no existing node found in "closed" -> add node to "open"
                        open.insert(node, node.cost + heuristic[node.name])
                        
                    if(existing_node != None and existing_node.cost > node.cost):
                        #we found better path -> delete node from "closed" and insert one with shorter path in "open"
                        del closed[existing_node.name]
                        open.insert(node, node.cost + heuristic[node.name])
        
        return SearchResult(False)

    def expand(transitions: list[tuple[str, float]], current_node: Node) -> list[Node]:
        """Creates Node objects from all the states that are neigbours to current_node
        
        Attributes:
            transitions (list[tuple[str, float]]): Transitions with cost
            current_node (Node): Node from which to transition
        Returns:
            list[Node]: list of neigbouring nodes
        """
        new_nodes = []
        for next_state, cost in transitions:
            new_nodes.append(Node(next_state, current_node.cost + cost, current_node))

        return new_nodes
        
