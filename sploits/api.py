import requests


class Api:
    def __init__(self):
        self.timeout = 4

    def add_unit_to_chess(self, host, first_unit_name, second_unit_name):
        request = [first_unit_name, second_unit_name]
        result = requests.put(
            f"http://{host}:8284/add_inner_unit_to_chess_unit",
            json=request, timeout=self.timeout
        )
        return result.json()["name"]

    def object_info(self, host, unit_name):
        request = [unit_name]
        result = requests.get(
            f"http://{host}:8284/info",
            json=request,
            timeout=self.timeout
        )
        return result.json()["info"]

    def get_latest_objects(self, host, amount: int):
        index = int(requests.get(f"http://{host}:8284/latest_index").json()["last"])
        amount = int(amount)
        request = requests.get(
            f"http://{host}:8284/objects",
            json=[max(index-amount, 0), index],
            timeout=self.timeout
        )
        return request.json()["objects"]
