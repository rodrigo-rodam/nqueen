import logging, cProfile, time
from logging.handlers import RotatingFileHandler
from app import settings
from app.services.nqueen_services import QueenService_PyEAD
from app.services.nqueen_services import QueenService_Genetic
from app.services.nqueen_services import QueenService_BranchBounce
from app.services.nqueen_services import QueenService_BackTracking
from app.services.nqueen_services import QueenServiceUtils

n = 9


def test_pyead():
    start_time = time.time()
    queen_services = QueenService_PyEAD(n)
    print(queen_services.get_a_solution())
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get a solution by PyEAD.")


def test_pyead_solutions_count():
    start_time = time.time()
    queen_services = QueenService_PyEAD(n)
    print(queen_services.get_all_possible_solutions_count())
    print(f"SOLUTIONS FOUND: {x}")
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get all solutions by PYEAD.")


def test_genetic():
    start_time = time.time()
    gn = QueenService_Genetic(n)
    print(gn.solveGA())
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get a solution by genetic.")


def test_backtracking():
    start_time = time.time()
    bt = QueenService_BackTracking(n)
    bt.solveBackTracking(0)
    print(QueenServiceUtils().hold_BackTracking_solution(bt.solutions[0]))
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get a solution by backtracking.")


def test_backtracking_solutions_count():
    start_time = time.time()
    bt = QueenService_BackTracking(n)
    bt.solve()
    print(bt.first_soltuion)
    print(len(bt.solutions))
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get a solution by backtracking.")


def test_branch_bounce():
    start_time = time.time()
    bb = QueenService_BranchBounce(n)
    print(bb.solveNQueens())
    elapsed_time = time.time() - start_time
    print(f"{elapsed_time} to get a solution by branch_bounce.")


if __name__ == "__main__":
    # test_pyead()
    # test_genetic()
    # test_backtracking()
    test_backtracking_solutions_count()
    # test_branch_bounce()

