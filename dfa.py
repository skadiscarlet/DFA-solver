class DFA():
    def __init__(self, start: str, ends: list[str],states: list[str] ,symbols:list[str], moves:list[list[str|None]]):
        self.symbols = symbols
        self.moves = []
        self.ends = []
        __tmp_states = []
        move_stack = {}
        
        DFA_stack = {}
        closure_stack = {}
        for __state in states:
            closure_stack[__state] = self.__epsilon_closure(moves, __state)
        # print(moves)
        for [init, symbol, target] in moves:
            if symbol is None:
                continue
            if (init, symbol) in move_stack.keys():
                move_stack[(init, symbol)] = move_stack[(init, symbol)] | closure_stack.get(target)
            else:
                move_stack[(init, symbol)] = closure_stack.get(target)
            # print(move_stack)
        __tmp_states.append(closure_stack.get(start))
        
        for __tmp_state in __tmp_states:
            for symbol in symbols:
                __tmp_target = set()
                
                for __tmp_state_item in __tmp_state:
                    if (__tmp_state_item, symbol) in move_stack.keys():
                        # print((__tmp_state_item, symbol))
                        __tmp_target = __tmp_target | move_stack[(__tmp_state_item, symbol)]
                if __tmp_target:
                    DFA_stack[(tuple(__tmp_state), symbol)] = __tmp_target
                    
                    if __tmp_target not in __tmp_states:
                        __tmp_states.append(__tmp_target)
                # print(DFA_stack, __tmp_states)
        for key in DFA_stack.keys():
            self.moves.append([f"S{__tmp_states.index(set(key[0]))}", key[1], f"S{__tmp_states.index(DFA_stack[key])}"])

        for __tmp_state in __tmp_states:
            if start in __tmp_state:
                self.start = f"S{__tmp_states.index(__tmp_state)}"
        # print(__tmp_states)
        # print(ends)
        for __tmp_state in __tmp_states:
            for end in ends:
                if end in __tmp_state:
                    self.ends.append(f"S{__tmp_states.index(__tmp_state)}")

        self.states = [f"S{index}" for index in range(len(__tmp_states))]
    
    def __epsilon_closure(self, move, state):
        closure = set([state])
        stack = [state]
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
        result = " ".join(self.states)
        result += "\nsymbos: " + " ".join(self.symbols)
        result += "\nends: " + " ".join(self.ends)
        result += "\nstart: " + self.start
        result += "\nmoves: "
        for move in self.moves:
            result += "\n- " + " ".join(move)
        return result      
    
    def __invert__(self):
        self.completes()
        # print(self)
        ends = self.states.copy()
        for e in self.ends:
            ends.remove(e)
        return DFA(self.start, ends, self.states, self.symbols, self.moves)
    
    def completes(self):
        graph = {}
        for [source, symbol, target ] in self.moves:
            if source not in graph.keys():
                graph[source] = {}
            graph[source][symbol] = target
        virtual_node = None
        # print(graph)
        for key, value in graph.items():
            # print(key, value)
            if value.keys() != self.symbols:
                if virtual_node is None:
                    virtual_node = "virtual_node"
                    self.states.append("virtual_node")
                    for symbol in self.symbols:
                        self.moves.append(["virtual_node", symbol,"virtual_node"])
                        
                for loss in set(self.symbols) - set(value.keys()):
                    self.moves.append([key, loss, "virtual_node"])

    def __or__(self, other):
        start = "S_tmp"
        end = "E_tmp"
        states = self.states + [end, start] + [f"{s}_1" for s in other.states]
        moves = self.moves + [[f"{s1}_1", s2, f"{s3}_1"] for [s1, s2, s3] in other.moves] + [[start, None, self.start], [start, None, f"{other.start}_1"]] + [[e, None, end] for e in self.ends] + [[f"{other_end}_1", None, end] for other_end in other.ends]
        # print(end, start, states, moves)
        return DFA(start, [end], states, list(set(self.symbols + other.symbols)), moves)
    
    def __eq__(self, other) -> bool:
        tmp_1 = ~(~self|other)
        # print(~self)
        tmp_2 = ~(self|~other)
        # print(~other)
        return not tmp_1.check_result_exist() and not  tmp_2.check_result_exist()

    def no_circle_DFS_for_DFA(self, findone):
        graph = {}
        for [source, symbol, target ] in self.moves:
            if source not in graph.keys():
                graph[source] = {}
            graph[source][target] = symbol
        results = []
        from collections import deque
        queue =  deque([(self.start, [self.start], [])])
        while queue:
            (node, path, result) = queue.popleft()
            next_node_set = set(graph.get(node).keys() if graph.get(node) is not None else [])
            for next_node in next_node_set - set(path):
                tmp_result = result + [graph[node][next_node]]
                if next_node in self.ends:
                    if findone:
                        return "".join(tmp_result)
                    results.append("".join(tmp_result))
                else:
                    queue.append((next_node, path + [next_node], tmp_result))

        return results
    
    def check_result_exist(self, findone = True):
        return len(self.no_circle_DFS_for_DFA(findone)) != 0