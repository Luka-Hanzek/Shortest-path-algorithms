from enum import Enum, auto
from data_strucutres.descriptors import StateSpaceDescriptor, HeuristicDescriptor
import string


class Parser:
    """Used to parse state space and heuristic space"""
    allowed_characters = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + "_ščćđžŠČĆĐŽ")

    class ParserStates(Enum):
        READING_STARTING_STATE=auto()
        READING_ENDING_STATES=auto()
        READING_TRANSITIONS=auto()

    @staticmethod
    def checkValidString(str_to_check: str) -> bool:
        """Checks if string contains characters: _ščćđžŠČĆĐŽ + ascii_lowercase + ascii_uppercase + digits
        Args:
            str_to_check (str): String to check
        Returns:
            bool: True if str_to_check contains only specified characters, False otherwise
        """
        return set(str_to_check) <= Parser.allowed_characters

    @staticmethod
    def checkValidNumber(str_to_check: str) -> bool:
        """Checks if string can be converted to number
        Args:
            str_to_check (str): String to check if it can be converted to number
        Returns:
            bool: True if str_to_check can be converted to number, False otherwise
        """
        try:
            float(str_to_check)
        except ValueError as e:
            return False
        
        return True

    @staticmethod
    def illegalString(line: str) -> None:
        print(f"\"{line}\" contains illegal character")
        exit()
    
    @staticmethod
    def illegalNumber(line: str) -> None:
        print(f"\"{line}\" cannot be parsed to number")
        exit()

    @staticmethod
    def parseStateSpaceDescription(filePath: str) -> StateSpaceDescriptor:
        """Parse state space
        Args:
            filePath (str): Path to file
        Returns:
            StateSpaceDescriptor: State space descriptor
        """
        parser_state = Parser.ParserStates.READING_STARTING_STATE
        state_space_descriptor = StateSpaceDescriptor()

        file = open(filePath, encoding="utf-8")

        for line in file.readlines():
            #remove newline
            line = line.strip()
            if(not line.startswith('#')):
                if(parser_state==Parser.ParserStates.READING_TRANSITIONS):
                    #parse transitions
                    pos = line.find(":")
                    fromState = line[0:pos]
                    if(not Parser.checkValidString(fromState)):
                        Parser.illegalString(fromState)
                    #remove ":\s"
                    line=line[pos+2:]
                    if(line == ''):
                        toStates=[]
                    else:
                        toStates=[tuple(x.split(",")) for x in line.split(" ")]
                        for toStateWCost in toStates:
                            if(not Parser.checkValidString(toStateWCost[0])):
                                Parser.illegalString(toStateWCost[0])
                            if(not Parser.checkValidNumber(toStateWCost[1])):
                                Parser.illegalNumber(toStateWCost[1])

                        toStates = [(x[0], float(x[1])) for x in toStates]
                    state_space_descriptor.setTransitions(fromState, toStates)
                elif(parser_state==Parser.ParserStates.READING_STARTING_STATE):
                    #parse ending states
                    #check if line contains valid characters
                    if(not Parser.checkValidString(line)):
                        Parser.illegalString(line)
                    state_space_descriptor.starting_state = line
                    parser_state=Parser.ParserStates.READING_ENDING_STATES
                elif(parser_state==Parser.ParserStates.READING_ENDING_STATES):
                    #parse starting state
                    ending_states = line.split(" ")
                    if(ending_states[-1]==""):
                        Parser.illegalString(ending_states[len(ending_states) - 2] + " ")
                    for state in ending_states:
                        if(not Parser.checkValidString(state)):
                            Parser.illegalString(state)
                    state_space_descriptor.ending_states = ending_states
                    parser_state=Parser.ParserStates.READING_TRANSITIONS
            else:
                #process comment
                pass
        file.close()
        return state_space_descriptor

    @staticmethod
    def parseHeuristicDescriptor(filePath: str) -> HeuristicDescriptor:
        """Parse heuristic space
        Args:
            filePath (str): Path to file
        Returns:
            HeuristicSpaceDescriptor: Heuristic space descriptor
        """
        file = open(filePath, encoding="utf-8")
        heuristic_descriptor = HeuristicDescriptor()
        
        for line in file.readlines():
            line = line.strip()
            pos = line.find(":")
            state = line[0:pos]
            if(not Parser.checkValidString(state)):
                Parser.illegalString(state)
            value = line[pos+2:]
            if(not Parser.checkValidNumber(value)):
                Parser.illegalNumber(value)
            heuristic_descriptor.addPair(state, float(value))

        file.close()

        return heuristic_descriptor
