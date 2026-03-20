import streamlit as st
from services.fdo_service import generate_CS4_fdo

def render_step_7(logger) -> None:
    st.subheader("Step 7 — FDO Creation")

    if st.button("Generate FDO", use_container_width=True):
        with st.spinner("Generating FDO..."):
            try:
                doi_result = st.session_state["doi_result"]
                enrichment_result = st.session_state["enrichment_result"]

                
                result = generate_CS4_fdo(logger, doi_result, enrichment_result)

                st.session_state["fdo_generation_result"] = result

                
            except Exception as exc:
                logger.exception("FDO Generation service failed")
                st.session_state["fdo_generation_result"] = {"error": str(exc)}

    fdo_generation_result = st.session_state.get("fdo_generation_result")

    if not fdo_generation_result:
        return

    st.success("FDO generated")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👁 Visualize", key=f"visualize_enrichment", use_container_width=True):
            logger.info("Visualize")

    with col2:
        st.download_button(
            label="⬇ Download",
            data=str("nothing"),
            file_name=f"fdo.trig",
            mime="text/plain",
            key=f"download_fdo",
            use_container_width=True,
        )