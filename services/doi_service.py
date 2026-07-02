import re
import requests

def clean_jats(text):
    return re.sub(r"<.*?>", "", text)
    
def get_metadata_from_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code != 200:
        return None

    data = r.json()["message"]
    print(data)
    title = data.get("title", [None])[0]
    abstract = data.get("abstract")  # often None

    return {
        "source": "Crossref",
        "title": title,
        "abstract": clean_jats(abstract)
    }


def get_metadata_from_datacite(doi):
    url = f"https://api.datacite.org/dois/{doi}"
    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code != 200:
        return None

    data = r.json()["data"]["attributes"]
    title = data.get("titles", [{}])[0].get("title")

    descriptions = data.get("descriptions", [])
    abstract = None
    for d in descriptions:
        if d.get("descriptionType") == "Abstract":
            abstract = d.get("description")
            break

    return {
        "source": "DataCite",
        "title": title,
        "abstract": clean_jats(abstract),
        "metadata": data
    }

def fetch_doi_metadata(doi: str):
    # Try Crossref first

    result = get_metadata_from_crossref(doi)
    if result:
        return result

    # Fallback to DataCite
    return get_metadata_from_datacite(doi)