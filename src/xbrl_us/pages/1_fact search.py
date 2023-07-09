import streamlit as st

if "instance" not in st.session_state:
    st.error("Please generate an API token.")
    st.stop()

else:
    st.write("## XBRL US API")
