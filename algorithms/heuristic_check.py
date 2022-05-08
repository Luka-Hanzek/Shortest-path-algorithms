from data_strucutres.descriptors import StateSpaceDescriptor, HeuristicDescriptor, ConsistentDescriptor, OptimisticDescriptor
from algorithms.search_algorithms import UCS

class HeuristicCheck:
    @staticmethod
    def checkConsistent(state_space_descriptor: StateSpaceDescriptor, heuristic_descriptor: HeuristicDescriptor):
        states = sorted(state_space_descriptor.states, key=lambda x: x)
        consistent_descriptor = ConsistentDescriptor()
        for state_from in states:
            states_to = state_space_descriptor.getStateTransitions(state_from)
            for state_to, cost in states_to:
                consistent_descriptor.addEntry(state_from, state_to, heuristic_descriptor.getStateHeuristic(state_from), heuristic_descriptor.getStateHeuristic(state_to), cost)
        
        return consistent_descriptor

    def checkOptimisitc(state_space_descriptor: StateSpaceDescriptor, heuristic_descriptor: HeuristicDescriptor):
        states = sorted(state_space_descriptor.states, key=lambda x: x)
        optimistic_descriptor = OptimisticDescriptor()

        for state in states:
            search_result = UCS.search(state, state_space_descriptor.ending_states, state_space_descriptor.transitions)
            optimistic_descriptor.addEntry(state, search_result.total_cost, heuristic_descriptor.getStateHeuristic(state))
        
        return optimistic_descriptor