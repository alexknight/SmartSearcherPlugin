import json

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Keep track of search queries. Does not persist if Python session is restarted.
_SEARCHES = {}

@app.post("/searches/<string:username>")
async def add_search(username):
    request_data = await quart.request.get_json(force=True)
    if username not in _SEARCHES:
        _SEARCHES[username] = []
    _SEARCHES[username].append(request_data["query"])
    return quart.Response(response='OK', status=200)

@app.get("/searches/<string:username>")
async def get_searches(username):
    return quart.Response(response=json.dumps(_SEARCHES.get(username, [])), status=200)

@app.delete("/searches/<string:username>")
async def delete_search(username):
    request_data = await quart.request.get_json(force=True)
    search_idx = request_data["search_idx"]
    # fail silently, it's a simple plugin
    if 0 <= search_idx < len(_SEARCHES[username]):
        _SEARCHES[username].pop(search_idx)
    return quart.Response(response='OK', status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5003)


if __name__ == "__main__":
    main()
