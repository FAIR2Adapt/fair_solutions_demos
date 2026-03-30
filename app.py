import streamlit as st

from views.overview import render as overview
from views.page_fs_1 import render as page_fs_1
from views.page_fs_2 import render as page_fs_2
from views.page_fs_3 import render as page_fs_3
from views.page_fs_4 import render as page_fs_4

st.set_page_config(
    page_title="Fair Solutions Demos",
    page_icon="📊",
    layout="wide"
)

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Overview"

st.sidebar.title("Menu")

if st.sidebar.button("🏠 Overview", use_container_width=True):
    st.session_state["selected_page"] = "Overview"


if st.sidebar.button("1️⃣ FAIR Solution #1", use_container_width=True):
    st.session_state["selected_page"] = "FAIR Solution #1"

if st.sidebar.button("2️⃣ FAIR Solution #2", use_container_width=True):
    st.session_state["selected_page"] = "FAIR Solution #2"

if st.sidebar.button("3️⃣ FAIR Solution #3", use_container_width=True):
    st.session_state["selected_page"] = "FAIR Solution #3"

if st.sidebar.button("4️⃣ FAIR Solution #4", use_container_width=True):
    st.session_state["selected_page"] = "FAIR Solution #4"

page = st.session_state["selected_page"]

if page == "Overview":
    overview()
#elif page == "FAIR Solution #1":
#    page_fs_1()
#elif page == "FAIR Solution #2":
#    page_fs_2()
#elif page == "FAIR Solution #3":
#    page_fs_3()
elif page == "FAIR Solution #4":
    page_fs_4()