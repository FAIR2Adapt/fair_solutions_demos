import streamlit as st


def render_step_3_pdf() -> None:
    st.subheader("Step 3 — Upload the PDF")

    pdf_file = st.file_uploader(
        "Upload the PDF file",
        type=["pdf"],
        key="pdf_file",
    )

    if pdf_file is not None:
        st.info(f"Uploaded PDF: {pdf_file.name}")