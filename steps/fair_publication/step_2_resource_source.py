import streamlit as st


def render_step_select_resource() -> None:
    st.subheader("Step: Select the resource source")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔗 The resource has a DOI", use_container_width=True):
            st.session_state["publication_resource_type"] = "doi"
            st.session_state.pop("pdf_file", None)
            st.session_state.pop("claims_result", None)

    #with col2:
    #    if st.button("📄 The resource is described in a PDF", use_container_width=True):
    #        st.session_state["publication_resource_type"] = "pdf"
    #        st.session_state.pop("doi_value", None)
    #        st.session_state.pop("doi_result", None)
    #        st.session_state.pop("claims_result", None)