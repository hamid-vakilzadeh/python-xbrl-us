import streamlit as st

from xbrl_us import XBRL


def generate_token(username: str, password: str, client_id: str, client_secret: str):
    try:
        XBRL(username=username, password=password, client_id=client_id, client_secret=client_secret)._get_token()
    except Exception as e:
        st.error(e)
        st.stop()

    return XBRL(username=username, password=password, client_id=client_id, client_secret=client_secret)


if __name__ == "__main__":
    st.title("XBRL US")

    # Setup credentials in Streamlit
    username = st.text_input(
        label="Username",
        type="password",
        help="Your username for the [XBRL.US](https://www.xbrl.us) API.",
    )

    password = st.text_input(
        "Password",
        type="password",
        help="Your password for the [XBRL.US](https://www.xbrl.us) API.",
    )

    client_id = st.text_input(
        "Client ID",
        type="password",
        help="Your client ID for the [XBRL.US](https://www.xbrl.us) API.",
    )

    client_secret = st.text_input(
        "Client Secret",
        type="password",
        help="Your client secret for the [XBRL.US](https://www.xbrl.us) API.",
    )

    generate_api = st.button(
        label="Generate token",
        help="Connect to the [XBRL.US](https://www.xbrl.us) API.",
        type="primary",
    )

    if generate_api:
        st.session_state.instance = generate_token(username=username, password=password, client_id=client_id, client_secret=client_secret)
        st.write("Connected to XBRL.US API!")
    # st.write(st.session_state.instance.access_token)
    st.write(st.session_state)
