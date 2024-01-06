import numpy as np

path = "test/board_configurations/"

def load_board(id):
    return np.loadtxt(path + f'board{id}.txt')

def parametrized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

@parametrized
def theory(test, theories):
    def aux(*args):
        [test(*args, *theory) for theory in theories]
    return aux
