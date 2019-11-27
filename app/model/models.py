from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from app.model import db


class Challenge(db.Model):
    __tablename__ = "challenge"
    challenge_number = Column(
        "challenge_number", Integer, nullable=False, primary_key=True
    )
    amount_of_solutions = Column("amount_of_solutions", Integer, default=1)
    finished = Column("finished", Boolean, default=False)

    def json(self):
        return {
            "challenge_number": self.challenge_number,
            "amount_of_solutions": self.amount_of_solutions,
            "finished": self.finished,
        }

    def __repr__(self):
        return f"<Challenge {self.challenge_number}, _finished:{self.finished}>"


class Solution(db.Model):
    __tablename__ = "solution"
    solution_id = Column("solution_id", Integer, primary_key=True, autoincrement=True)
    challenge_number = Column(
        "challenge_number", Integer, ForeignKey("challenge.challenge_number")
    )
    solution_array = db.Column("solution_array", Text)
    challenge = db.relationship(
        "Challenge",
        primaryjoin="Challenge.challenge_number == Solution.challenge_number",
        backref="challenge",
    )

    def json(self):
        return {
            "solution_id": self.solution_id,
            "challenge_number": self.challenge_number,
            "solution_array": self.solution_array,
        }

    def __repr__(self):
        return f"<Solution {self.solution_id} for {self.challenge_number}>"
