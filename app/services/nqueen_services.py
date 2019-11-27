import logging
import threading
from time import time
from random import randint as rand
from pyeda.inter import *

from app import app
from app.services.challenge_services import add_solution, update_challenge

# 1st: https://pyeda.readthedocs.io/en/latest/queens.html
# 2nd: https://towardsdatascience.com/genetic-algorithm-vs-backtracking-n-queen-problem-cdf38e15d73f
# 3rd: https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/
# 4th: https://www.geeksforgeeks.org/n-queen-problem-using-branch-and-bound/

log = logging.getLogger(__name__)


class QueenService_PyEAD:
    def __init__(self, n=8):
        log.info(f"QueenService.__init__(board_size={n})")
        self.board_size = n
        self.board = exprvars("x", self.board_size, self.board_size)

        R = And(
            *[
                OneHot(*[self.board[r, c] for c in range(self.board_size)])
                for r in range(self.board_size)
            ]
        )
        C = And(
            *[
                OneHot(*[self.board[r, c] for r in range(self.board_size)])
                for c in range(self.board_size)
            ]
        )

        starts = [(i, 0) for i in range(self.board_size - 2, 0, -1)] + [
            (0, i) for i in range(self.board_size - 1)
        ]
        lrdiags = []
        for r, c in starts:
            lrdiags.append([])
            ri, ci = r, c
            while ri < self.board_size and ci < self.board_size:
                lrdiags[-1].append((ri, ci))
                ri += 1
                ci += 1

        DLR = And(*[OneHot0(*[self.board[r, c] for r, c in diag]) for diag in lrdiags])

        starts = [
            (i, self.board_size - 1) for i in range(self.board_size - 2, -1, -1)
        ] + [(0, i) for i in range(self.board_size - 2, 0, -1)]
        rldiags = []
        for r, c in starts:
            rldiags.append([])
            ri, ci = r, c
            while ri < self.board_size and ci >= 0:
                rldiags[-1].append((ri, ci))
                ri += 1
                ci -= 1

        DRL = And(*[OneHot0(*[self.board[r, c] for r, c in diag]) for diag in rldiags])

        self.solution = R & C & DLR & DRL

    def get_all_possible_solutions_count(self):
        return self.solution.satisfy_count()

    def get_a_solution(self):
        log.info(f"QueenService.get_a_solution()")
        return self.solution.satisfy_one()

    def get_all_solutions(self):
        log.info(f"QueenService.get_all_solutions()")
        return list(self.solution.satisfy_all())

    def display(self, point):
        chars = list()
        for r in range(self.board_size):
            for c in range(self.board_size):
                if point[self.board[r, c]]:
                    chars.append("Q")
                else:
                    chars.append(".")
            if r != (self.board_size - 1):
                chars.append("\n")
        print("".join(chars))


class QueenService_Genetic:
    def __init__(self, n):
        self.board = self.createBoard(n)
        self.solutions = []
        self.size = n
        self.env = []
        self.goal = None
        self.goalIndex = -1

    def createBoard(self, n):
        board = [[0 for i in range(n)] for j in range(n)]
        return board

    def setBoard(self, board, gen):
        for i in range(self.size):
            board[gen[i]][i] = 1

    def genereteDNA(self):
        # genereates random list of length n
        from random import shuffle

        DNA = list(range(self.size))
        shuffle(DNA)
        while DNA in self.env:
            shuffle(DNA)
        return DNA

    def initializeFirstGenereation(self):
        for i in range(500):
            self.env.append(self.genereteDNA())

    def utilityFunction(self, gen):

        hits = 0
        board = self.createBoard(self.size)
        self.setBoard(board, gen)
        col = 0

        for dna in gen:
            try:
                for i in range(col - 1, -1, -1):
                    if board[dna][i] == 1:
                        hits += 1
            except IndexError:
                print(gen)
                quit()
            for i, j in zip(range(dna - 1, -1, -1), range(col - 1, -1, -1)):
                if board[i][j] == 1:
                    hits += 1
            for i, j in zip(range(dna + 1, self.size, 1), range(col - 1, -1, -1)):
                if board[i][j] == 1:
                    hits += 1
            col += 1
        return hits

    def isGoalGen(self, gen):
        if self.utilityFunction(gen) == 0:
            return True
        return False

    def crossOverGens(self, firstGen, secondGen):
        """Approach #1"""
        # bound = self.size // 2
        # for i in range(bound):
        #     firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
        """Approach #2"""
        # for i in range(1, len(firstGen)):
        #     if abs(firstGen[i - 1] - firstGen[i]) < 2:
        #         firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
        #     if abs(secondGen[i - 1] - secondGen[i]) < 2:
        #         firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
        """App1 + App2"""
        isSwapped = False
        for i in range(1, len(firstGen)):
            if abs(firstGen[i - 1] - firstGen[i]) < 2:
                isSwapped = True
                firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
            if abs(secondGen[i - 1] - secondGen[i]) < 2:
                isSwapped = True
                firstGen[i], secondGen[i] = secondGen[i], firstGen[i]
        if not isSwapped:
            bound = self.size // 2
            for i in range(bound):
                firstGen[i], secondGen[i] = secondGen[i], firstGen[i]

    def MutantGen(self, gen):
        """Approach #1"""
        # bound = self.size//2
        # from random import randint as rand
        # leftSideIndex = rand(0,bound)
        # RightSideIndex = rand(bound+1,self.size-1)
        # gen[leftSideIndex],gen[RightSideIndex] = gen[RightSideIndex],gen[leftSideIndex]
        # return gen
        """Approach #2"""
        # from random import randint as rand
        # newGen = []
        # for dna in gen:
        #     if dna not in newGen:
        #         newGen.append(dna)
        # for i in range(self.size):
        #     if i not in newGen:
        #         # newGen.insert(rand(0,len(gen)),i)
        #         newGen.append(i)
        # gen = newGen
        # return gen
        """Approach #3"""
        # from random import randint as rand
        # newGen = []
        # for dna in gen:
        #     if dna not in newGen:
        #         newGen.append(dna)
        # for i in range(self.size):
        #     if i not in newGen:
        #         inserted = False
        #         for j in range(len(newGen)):
        #             if abs(newGen[j] - i) >=2:
        #                 newGen.insert(j,i)
        #                 inserted = True
        #         if not inserted:
        #             newGen.append(i)
        # gen = []
        # for dna in newGen:
        #     if dna not in gen:
        #         gen.append(dna)

        # return gen
        """Approach #4"""
        bound = self.size // 2
        from random import randint as rand

        leftSideIndex = rand(0, bound)
        RightSideIndex = rand(bound + 1, self.size - 1)
        newGen = []
        for dna in gen:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.size):
            if i not in newGen:
                # newGen.insert(rand(0,len(gen)),i)
                newGen.append(i)

        gen = newGen
        gen[leftSideIndex], gen[RightSideIndex] = (
            gen[RightSideIndex],
            gen[leftSideIndex],
        )
        return gen

    def crossOverAndMutant(self):
        for i in range(1, len(self.env), 2):
            firstGen = self.env[i - 1][:]
            secondGen = self.env[i][:]
            self.crossOverGens(firstGen, secondGen)
            firstGen = self.MutantGen(firstGen)
            secondGen = self.MutantGen(secondGen)
            self.env.append(firstGen)
            self.env.append(secondGen)

    def makeSelection(self):
        # index problem
        genUtilities = []
        newEnv = []

        for gen in self.env:
            genUtilities.append(self.utilityFunction(gen))
        if min(genUtilities) == 0:
            self.goalIndex = genUtilities.index(min(genUtilities))
            self.goal = self.env[self.goalIndex]
            return self.env
        minUtil = None
        while len(newEnv) < self.size:
            minUtil = min(genUtilities)
            minIndex = genUtilities.index(minUtil)
            newEnv.append(self.env[minIndex])
            genUtilities.remove(minUtil)
            self.env.remove(self.env[minIndex])

        return newEnv

    def solveGA(self):
        self.initializeFirstGenereation()
        for gen in self.env:
            if self.isGoalGen(gen):
                return gen
        count = 0
        while True:
            self.crossOverAndMutant()
            self.env = self.makeSelection()
            count += 1
            if self.goalIndex >= 0:
                try:
                    print(count)
                    return self.goal
                except IndexError:
                    print(self.goalIndex)
            else:
                continue

    def reportGASolverTime(self):
        start = time()
        self.solveGA()
        end = time()
        print(str(end - start))


class QueenService_BackTracking:
    def __init__(self, n=8):
        self.n = n
        self.k = 0
        self.solutions = []
        self.first_solution = None

    def save(self, board):
        self.k += 1
        solution = self.reduce_board(board)
        if self.k == 1:
            self.first_solution = solution

        with app.app_context():
            add_solution(self.n, solution)
        self.solutions.append(solution)

    def reduce_board(self, board):
        resp = []
        for row in board:
            resp.append(self.get_position_in_row(row))
        return str(resp)[1:-1]

    def get_position_in_row(self, row):
        _pos = 1
        for pos in row:
            if pos and pos > 0:
                return _pos
            else:
                _pos += 1
        return 0

    def printSolution(self, solution):
        array = solution.split(",")
        for row in range(self.n):
            qpos = int(array[row]) - 1
            for col in range(self.n):
                if qpos == col:
                    print("Q", end="")
                else:
                    print(".", end="")
            print("\n")

    """ A utility function to check if a queen can  
    be placed on board[row][col]. Note that this  
    function is called when "col" queens are  
    already placed in columns from 0 to col -1.  
    So we need to check only left side for  
    attacking queens """

    def isSafe(self, board, row, col):

        # Check this row on left side
        for i in range(col):
            if board[row][i]:
                return False

        # Check upper diagonal on left side
        i = row
        j = col
        while i >= 0 and j >= 0:
            if board[i][j]:
                return False
            i -= 1
            j -= 1

        # Check lower diagonal on left side
        i = row
        j = col
        while j >= 0 and i < self.n:
            if board[i][j]:
                return False
            i = i + 1
            j = j - 1

        return True

    """ A recursive utility function to solve N  
    Queen problem """

    def solveNQUtil(self, board, col):

        """ base case: If all queens are placed  
        then return true """
        if col == self.n:
            self.save(board)
            return True

        """ Consider this column and try placing  
        this queen in all rows one by one """
        res = False
        for i in range(self.n):

            """ Check if queen can be placed on  
            board[i][col] """
            if self.isSafe(board, i, col):

                # Place this queen in board[i][col]
                board[i][col] = 1

                # Make result true if any placement
                # is possible
                res = self.solveNQUtil(board, col + 1) or res

                """ If placing queen in board[i][col]  
                doesn't lead to a solution, then  
                remove queen from board[i][col] """
                board[i][col] = 0  # BACKTRACK

        """ If queen can not be place in any row in  
            this column col then return false """
        return res

    """ This function solves the N Queen problem using  
    Backtracking. It mainly uses solveNQUtil() to  
    solve the problem. It returns false if queens  
    cannot be placed, otherwise return true and  
    prints placement of queens in the form of 1s.  
    Please note that there may be more than one  
    solutions, this function prints one of the  
    feasible solutions."""

    def solve(self):

        board = [[0 for j in range(self.n)] for i in range(self.n)]

        if self.solveNQUtil(board, 0) == False:
            print("Solution does not exist")
            return
        return


class QueenService_BranchBounce:
    """ Python3 program to solve N Queen Problem using Branch or Bound """

    def __init__(self, N=8):
        self.N = N

    """ A utility function to prsolution """

    def printSolution(self, board):
        for i in range(self.N):
            for j in range(self.N):
                print(board[i][j], end=" ")
            print()

    """ A Optimized function to check if  
    a queen can be placed on board[row][col] """

    def isSafe(
        self,
        row,
        col,
        slashCode,
        backslashCode,
        rowLookup,
        slashCodeLookup,
        backslashCodeLookup,
    ):
        if (
            slashCodeLookup[slashCode[row][col]]
            or backslashCodeLookup[backslashCode[row][col]]
            or rowLookup[row]
        ):
            return False
        return True

    """ A recursive utility function to solve N Queen problem """

    def solveNQueensUtil(
        self,
        board,
        col,
        slashCode,
        backslashCode,
        rowLookup,
        slashCodeLookup,
        backslashCodeLookup,
    ):

        """ base case: If all queens are placed then return True """
        if col >= self.N:
            return True
        for i in range(self.N):
            if self.isSafe(
                i,
                col,
                slashCode,
                backslashCode,
                rowLookup,
                slashCodeLookup,
                backslashCodeLookup,
            ):

                """ Place this queen in board[i][col] """
                board[i][col] = 1
                rowLookup[i] = True
                slashCodeLookup[slashCode[i][col]] = True
                backslashCodeLookup[backslashCode[i][col]] = True

                """ recur to place rest of the queens """
                if self.solveNQueensUtil(
                    board,
                    col + 1,
                    slashCode,
                    backslashCode,
                    rowLookup,
                    slashCodeLookup,
                    backslashCodeLookup,
                ):
                    return True

                """ If placing queen in board[i][col]  
                doesn't lead to a solution,then backtrack """

                """ Remove queen from board[i][col] """
                board[i][col] = 0
                rowLookup[i] = False
                slashCodeLookup[slashCode[i][col]] = False
                backslashCodeLookup[backslashCode[i][col]] = False

        """ If queen can not be place in any row in  
        this colum col then return False """
        return False

    """ This function solves the N Queen problem using  
    Branch or Bound. It mainly uses solveNQueensUtil()to  
    solve the problem. It returns False if queens  
    cannot be placed,otherwise return True or  
    prints placement of queens in the form of 1s.  
    Please note that there may be more than one  
    solutions,this function prints one of the  
    feasible solutions."""

    def solveNQueens(self):
        board = [[0 for i in range(self.N)] for j in range(self.N)]

        # helper matrices
        slashCode = [[0 for i in range(self.N)] for j in range(self.N)]
        backslashCode = [[0 for i in range(self.N)] for j in range(self.N)]

        # arrays to tell us which rows are occupied
        rowLookup = [False] * self.N

        # keep two arrays to tell us
        # which diagonals are occupied
        x = 2 * self.N - 1
        slashCodeLookup = [False] * x
        backslashCodeLookup = [False] * x

        # initialize helper matrices
        for rr in range(self.N):
            for cc in range(self.N):
                slashCode[rr][cc] = rr + cc
                backslashCode[rr][cc] = rr - cc + 7

        if (
            self.solveNQueensUtil(
                board,
                0,
                slashCode,
                backslashCode,
                rowLookup,
                slashCodeLookup,
                backslashCodeLookup,
            )
            == False
        ):
            print("Solution does not exist")
            return False

        # solution found
        return board


class QueenService(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.n = n
        self.first_solution = None
        self.queen_bt = QueenService_BackTracking(self.n)
        self.finnished = False

    def get_first_solution(self):
        self.first_solution = self.queen_bt.first_solution
        log.debug(f"First solution: {self.first_solution}")
        return self.first_solution

    def run(self):
        try:
            log.info(f"Starting solving! N={self.n}")
            self.queen_bt.solve()
            self.amount_of_solutions = len(self.queen_bt.solutions)
            log.info(
                f"N={self.n} solved! {self.amount_of_solutions} solutions founded!"
            )
            self.finnished = True
            with app.app_context():
                update_challenge(self.n, self.amount_of_solutions, True)

        except Exception as e:
            log.exception(e)
