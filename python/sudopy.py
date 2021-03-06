from copy import deepcopy
from time import sleep


class InvalidMove(Exception):
    '''Invalid move in sudoku'''


def next_rc(row, col):
    col += 1
    if col >= 9:
        col -= 9
        row += 1
    return row, col


def _solve_puzzle(puzzle, row, col):
    '''
    Solves a sudoku puzzle recursively by backtracking method.
    '''
    puzzle = deepcopy(puzzle)

    if row == 9 or col == 9:
        return puzzle

    # space is not blank; skip
    if puzzle[row,col] != 0:
        return _solve_puzzle(puzzle, *next_rc(row, col))

    for i in range(9):
        try:
            puzzle[row,col] = i+1
        except InvalidMove:
            continue

        if row == 8 and col == 8:
            return puzzle

        if p := _solve_puzzle(puzzle, *next_rc(row, col)):
            return p

    return False


class Puzzle:
    '''
    Sudoku puzzle object. Contains data for each of the 81 squares on a sudoku
    grid and has methods to check if the grid is solved (`Puzzle.complete()`)
    and to solve the puzzle (`Puzzle.solve()`).

    Constructor takes one parameter: a list of lists of integers in row-major
    form or a sort of matrix or table. A zero value in this table represents an
    empty space in the grid, 1-9 are answers in the grid. Any other value is
    invalid. This is all checked in `__init__`.
    '''

    def __init__(self, data):
        # data should be a 9x9 list of lists of int
        assert isinstance(data, list)
        assert len(data) == 9
        for r in data:
            assert isinstance(r, list)
            assert len(r) == 9
            for i in r:
                assert isinstance(i, int)
                assert 0 <= i <= 9

        self.data = data


    def complete(self):
        '''
        Checks if the puzzle is solved by seeing if all columns sum to 45 and
        all rows sum to 45.
        '''
        columnwise_sums = [0 for i in range(9)]
        rowwise_sums = [0 for i in range(9)]
        for i in range(9):
            for j in range(9):
                c = self[i,j]
                rowwise_sums[i] += c
                columnwise_sums[j] += c
        return all([s == 45 for s in columnwise_sums]) and all([s == 45 for s in rowwise_sums])


    def solve(self):
        '''
        Light wrapper that calls the backend `_solve_puzzle(...)` function on
        this object. This recursive function returns the solved version of the
        sudoku grid.
        '''
        solution = _solve_puzzle(self, 0, 0)
        self.data = solution.data


    def __str__(self):
        strdata = [[str(c) if c > 0 else '-' for c in row] for row in self.data]
        for i, row in enumerate(strdata):
            strdata[i].insert(6, '│')
            strdata[i].insert(3, '│')
        
        lines = [' '.join(row) for row in strdata]
        bar = ['─']*len(lines[0])
        bar[6] = '┼'
        bar[14] = '┼'
        bar=''.join(bar)
        lines.insert(6, bar)
        lines.insert(3, bar)

        return '\n'.join(lines)


    def __getitem__(self, coord):
        assert isinstance(coord, tuple)
        assert len(coord) == 2
        row, col = coord
        return self.data[row][col]


    def check_valid_move(self, row, col, v):

        for i in range(9):
            if self[i, col] == v:
                return False
            if self[row, i] == v:
                return False

        sq_row, sq_col = int((row)//3)*3, int((col)//3)*3
        for i in range(sq_row, sq_row+3):
            for j in range(sq_col, sq_col+3):
                if self[i,j] == v:
                    return False

        return True


    def __setitem__(self, coord, value):
        assert isinstance(coord, tuple)
        assert len(coord) == 2
        assert isinstance(value, int)

        row, col = coord
        if not self.check_valid_move(row, col, value):
            raise InvalidMove()

        self.data[row][col] = value