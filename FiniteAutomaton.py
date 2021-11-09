import collections
from typing import Dict, Tuple, Set, List

class FiniteAutomaton:
    def __init__(self, initialState: str, states: Set[str], finalStates: Set[str], alphabet: Set[str], transitions: Dict[Tuple[str, str], List[str]]):
        self.initialState = initialState
        self.states = states
        self.finalStates = finalStates
        self.alphabet = alphabet
        self.transitions = transitions

    def checkIfDeterministic(self) -> bool:
        for _, state2 in self.transitions.items():
            if len(state2) > 1:
                return False
        return True

    def trySequence(self, sequence: str) -> bool:
        if not self.checkIfDeterministic():
            return False
        idx = 0
        currentState = self.initialState
        if len(sequence) == 0:
            if currentState in self.finalStates:
                return True
            else:
                return False
        for char in sequence:
            if char not in self.alphabet:
                return False
            states = self.transitions[(currentState, char)]
            if len(states) == 0:
                return False
            idx += 1
            currentState = states[0]
        return True

    @staticmethod
    def parse(filename: str) -> 'FiniteAutomaton':
        FA = FiniteAutomaton("", set(), set(), set(), collections.defaultdict(list))
        with open(filename, "r") as f:
            states = f.readline().split()
            FA.initialState = states[0]
            FA.states = set(states)
            FA.finalStates = set(f.readline().split())
            FA.alphabet = set(f.readline().split())
            while f:
                transition = f.readline().split()
                if not transition:
                    break
                state1 = transition[0]
                character = transition[1]
                state2 = transition[2]
                FA.transitions[(state1, character)].append(state2)

        return FA