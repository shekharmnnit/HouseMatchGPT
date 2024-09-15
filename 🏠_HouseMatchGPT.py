import streamlit as st

import helpers.sidebar

st.set_page_config(
	page_title="HouseMatchGPT",
	page_icon="🧑‍💻",
	layout="wide"
)

helpers.sidebar.show()

st.toast("Welcome to HouseMatchGPT!", icon="🧑‍💻")

st.markdown("Welcome to HouseMatchGPT, your AI-driven search engine for your real estate!")
st.write("HouseMatchGPT is crafted to aid you in exploring and comprehending your home search effectively.")

