from sanic import Sanic, request
from sanic.response import json, empty, html
import scenarios
from Helpers.validators import validate_requests, validate_units


app = Sanic(name=__name__)
app.config.REQUEST_MAX_SIZE = 1000000
app.config.REQUEST_TIMEOUT = 60 * 5

with open("main.html") as file:
    data = file.read()


@app.route("/")
async def main(req):
    return html(data, 200)


@app.post("/add_new_unit")
async def add_new_unit(req: request.Request):
    try:
        received = req.json
        if isinstance(received, dict) \
                and all(map(lambda x: isinstance(x, list), received.values()))\
                and validate_units(received):
            unit_id_response = scenarios.add_new_unit(received)
            return json({"unit_response": unit_id_response})
        return empty(400)
    except LookupError:
        return empty(409)
    except:
        return empty(400)


@app.put("/add_inner_unit_to_chess_unit")
async def add_unit_to_chess(req: request.Request):
    try:
        received = req.json
        if isinstance(received, list) and len(received) == 2 and validate_requests(received):
            resulting_name = scenarios.add_inner_unit_to_chess_unit(*received)
            return json({"name": resulting_name})
        return empty(400)
    except:
        return empty(400)


@app.get("/info")
async def get_object_info(req):
    try:
        received = req.json
        if isinstance(received, list) and len(received) == 1 and validate_requests(received):
            object_info = scenarios.print_object_info(received[0])
            return json({"info": object_info})
        return empty(400)
    except:
        return empty(400)


@app.get("/basement_info")
async def get_basement_info(req):
    try:
        received = req.json
        if isinstance(received, list) and len(received) == 2 and validate_requests(received):
            basement_info = scenarios.get_basement_info(*received)
            return json({"basement_info": basement_info})
        return empty(400)
    except:
        return empty(400)


@app.get("/objects")
async def get_objects_by_window(req):
    try:
        received = req.json
        if isinstance(received, list) \
                and len(received) == 2 \
                and all(map(lambda x: isinstance(x, int), received)):
            objects_in_window = scenarios.get_window_of_objects(received[0], received[1])
            return json({"objects": objects_in_window})
        return empty(400)
    except:
        return empty(400)


@app.get("/latest_index")
async def get_latest_index(_):
    try:
        return json({"last": scenarios.get_last_index()})
    except:
        return empty(500)


@app.listener('after_server_stop')
async def save_db_on_stop(_, __):
    scenarios.save_final_version_of_db()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8284,
        access_log=True
    )