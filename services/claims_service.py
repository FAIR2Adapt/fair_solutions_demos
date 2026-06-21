import requests
import json
import config

def get_claims(data):

    headers = {
        "Content-Type": "text/plain"
    }

    response = requests.post(config.CLAIMS_ENDPOINT, headers=headers, data=data)

    print(data)
    print(response.text)

    return response.status_code, response.text

def fetch_claims_from_abstract(abstract: str) -> list[dict]:
    code, claims_text = get_claims(abstract)
    return json.loads(claims_text)
