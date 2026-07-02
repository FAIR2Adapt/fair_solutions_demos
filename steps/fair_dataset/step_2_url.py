import streamlit as st
from services.seanoe_service import extract_seanoe_metadata
from services.seanoe_service import extract_seanoe_metadata_scrapping
from services.sextant_service import extract_sextant_metadata
from services.doi_service import fetch_doi_metadata
from utils.fair_publication_state import split_abstract

def render_step_url(logger) -> None:
    st.subheader("Step: Enter a URL from one of the databases")

    st.text_input(
        "URL",
        placeholder="e.g. https://www.seanoe.org/data/01068/118008/",
        key="url_value",
    )

    if st.button("Process URL", use_container_width=True):
        url = st.session_state.get("url_value", "").strip()
        st.session_state["url"] = url

        logger.info("Processing URL: %s", url)

        with st.spinner("Retrieving metadata..."):
            try:
                if "seanoe" in url:
                    result = extract_seanoe_metadata_scrapping(logger, url)
                elif "sextant" in url:
                    result = extract_sextant_metadata(logger, url)

                logger.info("Metadata webscrapping")
                logger.info(result)
                result_doi = fetch_doi_metadata(result["doi"])

                logger.info("DOI result")
                logger.info(result_doi)

                result["title"] = result_doi["title"]
                result["abstract"] = result_doi["abstract"]

                metadata = result_doi.get("metadata", {})

                creators = metadata.get("creators", [])

                result["creators"] = creators

                authors = ", ".join(
                    creator.get("name", "").replace(",", "")
                    for creator in creators
                )

                year = metadata.get("publicationYear", "")
                title = result_doi.get("title", "")
                publisher = metadata.get("publisher", "")
                doi = metadata.get("doi", result.get("doi", ""))

                result["citation_text"] = (
                    f"{authors} ({year}). "
                    f"{title}. "
                    f"{publisher}. "
                    f"https://doi.org/{doi}."
                )

                logger.info("Creators")
                logger.info(result["creators"])

                if "sextant" in url:
                    result["title"] = result_doi["title"]
                    url_value = f"https://doi.org/{result["doi"]}"
                    result["files_involved"].append({"name":result["title"],"url":url_value})
                st.session_state["doi_result"] = result
                st.session_state.pop("claims_result", None)
                logger.info("URL metadata retrieved successfully")
                logger.info(result)
            except Exception as exc:
                    logger.exception("DOI processing failed")
                    st.session_state["doi_result"] = {"error": str(exc)}

    url_result = st.session_state.get("doi_result")

    if not url_result:
        return

    if "error" in url_result:
        st.error("Problem to retrive metadata from DOI")
        return

    st.success(f"Metadata retrieved from {url_result['url']}")

    st.subheader("Title")
    st.write(url_result.get("title", "No title found"))

    st.subheader("Abstract")
    abstract = url_result.get("abstract")

    if abstract:
        preview, remainder = split_abstract(abstract, max_chars=300)
        st.write(preview)

        if remainder:
            with st.expander("Show remaining abstract"):
                st.write(remainder)
    else:
        st.info("No abstract available.")