import logging
from sqlalchemy.orm.exc import NoResultFound
from app.model import db
from app.model.models import Challenge, Solution

log = logging.getLogger(__name__)


def get_challenge(challenge_number):
    log.debug(f"get_challenge({challenge_number})")
    return Challenge.query.filter(
        Challenge.challenge_number == challenge_number
    ).first()


def list_challenges():
    log.debug("list_challenges()")
    return Challenge.query.all()


def update_challenge(challenge_number, amount_of_solutions, finished):
    challenge = get_challenge(challenge_number)
    if challenge:
        challenge.amount_of_solutions = amount_of_solutions
        challenge.finished = finished
        db.session.add(challenge)
        db.session.commit()
    else:
        return None


def list_solutions_by_challenge(challenge):
    log.debug(f"list_solutions_by_challange({challenge})")
    return (
        db.session.query(Solution)
        .filter(Solution.challenge_number == challenge.challenge_number)
        .all()
    )


def get_solution_by_challenge(challenge):
    log.debug(f"list_solution_by_challange({challenge})")
    try:
        Solution.query.filter(
            Solution.challenge_number == challenge.challenge_number
        ).first()

    except NoResultFound:
        solution = None


def get_solution_by_array(solution_array):
    log.debug(f"get_solution_by_array({solution_array})")
    try:
        solution = (
            db.session.query(Solution)
            .filter(Solution.solution_array == solution_array)
            .one()
        )
        return solution
    except NoResultFound:
        return None


def add_challenge(challenge_number, amount_of_solutions=0, finished=False):
    log.debug(
        f"add_challenge(challenge_number:{challenge_number}, amount_of_solutions:{amount_of_solutions})"
    )
    try:
        to = get_challenge(challenge_number)
        if to:
            return to
        to = Challenge()
        to.challenge_number = challenge_number
        to.amount_of_solutions = amount_of_solutions
        to.finished = finished
        db.session.add(to)
        db.session.commit()
        db.session.refresh(to)
        return to
    except Exception as e:
        log.exception(e)
        return {"ERROR": str(e)}


def add_solution(challenge_number, solution_array):
    log.debug(
        f"add_solution(challenge_number:{challenge_number}, solution_array:{solution_array})"
    )
    try:
        to = get_solution_by_array(solution_array)
        if to:
            return to
        else:
            to = Solution(
                challenge_number=challenge_number, solution_array=solution_array
            )
            db.session.add(to)
            db.session.commit()
            db.session.refresh(to)
            return to

    except Exception as e:
        log.exception(e)
        return {"ERROR": str(e)}
