import streamlit as st

from utils.logging_config import setup_logger
from steps.fair_publication.step_1_fair_object import render_step_1
from steps.fair_publication.step_2_resource_source import render_step_select_resource
from steps.fair_publication.step_3_doi import render_step_doi
from steps.fair_publication.step_3_pdf import render_step_3_pdf
from steps.fair_publication.step_4_claims import render_step_4
from steps.fair_publication.step_5_nanopublication import render_step_5
from steps.fair_publication.step_6_enrichment import render_step_6
from steps.fair_publication.step_7_fdo import render_step_7
from steps.fair_publication.step_add_metadata_manually import render_add_metadata_manually


logger = setup_logger("app")



def render_publication_flow() -> None:
    st.success("You selected: FAIRify Publication")

    render_step_select_resource()

    resource_type = st.session_state.get("publication_resource_type")

    if resource_type == "doi":
        render_step_doi(logger)

        doi_result = st.session_state.get("doi_result")

        # Case 1: DOI metadata retrieved successfully
        if doi_result and "error" not in doi_result:
            st.divider()
            render_step_4(logger)

            claims_result = st.session_state.get("claims_result")

            if isinstance(claims_result, list) and claims_result:

                # STEP 5: At least one approved claim
                if any(
                    claim.get("status") == "approved"
                    for claim in claims_result
                ):
                    st.divider()
                    render_step_5(logger)

                # STEP 6: All claims reviewed
                if all(
                    claim.get("status") in ("approved", "rejected")
                    for claim in claims_result
                ):
                    st.divider()
                    render_step_6(logger)

            elif isinstance(claims_result, dict) and "error" in claims_result:
                logger.info("Skip claims extraction process")
                st.divider()
                render_step_6(logger)

            # STEP 7: After enrichment
            enrichment_result = st.session_state.get("enrichment_result")

            if enrichment_result:
                st.divider()
                render_step_7(logger)

        # Case 2: DOI retrieval failed; manual metadata
        elif doi_result and "error" in doi_result:
            render_add_metadata_manually(logger)

            doi_result = st.session_state.get("doi_result")

            if doi_result and "error" not in doi_result:
                st.divider()
                logger.info("STEP 4 enter")
                render_step_4(logger)

                claims_result = st.session_state.get("claims_result")
                logger.info("STEP 4 exit")
                logger.info(claims_result)

                if isinstance(claims_result, list) and claims_result:

                    # STEP 5: At least one approved claim
                    if any(
                        claim.get("status") == "approved"
                        for claim in claims_result
                    ):
                        st.divider()
                        logger.info("Enter nanopublication generation")
                        render_step_5(logger)

                    # STEP 6: All claims reviewed
                    if all(
                        claim.get("status") in ("approved", "rejected")
                        for claim in claims_result
                    ):
                        st.divider()
                        render_step_6(logger)

                elif isinstance(claims_result, dict) and "error" in claims_result:
                    logger.info("Skip claims extraction process")
                    st.divider()
                    render_step_6(logger)

                # STEP 7: After enrichment
                enrichment_result = st.session_state.get("enrichment_result")

                if enrichment_result and "error" not in enrichment_result:
                    st.divider()
                    render_step_7(logger)

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