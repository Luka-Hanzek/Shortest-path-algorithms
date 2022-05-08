from utils.input_parser import Parser
from algorithms.search_algorithms import BFS, UCS, A_STAR
from algorithms.heuristic_check import HeuristicCheck
import argparse

if(__name__=="__main__"):
    flags_parser = argparse.ArgumentParser()
    input_parser = Parser()

    #parse flags
    flags_parser.add_argument('--alg', action="store", dest='alg', default=None)
    flags_parser.add_argument('--ss', action="store", dest='ss', default=None)
    flags_parser.add_argument('--h', action="store", dest='h', default=None)
    flags_parser.add_argument('--check-optimistic', action="store", dest='check_optimistic', nargs='?', const="0", default=None)
    flags_parser.add_argument('--check-consistent', action="store", dest='check_consistent', nargs='?', const="0", default=None)
    args = flags_parser.parse_args()
    
    #parse data
    state_space_descriptor=input_parser.parseStateSpaceDescription(args.ss)
    

    if(args.alg == "bfs"):
        print("# BFS")
        searchResult = BFS.search(state_space_descriptor.starting_state, state_space_descriptor.ending_states, state_space_descriptor.transitions)
        print(searchResult.getFormattedOutput())
    elif(args.alg == "ucs"):
        print("# UCS")
        searchResult = UCS.search(state_space_descriptor.starting_state, state_space_descriptor.ending_states, state_space_descriptor.transitions)
        print(searchResult.getFormattedOutput())
    elif(args.alg == "astar"):
        heuristic_descriptor = input_parser.parseHeuristicDescriptor(args.h)
        heuristic_file_name = args.h.split('\\')[-1]
        print(f"# A-STAR {heuristic_file_name}")
        searchResult = A_STAR.search(state_space_descriptor.starting_state, state_space_descriptor.ending_states, state_space_descriptor.transitions, heuristic_descriptor.pairs)
        print(searchResult.getFormattedOutput())
    elif(args.check_optimistic == "0"):
        heuristic_file_name = args.h.split('\\')[-1]
        print(f"# HEURISTIC_OPTIMISTIC {heuristic_file_name}")
        heuristic_descriptor = input_parser.parseHeuristicDescriptor(args.h)
        result = HeuristicCheck.checkOptimisitc(state_space_descriptor, heuristic_descriptor)
        print(result.getFormattedOutput())
    elif(args.check_consistent != None):
        heuristic_file_name = args.h.split('\\')[-1]
        print(f"# HEURISTIC_CONSISTENT {heuristic_file_name}")
        heuristic_descriptor = input_parser.parseHeuristicDescriptor(args.h)
        result = HeuristicCheck.checkConsistent(state_space_descriptor, heuristic_descriptor)
        print(result.getFormattedOutput())
    else:
        print("Invalid input")
