import streamlit as st
from utils.fair_publication_state import clear_publication_inputs, clear_data_inputs


def render_step_1() -> None:
    st.subheader("Step 1 — What do you want to FAIRify?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💻 FAIRify Data", use_container_width=True):
            st.session_state["fair_object"] = "data"
            clear_publication_inputs()
            clear_data_inputs()