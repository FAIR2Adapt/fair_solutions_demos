import streamlit as st

from utils.logging_config import setup_logger
from steps.fair_publication.step_1_fair_object import render_step_1
from steps.fair_publication.step_2_resource_source import render_step_2
from steps.fair_publication.step_3_doi import render_step_3_doi
from steps.fair_publication.step_3_pdf import render_step_3_pdf
from steps.fair_publication.step_4_claims import render_step_4
from steps.fair_publication.step_5_nanopublication import render_step_5
from steps.fair_publication.step_6_enrichment import render_step_6

logger = setup_logger("app")


def render_publication_flow() -> None:
    st.success("You selected: FAIRify Publication")

    render_step_2()

    resource_type = st.session_state.get("publication_resource_type")

    if resource_type == "doi":
        render_step_3_doi(logger)

        doi_result = st.session_state.get("doi_result")
        if doi_result and "error" not in doi_result:
            st.divider()
            render_step_4(logger)

            claims_result = st.session_state.get("claims_result")

            if claims_result and "error" not in claims_result:
                st.divider()
                render_step_5(logger)

                nanopublications_result = st.session_state.get("nanopublications_result")

                if nanopublications_result and "error" not in nanopublications_result:
                    st.divider
                    render_step_6(logger)

    elif resource_type == "pdf":
        render_step_3_pdf()


def render_data_flow() -> None:
    st.success("You selected: FAIRify Data")
    st.write("Data FAIRification steps will go here.")


def render() -> None:
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