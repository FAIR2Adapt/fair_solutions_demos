import streamlit as st

def render_add_metadata_manually(logger) -> None:
    st.subheader("Step: Enter Title and Abstract of the publication")

    st.text_input(
        "Title",
        key="title_value",
    )

    st.text_input(
        "Abstract",
        key="abstract_value",
    )

    if st.button("Next", use_container_width=True):
        title = st.session_state.get("title_value", "").strip()
        abstract = st.session_state.get("abstract_value", "").strip()

        if not title:
            logger.warning("Empty Title")
            st.warning("Please enter a Title.")
            return
        
        if not abstract:
            logger.warning("Empty Abstract")
            st.warning("Please enter an Abstract.")
            return
        
        doi_result = {
            "source": "Manual",
            "title": title,
            "abstract": abstract
        }
        
        st.session_state["doi_result"] = doi_result

