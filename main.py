import requests
import json

vercel_base_url = "https://py-smart-search-backend-57s9.vercel.app"


class SmartSearcherPlugin:
    def __init__(self):
        self.vercel_base_url = vercel_base_url

    def post_request_to_vercel(self, query):
        payload = json.dumps({"query": query})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.vercel_base_url}/api/search", data=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch data"}

    def search(self, query):
        response = self.post_request_to_vercel(query)
        if "error" not in response:
            return response.get("matched_data", "No matched data found.")
        else:
            return response["error"]

    def handle_event(self, event):
        query = event.get("query")
        if query:
            return self.search(query)
        else:
            return {"error": "No query provided"}






# Example usage
if __name__ == "__main__":
    plugin = SmartSearcherPlugin()
    event = {"query": "example query"}
    result = plugin.handle_event(event)
    print(result)
