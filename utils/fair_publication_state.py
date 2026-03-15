import streamlit as st


def split_abstract(text: str, max_chars: int = 300) -> tuple[str, str]:
    if not text:
        return "", ""

    if len(text) <= max_chars:
        return text, ""

    preview = text[:max_chars].rstrip()
    remainder = text[max_chars:].lstrip()
    return preview + "...", remainder


def clear_publication_inputs() -> None:
    for key in [
        "publication_resource_type",
        "doi_value",
        "doi_result",
        "pdf_file",
        "claims_result",
    ]:
        st.session_state.pop(key, None)


def clear_data_inputs() -> None:
    for key in [
        "data_resource_type",
    ]:
        st.session_state.pop(key, None)


def clear_all_fair_inputs() -> None:
    for key in [
        "fair_object",
        "publication_resource_type",
        "data_resource_type",
        "doi_value",
        "doi_result",
        "pdf_file",
        "claims_result",
    ]:
        st.session_state.pop(key, None)