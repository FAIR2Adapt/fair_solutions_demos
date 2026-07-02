import streamlit as st
from services.fdo_service import generate_CS1_fdo

def render_step_7(logger) -> None:
    st.subheader("Step: FDO Creation")

    if st.button("Generate FDO", use_container_width=True):
        with st.spinner("Generating FDO..."):
            try:
                doi_result = st.session_state["doi_result"]

                creators_text = "\n".join(
                    f"- {creator.get('name', '').replace(',', '')}"
                    for creator in doi_result.get("creators", [])
)

                abstract = doi_result.get("abstract", "")

                doi_result["abstract"] = (
                    f"{abstract}\n\n"
                    f"DOI: {doi_result["doi"]}\n\n"
                    f"Creators: {creators_text}\n\n"
                    f"Citation: {doi_result["citation_text"]}"
                )

                logger.info("New abstract")
                logger.info(doi_result["abstract"])

                result = generate_CS1_fdo(logger, doi_result)

                st.session_state["fdo_generation_result"] = result

                
            except Exception as exc:
                logger.exception("FDO Generation service failed")
                st.session_state["fdo_generation_result"] = {"error": str(exc)}

    fdo_generation_result = st.session_state.get("fdo_generation_result")

    if not fdo_generation_result:
        return

    st.success("FDO generated")