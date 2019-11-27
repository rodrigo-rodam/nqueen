import requests
from requests.auth import HTTPBasicAuth
import pprint
from app import settings


port = settings.HOST_PORT
base_url = f"http://localhost:{port}/api"
_headers = {"Accept": "application/json"}
_auth = HTTPBasicAuth(settings.SEC_USER, settings.SEC_AP)

challenges_url = f"{base_url}/nqueen/challenges"


def test_post_challenges():
    resp = requests.request(
        method="POST", url=challenges_url, auth=_auth, verify=False, headers=_headers
    )
    challenges = resp.json()


def test_get_challenges(propagate=False):
    resp = requests.request(
        method="GET", url=challenges_url, auth=_auth, verify=False, headers=_headers
    )
    total = len(resp.json())
    print(f"Challenges returned: {total}")
    if propagate:
        challenges = resp.json()
        for challenge in challenges:
            challenge_number = challenge.get("challenge_number")
            amount_of_solutions = challenge.get("amount_of_solutions")
            print(
                f"Challenge  number: {challenge_number}, amount_of_solutions: {amount_of_solutions}"
            )
            test_get_challenge(challenge_number)


def test_get_challenge(challenge_number):
    challenge_url = f"{challenges_url}/{challenge_number}/solutions"
    resp = requests.request(
        method="GET", url=challenge_url, auth=_auth, verify=False, headers=_headers
    )
    solutions = len(resp.json())
    print(f"{solutions} returned for challenge {challenge_number}")


if __name__ == "__main__":
    test_post_challenge()
    test_get_challenges(True)
