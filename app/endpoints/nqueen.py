import logging
from flask import request
from flask import jsonify
from flask_restplus import Resource
from app.restplus import api
from app.restplus import auth
from app.services.nqueen_services import QueenService
from app.services.challenge_services import add_challenge
from app.services.challenge_services import get_challenge
from app.services.challenge_services import add_solution
from app.services.challenge_services import list_challenges
from app.services.challenge_services import list_solutions_by_challenge
from app.services.challenge_services import get_solution_by_challenge
from app.resources.serializers import solution_model_serializer
from app.resources.serializers import challenge_model_serializer
from app.resources.serializers import add_challenge_serializer
from app.resources.serializers import list_of_challenges_serializer
from app.resources.serializers import list_of_solutions_serializer

log = logging.getLogger(__name__)

ns = api.namespace("nqueen", description="API to solve N-Queens Challenge")


@ns.route("/challenges", doc={"description": "List all challenges solved"})
class ListChallenges(Resource):
    @auth.login_required
    @api.marshal_with(list_of_challenges_serializer)
    def get(self):
        return list_challenges()

    @auth.login_required
    @api.expect(add_challenge_serializer)
    @api.marshal_with(challenge_model_serializer)
    def post(self):
        data = request.json
        challenge_number = int(data.get("challenge_number"))
        challenge = get_challenge(challenge_number)
        if challenge:
            if not challenge.finished:
                start(challenge_number)
        else:
            challenge = add_challenge(challenge_number)
            start(challenge_number)
        return challenge


@ns.route(
    "/challenges/<int:challenge_number>/solutions",
    doc={"description": "Get the solutions from a specific challenge"},
)
class Challenges(Resource):
    @auth.login_required
    @api.marshal_with(list_of_solutions_serializer)
    def get(self, challenge_number):
        challenge = get_challenge(challenge_number)
        if challenge:
            solutions = list_solutions_by_challenge(challenge)
            if solutions:
                return solutions

        return None, 404


def start(challenge_number):
    nqueen_services = QueenService(challenge_number)
    nqueen_services.start()
