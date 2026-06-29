import streamlit as st
from services.claims_service import fetch_claims_from_abstract


def _set_claim_status(index: int, status: str) -> None:
    st.session_state["claims_result"][index]["status"] = status
    st.rerun()


def _remove_claim(index: int) -> None:
    st.session_state["claims_result"].pop(index)
    st.rerun()


def _render_claim_card(index: int, claim_data: dict) -> None:
    claim_text = claim_data.get("claim", "")
    status = claim_data.get("status", "pending")

    status_colors = {
        "pending": "#9e9e9e",
        "approved": "#2e7d32",
        "rejected": "#c62828",
    }
    status_color = status_colors.get(status, "#9e9e9e")

    with st.container():
        st.markdown(
            f"""
            <div style="
                padding: 14px;
                border: 1px solid #e6e6e6;
                border-radius: 10px;
                background-color: #f8f9fa;
                margin-bottom: 10px;
            ">
                <div style="
                    font-size: 0.85rem;
                    font-weight: 600;
                    color: {status_color};
                    margin-bottom: 6px;
                    text-transform: uppercase;
                ">
                    {status}
                </div>
                <div style="font-size: 1rem;">
                    {claim_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Approve", key=f"approve_{index}", use_container_width=True):
                _set_claim_status(index, "approved")

        with col2:
            if st.button("🚫 Reject", key=f"reject_{index}", use_container_width=True):
                _set_claim_status(index, "rejected")

        with col3:
            if st.button("🗑 Remove", key=f"remove_{index}", use_container_width=True):
                _remove_claim(index)


def render_step_4(logger) -> None:
    st.subheader("Step  — Claim Extraction")

    doi_result = st.session_state.get("doi_result", {})
    abstract = doi_result.get("abstract")

    if not abstract:
        st.info("No abstract available for claim extraction.")
        return

    if st.button("Extract claims", use_container_width=True):
        logger.info("Requesting data from claim extraction service")

        with st.spinner("Retrieving claims from service..."):
            try:
                claims = fetch_claims_from_abstract(abstract)

                # Normalize claims for review UI
                normalized_claims = [
                    {
                        "claim": claim.get("claim", ""),
                        "status": "pending",
                    }
                    for claim in claims
                    if claim.get("claim")
                ]

                st.session_state["claims_result"] = normalized_claims
                logger.info("Claims detected: %s", normalized_claims)

            except Exception as exc:
                logger.exception("Claim extraction failed")
                st.session_state["claims_result"] = {"error": str(exc)}

    claims_result = st.session_state.get("claims_result")

    if not claims_result:
        return
    
    if "error" in claims_result:
        st.error("Problem to retrive metadata from DOI")
        return

    if isinstance(claims_result, dict) and "error" in claims_result:
        st.error(claims_result["error"])
        return

    st.success("Claims retrieved")

    for index, claim in enumerate(claims_result):
        _render_claim_card(index, claim)