import re
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_seanoe_metadata(logger, url: str) -> dict:
    record_id = re.search(r"/data/\d+/(\d+)/?", url).group(1)
    logger.info("Record ID:"+str(record_id))

    endpoints = [
        "http://www.seanoe.org/oai/OAIHandler"
    ]

    identifiers = [
        f"oai:seanoe.org:{record_id}",
        f"oai:www.seanoe.org:{record_id}",
        record_id,
    ]

    last_error = None

    for endpoint in endpoints:
        for identifier in identifiers:
            response = requests.get(
                endpoint,
                params={
                    "verb": "GetRecord",
                    "metadataPrefix": "oai_dc",
                    "identifier": identifier,
                },
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
            )

            if response.status_code >= 400:
                last_error = (
                    response.status_code,
                    response.url,
                    response.text[:500],
                )
                continue
            root = ET.fromstring(response.content)

            # OAI-PMH error returned as XML
            if root.find(".//{http://www.openarchives.org/OAI/2.0/}error") is not None:
                last_error = response.text[:500]
                continue

            ns = {"dc": "http://purl.org/dc/elements/1.1/"}

            def values(tag):
                return [
                    e.text.strip()
                    for e in root.findall(f".//dc:{tag}", ns)
                    if e.text and e.text.strip()
                ]

            rights = values("rights")

            return {
                "title": values("title")[0] if values("title") else None,
                "files_involved": values("identifier"),
                "keywords": values("subject"),
                "locations": values("coverage") + values("source"),
                "license": rights[0] if rights else None,
                "oai_identifier": identifier,
                "oai_endpoint": endpoint,
            }

    raise RuntimeError(f"Could not retrieve OAI-PMH record. Last error: {last_error}")

def extract_seanoe_metadata_scrapping(logger, url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n", strip=True)

    def clean(value):
        return re.sub(r"\s+", " ", value).strip() if value else None

    def find_after_label(labels):
        for label in labels:
            pattern = rf"{label}\s*[:\n]\s*(.+?)(?=\n[A-Z][A-Za-z /-]{{2,}}[:\n]|\n\n|$)"
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return clean(match.group(1))
        return None

    # Title
    title = None
    h1 = soup.find("h1")
    if h1:
        title = clean(h1.get_text(" ", strip=True))

    if not title and soup.title:
        title = clean(soup.title.get_text(" ", strip=True))

    doi = None

    # Method 1: citation_doi meta tag
    meta = soup.find("meta", attrs={"name": "citation_doi"})
    if meta and meta.get("content"):
        doi = meta["content"].strip()

    # Method 2: DC.identifier
    if doi is None:
        meta = soup.find("meta", attrs={"name": "DC.identifier"})
        if meta and meta.get("content"):
            m = re.search(r"10\.\d{4,9}/\S+", meta["content"])
            if m:
                doi = m.group(0)

    # Method 3: Search the whole page (fallback)
    if doi is None:
        m = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
        if m:
            doi = m.group(0)

    # Method 1: citation_doi meta tag
    meta = soup.find("meta", attrs={"name": "citation_doi"})
    if meta and meta.get("content"):
        doi = meta["content"].strip()

    # Keywords
    keywords_text = find_after_label(["Keywords", "Key words", "Mots-clés"])
    keywords = []
    if keywords_text:
        keywords = [
            clean(k)
            for k in re.split(r",|;", keywords_text)
            if clean(k)
        ]

    # Locations
    locations_text = find_after_label([
        "Location",
        "Locations",
        "Geographical area",
        "Geographic area",
        "Spatial coverage",
        "Coverage"
    ])

    locations = []
    if locations_text:
        locations = [
            clean(x)
            for x in re.split(r",|;", locations_text)
            if clean(x)
        ]

    # License
    license_info = None
    for a in soup.find_all("a", href=True):
        href = a["href"]
        label = clean(a.get_text(" ", strip=True))

        if "creativecommons.org/licenses" in href.lower():
            license_info = {
                "label": label,
                "url": href
            }
            break

    if not license_info:
        license_text = find_after_label(["License", "Licence", "Rights"])
        license_info = license_text

    # Files
    
    files = []

    table = soup.find("table", id="data-table")

    if table:
        tbody = table.find("tbody") or table

        for row in tbody.find_all("tr"):
            cells = row.find_all("td")
            if not cells:
                continue

            # First column = FILE
            name = clean(cells[0].get_text(" ", strip=True))

            # Download link
            link = row.find("a", href=True)
            if not link:
                continue

            href = urljoin(url, link["href"])

            files.append({
                "name": name,
                "url": href
            })

    # Remove duplicate files
    files = list({f["url"]: f for f in files}.values())
    return {
        "url": url,
        "doi": doi,
        "title": title,
        "files_involved": files,
        "keywords": keywords,
        "locations": locations,
        "license": license_info
    }