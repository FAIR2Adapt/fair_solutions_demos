import streamlit as st

from services.doi_service import fetch_doi_metadata
from utils.fair_publication_state import split_abstract


def render_step_3_doi(logger) -> None:
    st.subheader("Step 3 — Enter the DOI")

    st.text_input(
        "DOI",
        placeholder="e.g. 10.5281/zenodo.1234567",
        key="doi_value",
    )

    if st.button("Process DOI", use_container_width=True):
        doi = st.session_state.get("doi_value", "").strip()

        if not doi:
            logger.warning("Empty DOI submitted")
            st.warning("Please enter a DOI.")
            return

        logger.info("Processing DOI: %s", doi)

        with st.spinner("Retrieving metadata..."):
            try:
                result = fetch_doi_metadata(doi)
                st.session_state["doi_result"] = result
                st.session_state.pop("claims_result", None)
                logger.info("DOI metadata retrieved successfully")
            except Exception as exc:
                logger.exception("DOI processing failed")
                st.session_state["doi_result"] = {"error": str(exc)}

    doi_result = st.session_state.get("doi_result")

    if not doi_result:
        return

    if "error" in doi_result:
        st.error(doi_result["error"])
        return

    st.success(f"Metadata retrieved from {doi_result['source']}")

    st.subheader("Title")
    st.write(doi_result.get("title", "No title found"))

    st.subheader("Abstract")
    abstract = doi_result.get("abstract")

    if abstract:
        preview, remainder = split_abstract(abstract, max_chars=300)
        st.write(preview)

        if remainder:
            with st.expander("Show remaining abstract"):
                st.write(remainder)
    else:
        st.info("No abstract available.")