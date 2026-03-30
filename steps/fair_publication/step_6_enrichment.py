import streamlit as st
from services.enrichment_service import enrich_with_pdf

def render_step_6(logger) -> None:
    st.subheader("Step 6 — Enrichment service")

    st.write("Do you want to analyze the document to enrich the FDO?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Yes", use_container_width=True):
            st.success("User selected YES")
            st.session_state["upload_file"]="yes"
            
            # add your logic here

    with col2:
        if st.button("❌ No", use_container_width=True):
            st.info("User selected NO")
            st.session_state["upload_file"]="no"
            # add alternative logic here

    upload_file = st.session_state.get("upload_file")

    if upload_file == "yes":
        st.info("I can't find a PDF file to analyze. Could you upload the PDF of the publication?")
        pdf_file = st.file_uploader(
            "Upload the PDF file",
            type=["pdf"],
            key="pdf_file",
        )

        if pdf_file is not None:
            st.success(f"PDF uploaded: {pdf_file.name}")

            if st.button("Analyze PDF", use_container_width=True):
                with st.spinner("Sending PDF to enrichment service..."):
                    try:
                        result = enrich_with_pdf(
                            logger=logger,
                            pdf_file=pdf_file
                        )

                        st.session_state["enrichment_result"] = result
                        logger.info("Enrichment completed successfully")

                    except Exception as exc:
                        logger.exception("Enrichment service failed")
                        st.session_state["enrichment_result"] = {"error": str(exc)}

        enrichment_result = st.session_state.get("enrichment_result")
        logger.info(enrichment_result)

        if not enrichment_result:
            return

        if isinstance(enrichment_result, dict) and "error" in enrichment_result:
            st.error("Error to connect with enrichment service")
            return

        # Normal case: API already returned JSON
        if isinstance(enrichment_result, dict) and "response" in enrichment_result:
            data = enrichment_result["response"]

        # Fallback case: API response was not JSON
        elif isinstance(enrichment_result, dict) and "raw_response" in enrichment_result:
            st.error("The enrichment service did not return valid JSON.")
            st.text(enrichment_result["raw_response"])
            return

        else:
            st.error("Unexpected enrichment result format.")
            st.write(enrichment_result)
            return

        locations = [
            item["entity"]
            for item in data.get("entity_locations", [])
            if item.get("entity")
        ]

        keywords = [
            item["key_element"]
            for item in data.get("ke_phrases", [])
            if item.get("key_element")
        ]

        logger.info(keywords)

        topics = [
            item["topic"]
            for item in data.get("topic_domains", [])
            if item.get("topic")
        ]

        st.success("Enrichment completed")

        st.subheader("Locations")
        st.write(", ".join(locations) if locations else "No locations found.")

        st.subheader("Keywords")
        st.write(", ".join(keywords) if keywords else "No keywords found.")

        st.subheader("Topic Domains")
        st.write(", ".join(topics) if topics else "No topic domains found.")
    elif upload_file == "no":
        st.session_state["enrichment_result"] = {"error": "No file uploaded"}

