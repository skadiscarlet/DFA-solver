class DFA():
    def __init__(self, start: str, ends: list[str|None],states: list[str] ,symbols:list[str|None], moves:list[list[str|None]]):
        self.symbols = symbols
        self.moves = []
        self.ends = []
        __tmp_states = []
        move_stack = {}
        
        DFA_stack = {}
        closure_stack = {}
        for __state in states:
            closure_stack[__state] = self.__epsilon_closure(moves, __state)

        for [init, symbol, target] in moves:
            if symbol is None:
                continue
            if (init, symbol) in move_stack.keys():
                move_stack[(init, symbol)] |= closure_stack.get(target)
            else:
                move_stack[(init, symbol)] = closure_stack.get(target)

        __tmp_states.append(closure_stack.get(start))
        
        for __tmp_state in __tmp_states:
            for symbol in symbols:
                __tmp_target = set()
                
                for __tmp_state_item in __tmp_state:
                    if (__tmp_state_item, symbol) in move_stack.keys():
                        __tmp_target |= move_stack[(__tmp_state_item, symbol)]
            
                DFA_stack[(tuple(__tmp_state), symbol)] = __tmp_target
                    
                if __tmp_target not in __tmp_states:
                    __tmp_states.append(__tmp_target)
                print(DFA_stack, __tmp_states)
        for key in DFA_stack.keys():
            self.moves.append([f"S{__tmp_states.index(set(key[0]))}", key[1], f"S{__tmp_states.index(DFA_stack[key])}"])

        for __tmp_state in __tmp_states:
            if start in __tmp_state:
                self.start = f"S{__tmp_states.index(__tmp_state)}"

        for __tmp_state in __tmp_states:
            for end in ends:
                if end in __tmp_state:
                    self.ends.append(f"S{__tmp_states.index(__tmp_state)}")

        self.states = [f"S{index}" for index in range(len(__tmp_states))]
    
    def __epsilon_closure(self, move, states):
        closure = set(states)
        stack = list(states)

        while stack:
            current_state = stack.pop()
            for transition in move:
                if transition[0] == current_state and transition[1] is None:
                    next_state = transition[2]
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)

        return closure
    
    def __str__(self):
        result = ""
        result += "symbos: " + "".join(self.symbols)
        result += "ends: " + " ".join(self.ends)
        result += "start: " + self.start
        result += "moves: "
        for move in self.moves:
            result += "- " + " ".join(move)
        return result      
    
    def __invert__(self):
        start = "S_tmp"
        states = self.states.append(start)
        ends = [self.start]
        moves = self.moves + [[start, None, s] for s in self.ends]
        return DFA(start, ends, states, self.symbols, moves)
        
    def __or__(self, other):
        start = "S_tmp"
        end = "E_tmp"
        states = self.states + [end, start] + [f"{s}_1" for s in other.states]
        moves = self.moves + [[f"{s1}_1", s2, f"{s3}_1"] for [s1, s2, s3] in other.moves] + [[start, None, self.start], [start, None, other.start]] + [[e, None, end] for e in self.ends] + [[other_end, None, end] for other_end in other.ends]
        return DFA(start, [end], states, self.symbols + other.symbols, moves)
    
    def __eq__(self, other) -> bool:
        tmp_1 = ~(~self|other)
        tmp_2 = ~(self|~other)
        return not tmp_1.check_result_exist() and not  tmp_2.check_result_exist()

    def __DFS_for_DFA(self):
        pass
    def check_result_exist(self):
        pass
    

                