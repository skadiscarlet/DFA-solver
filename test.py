start = "0"
end = ["9"]
symbols = ["a", "b"]
states = [str(i) for i in range(10)]
move = [
        ["0",None,"1"],
        ["0",None,"7"],
        ["1",None,"2"],
        ["1",None,"4"],
        ["2","a","3"],
        ["3",None,"6"],
        ["6", None, "1"],
        ["4","b","5"],
        ["5",None,"6"],
        ["6",None,"7"],
        ["7","a","8"],
        ["8","b","9"],
        ["9",None,"6"]
    ]
from dfa import DFA

dfa = DFA(start, end, states, symbols, move)
dfa.print()