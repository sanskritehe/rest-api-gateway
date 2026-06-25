import requests

def fetch_appointment(id: int):
    query = """
    query getAppointment($id: Int!) {
        appointment(id: $id) {
            id
            user
            time
            status
        }
    }
    """
    response = requests.post("http://database-service/graphql", json={'query': query, 'variables': {'id': id}})
    response_data = response.json()
    return response_data.get("data", {}).get("appointment", None)
