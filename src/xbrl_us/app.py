import streamlit as st

from xbrl_us import XBRL


@st.cache_data(show_spinner="validating credentials...")
def xbrl_instance(user_name: str, pass_word: str, client_id: str, client_secret: str):
    try:
        XBRL(username=user_name, password=pass_word, client_id=client_id, client_secret=client_secret)._get_token()
        return XBRL(username=user_name, password=pass_word, client_id=client_id, client_secret=client_secret)
    except Exception as e:
        st.error(f"Invalid credentials. Please try again. {e}")
        st.stop()


def show_login():
    # Setup credentials in Streamlit
    username = st.text_input(
        label="Username",
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

    verify_api = st.button(
        label="Create a New Session",
        help="Connect to the [XBRL.US](https://www.xbrl.us) API.",
        type="primary",
        use_container_width=True,
    )
    if verify_api:
        # try the credentials before creating an instance
        st.session_state.instance = xbrl_instance(user_name=username, pass_word=password, client_id=client_id, client_secret=client_secret)
        st.experimental_rerun()


def update_number_input(slider_key: str, number_input_key_min: str, number_input_key_max: str):
    st.session_state[number_input_key_min] = st.session_state[slider_key][0]
    st.session_state[number_input_key_max] = st.session_state[slider_key][1]


if __name__ == "__main__":
    st.title("XBRL US")

    sidebar = st.sidebar
    if "instance" not in st.session_state:
        st.error("Please enter your credentials to begin.")
        with sidebar:
            show_login()
        st.stop()
    else:
        with sidebar:
            st.button(
                label="Reset Credentials",
                help="Disconnect from the [XBRL.US](https://www.xbrl.us) API.",
                type="secondary",
                use_container_width=True,
                on_click=lambda: st.session_state.pop("instance"),
                key="logout",
            )

        methods = st.session_state.instance.methods()

        method = sidebar.selectbox(
            label="API Method",
            options=sorted(methods),
            index=19,
            key="method",
        )

        # get the acceptable parameters for the method
        method_params = st.session_state.instance.acceptable_params(method)

        # print the name of the method
        st.header(method)

        # print the url of the method
        st.caption(st.session_state.instance.acceptable_params(method).url)

        # show the list of fields in the sidebar
        with st.container():
            sidebar.multiselect(
                label="Fields :red[*]",
                options=method_params.fields,
                key="fields",
            )

            sidebar.multiselect(
                label="Parameters",
                options=method_params.parameters,
                key="parameters",
            )

            sidebar.multiselect(
                label="Sort",
                options=st.session_state.fields,
                key="sort",
            )

            if len(st.session_state.sort) == 0:
                sidebar.warning("Please select at least one field to sort by.")

            st.session_state.limit_params = {}
            # check box for limit
            sidebar.checkbox(
                label="Limit",
                key="limit_yes",
            )
            if st.session_state.limit_yes:
                for field in method_params.limit:
                    limit = sidebar.number_input(
                        label=f"**{field} limit:**",
                        value=100,
                    )
                    st.session_state.limit_params[field] = limit

            # check box for offset
            sidebar.checkbox(
                label="Offset",
                key="offset_yes",
            )

            if st.session_state.offset_yes:
                sidebar.number_input(
                    label="Offset",
                    value=0,
                    key="offset",
                )

        with st.expander(label="**Query Criteria Details**", expanded=True):
            st.write("Your query criteria will be applied to the following fields")
            st.session_state.sort_params = {}
            if len(st.session_state.sort) > 0:
                for field in st.session_state.sort:
                    sort_order = st.radio(
                        label=f"Sort order for {field}:",
                        options=("Ascending", "Descending"),
                        horizontal=True,
                    )
                    st.session_state.sort_params[field] = "asc" if sort_order == "Ascending" else "desc"

            if "concept.local-name" in st.session_state.parameters:
                st.text_area(
                    label="Concept Local Name",
                    key="concept.local-name",
                )

            if "period.fiscal-year" in st.session_state.parameters:
                # radio options for range or list
                st.radio(
                    label="Input **period.fiscal-year** as a range or list:",
                    options=("Range", "List"),
                    horizontal=True,
                    key="period.fiscal-year_input_method",
                )

                if st.session_state["period.fiscal-year_input_method"] == "Range":
                    # update_slider_range("period.fiscal-year_input")
                    col1, col2 = st.columns(2)

                    col1.number_input(
                        label="Between",
                        min_value=1952,
                        max_value=9999,
                        value=1952,
                        key="period.fiscal-year_min_value",
                    )

                    col2.number_input(
                        label="And",
                        min_value=1952,
                        max_value=9999,
                        value=2021,
                        key="period.fiscal-year_max_value",
                    )

                    st.slider(
                        label="**period.fiscal-year**",
                        min_value=1952,
                        max_value=2023,
                        value=[st.session_state["period.fiscal-year_min_value"], st.session_state["period.fiscal-year_max_value"]],
                        key="period.fiscal-year",
                        on_change=update_number_input,
                        args=(
                            "period.fiscal-year",
                            "period.fiscal-year_min_value",
                            "period.fiscal-year_max_value",
                        ),
                    )

                    if st.session_state["period.fiscal-year"][0] == st.session_state["period.fiscal-year"][1]:
                        st.error(f"switch to list mode and select {st.session_state['period.fiscal-year'][0]}")
                else:
                    st.multiselect(
                        label="Period Fiscal Year",
                        options=list(range(1952, 2024)),
                        key="period.fiscal-year",
                    )

            st.session_state.query_params = {}

            st.session_state.query_params["parameters"] = {item: item for item in st.session_state.parameters}
            for param in st.session_state.parameters:
                st.session_state.query_params["parameters"][param] = st.session_state[param]
            st.session_state.query_params["fields"] = st.session_state.fields
            st.session_state.query_params["sort"] = st.session_state.sort_params
            st.session_state.query_params["limit"] = st.session_state.limit_params
            st.session_state.query_params["method"] = method
            # st.write(st.session_state.query_params)

    # run the query
    query_btn_disabled = True
    if len(st.session_state["fields"]) > 0:
        query_btn_disabled = False

    st.button(
        label="Run Query",
        help="Run the query.",
        key="run_query",
        disabled=query_btn_disabled,
    )
    if "last_query" not in st.session_state:
        st.session_state.last_query = None

    if st.session_state.run_query:
        with st.spinner("Running query..."):
            st.session_state.last_query = st.session_state.instance.query(**st.session_state.query_params, as_dataframe=True)

    # show the dataframe
    if st.session_state.last_query is not None:
        st.write(st.session_state.last_query)

    st.write(st.session_state)
