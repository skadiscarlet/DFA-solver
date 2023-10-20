from dfa import DFA

start = "S0"
end = ['S4']
symbols = ["a", "b"]
states = ['S0', "S1", "S2", "S3", "S4"]
move = [['S0', 'a', 'S1'], ['S1', 'b', 'S1'], ['S2', 'b', 'S2'],
        ['S3', 'b', 'S3'], ['S1', None, 'S2'], ['S2', None, 'S3'], ['S3', 'b', 'S4']]
dfa1 = DFA(start, end, states, symbols, move)

start = "S0"
end = ['S3']
symbols = ["a", "b"]
states = ['S0', "S1", "S2", "S3"]
move = [['S0', 'a', 'S0'], ['S1', 'b', 'S1'], ['S2', 'b', 'S2'],
        ['S0', None, 'S1'], ['S1', None, 'S2'], ['S2', 'b', 'S3']]
dfa2 = DFA(start, end, states, symbols, move)

print(dfa1 == dfa2)
