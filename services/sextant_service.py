import re
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin


def extract_sextant_metadata(logger, url: str) -> dict:
    """
    Extract metadata from a Sextant / GeoNetwork record using the API.

    Required library:
        pip install requests

    Returns:
        {
            "url": str,
            "uuid": str,
            "doi": str | None,
            "title": str | None,
            "files_involved": list[dict],
            "keywords": list[str],
            "locations": dict | list,
            "license": str | None
        }
    """

    uuid_match = re.search(
        r"/records/([0-9a-fA-F-]{36})",
        url
    )

    if not uuid_match:
        raise ValueError("Could not extract the metadata UUID from the URL")

    uuid = uuid_match.group(1)

    base_url = "https://sextant.ifremer.fr/geonetwork"
    api_url = f"{base_url}/srv/api/records/{uuid}/formatters/xml"

    response = requests.get(
        api_url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)

    ns = {
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gco": "http://www.isotc211.org/2005/gco",
        "gmx": "http://www.isotc211.org/2005/gmx",
        "gml": "http://www.opengis.net/gml",
        "srv": "http://www.isotc211.org/2005/srv",
    }

    def text(path):
        element = root.find(path, ns)
        return element.text.strip() if element is not None and element.text else None

    def texts(path):
        return [
            e.text.strip()
            for e in root.findall(path, ns)
            if e.text and e.text.strip()
        ]

    # Title
    title = text(
        ".//gmd:identificationInfo/*/gmd:citation/"
        "gmd:CI_Citation/gmd:title/gco:CharacterString"
    )

    # DOI: search in identifiers and full XML text
    xml_text = response.text

    doi = None
    doi_match = re.search(
        r"10\.\d{4,9}/[-._;()/:A-Z0-9]+",
        xml_text,
        re.I
    )
    if doi_match:
        doi = doi_match.group(0)

    # Keywords
    keywords = texts(
        ".//gmd:descriptiveKeywords/gmd:MD_Keywords/"
        "gmd:keyword/gco:CharacterString"
    )

    keywords += texts(
        ".//gmd:descriptiveKeywords/gmd:MD_Keywords/"
        "gmd:keyword/gmx:Anchor"
    )

    keywords = sorted(set(keywords))

    # Geographic bounding box
    west = text(".//gmd:EX_GeographicBoundingBox/gmd:westBoundLongitude/gco:Decimal")
    east = text(".//gmd:EX_GeographicBoundingBox/gmd:eastBoundLongitude/gco:Decimal")
    south = text(".//gmd:EX_GeographicBoundingBox/gmd:southBoundLatitude/gco:Decimal")
    north = text(".//gmd:EX_GeographicBoundingBox/gmd:northBoundLatitude/gco:Decimal")

    locations = {}

    if all([west, east, south, north]):
        locations["bounding_box"] = {
            "west": float(west),
            "east": float(east),
            "south": float(south),
            "north": float(north),
        }

    place_names = texts(
        ".//gmd:extent/gmd:EX_Extent/gmd:description/gco:CharacterString"
    )

    if place_names:
        locations["place_names"] = place_names

    # License / use constraints
    license_values = texts(
        ".//gmd:resourceConstraints//gmd:useLimitation/gco:CharacterString"
    )

    license_values += texts(
        ".//gmd:resourceConstraints//gmd:otherConstraints/gco:CharacterString"
    )

    license_values += texts(
        ".//gmd:resourceConstraints//gmd:otherConstraints/gmx:Anchor"
    )

    license_info = license_values[0] if license_values else None

    # Online resources / files / services
    files = []

    for online in root.findall(".//gmd:CI_OnlineResource", ns):
        linkage = online.find(
            ".//gmd:linkage/gmd:URL",
            ns
        )
        name = online.find(
            ".//gmd:name/gco:CharacterString",
            ns
        )
        description = online.find(
            ".//gmd:description/gco:CharacterString",
            ns
        )
        protocol = online.find(
            ".//gmd:protocol/gco:CharacterString",
            ns
        )

        if linkage is not None and linkage.text:
            files.append({
                "name": name.text.strip() if name is not None and name.text else None,
                "description": description.text.strip() if description is not None and description.text else None,
                "protocol": protocol.text.strip() if protocol is not None and protocol.text else None,
                "url": urljoin(base_url, linkage.text.strip()),
            })

    # Remove duplicate URLs
    files = list({f["url"]: f for f in files}.values())

    return {
        "url": url,
        "uuid": uuid,
        "doi": doi,
        "title": title,
        "files_involved": files,
        "keywords": keywords,
        "locations": locations,
        "license": license_info,
    }
