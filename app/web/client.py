import requests
import logging
from requests.auth import HTTPBasicAuth
from app import settings
from app.settings import API_CONF as apiconf

log = logging.getLogger(__name__)


class Client:
    @staticmethod
    def getInstance():
        return Client(
            apiconf["host"], apiconf["port"], apiconf["username"], apiconf["password"]
        )

    def __init__(self, host, port, user, passwd):
        self._base_url = f"http://{host}:{port}/api/"
        self._headers = {"Accept": "application/json"}
        self._auth = HTTPBasicAuth(user, passwd)

    def get_challenges(self):
        url = f"nqueen/challenges"
        return self.call_service(url)

    def add_challenge(self, challenge_number):
        url = f"nqueen/challenges"
        payload = {"challenge_number": challenge_number}
        return self.call_service(url, "POST", payload)

    def get_solutions(self, challenge_number):
        url = f"nqueen/challenges/{challenge_number}/solutions"
        return self.call_service(url)

    def call_service(self, url, method="GET", payload=""):
        url_to_call = f"{self._base_url}{url}"
        log.debug(url_to_call)
        try:
            resp = requests.request(
                method=method,
                url=url_to_call,
                json=payload,
                auth=self._auth,
                verify=False,
                headers=self._headers,
            )
            if resp.status_code in [200, 201, 202, 204]:
                json_resp = resp.json()
                log.debug(json_resp)
                return json_resp
            else:
                log.error(resp.content)
                raise Exception("Error to process.")
        except Exception as e:
            log.error(e)
            raise e
