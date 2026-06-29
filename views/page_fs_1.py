import streamlit as st
from utils.logging_config import setup_logger

from steps.fair_dataset.step_1_fair_dataset import render_step_1
from steps.fair_dataset.step_2_url import render_step_url
from steps.fair_publication.step_4_claims import render_step_4
from steps.fair_publication.step_5_nanopublication import render_step_5
from steps.fair_dataset.step_3_fdo import render_step_7


logger = setup_logger("app")

def render_data_flow() -> None:
    st.success("You selected: FAIRify Dataset")

    render_step_url(logger)

    url_result = st.session_state.get("url_result")

    if url_result and "error" not in url_result:
        logger.info(url_result)
        st.text("Next step")



def render():
    st.title("FAIR Solution #1")

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

    if fair_object == "data":
        render_data_flow()

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
                    st.divider()
                    render_step_7(logger)