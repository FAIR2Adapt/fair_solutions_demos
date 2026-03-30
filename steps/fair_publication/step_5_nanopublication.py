import streamlit as st
from services.nanopublication_service import create_aida_nanopub
from services.nanopublication_service import publish_nanopublication

def _toggle_visualization(index: int) -> None:
    key = f"show_nanopub_{index}"
    st.session_state[key] = not st.session_state.get(key, False)


def _publish_nanopublication(logger, index: int, nanopub_data: dict) -> None:
    # Placeholder publish action
    # Replace this with your real publish service call
    logger.info("Publishing nanopublication %s", nanopub_data.get("label", f"#{index + 1}"))
    publish_nanopublication(logger, nanopub_data)
    st.session_state[f"published_nanopub_{index}"] = True


def _render_nanopublication_card(logger, index: int, nanopub_data: dict) -> None:
    label = nanopub_data.get("label", f"Nanopublication {index + 1}")
    nanopublication_content = nanopub_data.get("nanopublication", "")

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
                    font-size: 1rem;
                    font-weight: 600;
                    margin-bottom: 4px;
                ">
                    {label}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("👁 Visualize", key=f"visualize_nanopub_{index}", use_container_width=True):
                _toggle_visualization(index)

        with col2:
            st.download_button(
                label="⬇ Download",
                data=str(nanopublication_content),
                file_name=f"nanopublication_{index + 1}.trig",
                mime="text/plain",
                key=f"download_nanopub_{index}",
                use_container_width=True,
            )

        with col3:
            if st.button("🚀 Publish", key=f"publish_nanopub_{index}", use_container_width=True):
                _publish_nanopublication(logger, index, nanopub_data)
                st.success(f"Nanopublication published: {label}")

        if st.session_state.get(f"show_nanopub_{index}", False):
            st.markdown("**Nanopublication content**")
            st.code(str(nanopublication_content), language="turtle")

        if st.session_state.get(f"published_nanopub_{index}", False):
            st.caption("Published")

def render_step_5(logger) -> None:
    st.subheader("Step 5 — Nanopublication generation")

    if st.button("Generate Nanopublication", use_container_width=True):
        logger.info("Generation of nanopublication")

        with st.spinner("Generation of nanopublication..."):
            try:
                claims = st.session_state.get("claims_result")

                nanopublications = []
                for claim in claims:
                    if claim["status"] == "approved":
                        logger.info("Generating nanopublication...")
                        ds, label = create_aida_nanopub(logger, claim)
                        serialized_nanopub = ds.serialize(format="trig")
                        logger.info("Nanopublication generated "+str(label))
                        nanopublications.append({"label":label,"nanopublication":serialized_nanopub})

                st.session_state["nanopublications_result"] = nanopublications
                
            except Exception as exc:
                logger.exception("Nanopublication generation failed")
                st.session_state["nanopublications_result"] = {"error": str(exc)}

    nanopublications_result = st.session_state.get("nanopublications_result")

    if not nanopublications_result:
        return

    if isinstance(nanopublications_result, dict) and "error" in nanopublications_result:
        st.error(nanopublications_result["error"])
        return

    st.success("Nanopublications generated")

    for index, nanopub in enumerate(nanopublications_result):
        _render_nanopublication_card(logger, index, nanopub)