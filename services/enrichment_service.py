import requests
import config


def enrich_with_pdf(logger, pdf_file) -> dict:
    """
    Send an uploaded PDF file to the enrichment service.

    Args:
        logger: logger instance
        pdf_file: Streamlit uploaded file object
        service_url: endpoint URL

    Returns:
        Parsed JSON response if possible, otherwise a dict with raw text.
    """
    if pdf_file is None:
        raise ValueError("No PDF file provided")

    logger.info("Sending PDF to enrichment service: %s", pdf_file.name)

    files = {
        "file": (pdf_file.name, pdf_file.getvalue(), "application/pdf")
    }

    response = requests.post(
        config.ENRICHMENT_ENDPOINT,
        files=files,
        timeout=120,
    )

    logger.info("Enrichment service response status: %s", response.status_code)

    response.raise_for_status()

    try:
        return response.json()
    except ValueError:
        return {
            "raw_response": response.text
        }