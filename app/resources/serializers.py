from flask_restplus import fields

from app.restplus import api


add_challenge_serializer = api.model(
    "Add_challenge",
    {
        "challenge_number": fields.Integer(
            required=True, description="Number of the challenge"
        )
    },
)
add_solution_serializer = api.model(
    "Add_solution",
    {
        "challenge_number": fields.Integer(
            required=True, description="Number of the challenge"
        ),
        "solution_array": fields.Integer(required=True, description="Solution array"),
    },
)

challenge_model_serializer = api.model(
    "Challenge_model",
    {
        "challenge_number": fields.Integer(
            required=True, description="Number of the challenge"
        ),
        "amount_of_solutions": fields.Integer(
            required=True, description="amount of solutions found"
        ),
        "finished": fields.Boolean(
            required=True, description="Are all the possible solutions found"
        ),
    },
)

solution_model_serializer = api.model(
    "Solution_model",
    {
        "challenge_number": fields.Integer(
            required=True, description="Number of the challenge"
        ),
        "solution_id": fields.Integer(required=True, description="Id of solution"),
        "solution_array": fields.String(
            required=True,
            description="Solution of the challenge as array. Each number is the position (column) of the Queen, each position in array is the row.",
        ),
    },
)

list_of_challenges_serializer = api.inherit("Challenges", challenge_model_serializer,)
list_of_solutions_serializer = api.inherit("Solutions", solution_model_serializer,)
