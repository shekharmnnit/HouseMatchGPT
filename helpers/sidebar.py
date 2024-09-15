import streamlit as st


def show() -> None:
	with st.sidebar:
		st.markdown(f"""
			<a href="/" style="color:black;text-decoration: none;">
				<div style="display:table;margin-top:-16rem;margin-left:0%;">
					<img src="/app/static/home.png" width="55">
					<span style="font-size: 1.1em; color: #4CAF50;">AI search engine for Homes</span><br>
				</div>
			</a>
			<br>
				""", unsafe_allow_html=True)

		reload_button = st.button("↪︎  Reload Page")
		if reload_button:
			st.session_state.clear()
			# st.experimental_rerun()

