import streamlit as st

from utils.logging_config import setup_logger
from steps.fair_publication.step_1_fair_object import render_step_1
from steps.fair_publication.step_2_resource_source import render_step_2
from steps.fair_publication.step_3_doi import render_step_3_doi

logger = setup_logger("app")

def render_publication_flow() -> None:
    st.success("You selected: FAIRify Data")
    st.write("Data FAIRification steps will go here.")
    st.write("Operation not allowed in this FAIR Solution")

def render_data_flow() -> None:
    st.success("You selected: FAIRify Publication")
    st.write("Data FAIRification steps will go here.")

    st.success("You selected: FAIRify Publication")

    render_step_2()

    resource_type = st.session_state.get("publication_resource_type")

    if resource_type == "doi":
        render_step_3_doi(logger)

        doi_result = st.session_state.get("doi_result")

def render():
    logger.info("Rendering page_fs_4")

    st.title("FAIRification Assistant")

    st.write(
        """
        This tool helps researchers make their research outputs FAIR
        (Findable, Accessible, Interoperable, and Reusable).
        """
    )

    st.divider()

    render_step_1()

    st.divider()

    fair_object = st.session_state.get("fair_object")

    if fair_object == "publication":
        render_publication_flow()
    elif fair_object == "data":
        render_data_flow()
