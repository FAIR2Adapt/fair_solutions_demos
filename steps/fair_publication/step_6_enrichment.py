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

        if not enrichment_result:
            return

        if isinstance(enrichment_result, dict) and "error" in enrichment_result:
            st.error(enrichment_result["error"])
            return

        st.success("Enrichment completed")
        st.json(enrichment_result)

