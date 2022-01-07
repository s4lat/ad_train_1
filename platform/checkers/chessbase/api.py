import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def retryable_requests(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(400, 409, 500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class Api:
    def __init__(self):
        self.timeout = 4

    def add_new_chess_unit(self, host, unit_name, flag_id) -> str:
        request = {"ChessUnit": [unit_name, flag_id]}
        result = retryable_requests().post(
            f"http://{host}/add_new_unit",
            json=request, timeout=self.timeout
        )
        return result.json()["unit_response"]

    def add_armory_unit(self, host, unit_name):
        request = {"Armory": [unit_name, "axes", "helmets"]} # should be randomized
        result = retryable_requests().post(
            f"http://{host}/add_new_unit",
            json=request, timeout=self.timeout
        )
        return result.json()["unit_response"]

    def add_unit_to_chess(self, host, first_unit_name, second_unit_name):
        request = [first_unit_name, second_unit_name]
        result = retryable_requests().put(
            f"http://{host}/add_inner_unit_to_chess_unit",
            json=request, timeout=self.timeout
        )
        return result.json()["name"]

    def object_info(self, host, unit_name):
        request = [unit_name]
        result = retryable_requests().get(
            f"http://{host}/info",
            json=request,
            timeout=self.timeout
        )
        return result.json()["info"]

    def basement_info(self, host, unit_id, secret_to_access):
        request = [unit_id, secret_to_access]
        result = retryable_requests().get(
            f"http://{host}/basement_info",
            json=request,
            timeout=self.timeout
        )
        return result.json()["basement_info"]

    def get_latest_objects(self, host, amount: int):
        index = int(retryable_requests().get(f"http://{host}/latest_index").json()["last"])
        amount = int(amount)
        request = retryable_requests().get(
            f"http://{host}/objects",
            json=[max(index-amount, 0), index],
            timeout=self.timeout
        )
        return request.json()["objects"]