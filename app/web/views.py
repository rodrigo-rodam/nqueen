import logging
from flask import Blueprint, render_template, request
from web.client import Client

log = logging.getLogger(__name__)

web = Blueprint("web_client", __name__)


@web.route("/", methods=["GET", "POST"])
def index():
    msg = None
    cli = Client.getInstance()
    challenge_number = request.form.get("challenge_number")
    if challenge_number:
        try:
            n = int(challenge_number)
            cli.add_challenge(n)
            msg = "Challenge accepted!"

        except Exception as e:
            log.error(e)
            msg = "Challenge not accepted! Sorry."
    else:
        msg = "Please insert a number (integer) to create a challenge."

    challenges = cli.get_challenges()
    return render_template("index.html", challenges=challenges, msg=msg)


@web.route("/solutions", methods=["GET"])
def solutions():
    cli = Client.getInstance()
    challenge_number = request.args.get("challenge_number")
    solutions = []
    if challenge_number:
        try:
            n = int(challenge_number)
            solutions = cli.get_solutions(n)

        except Exception as e:
            log.error(e)

    return render_template(
        "solutions.html", solutions=solutions, challenge_number=challenge_number
    )


@web.route("/board", methods=["GET"])
def board():
    challenge_number = int(request.args.get("challenge_number"))
    solution = request.args.get("solution")
    return render_template(
        "board.html", challenge_number=challenge_number, solution=solution
    )
