import streamlit as st

from xbrl_us import XBRL


def try_credentials(user_name: str, pass_word: str, client_id: str, client_secret: str):
    try:
        with st.spinner(text="Validating credentials..."):
            XBRL(username=user_name, password=pass_word, client_id=client_id, client_secret=client_secret)._get_token()
            st.session_state.username = user_name
            st.session_state.password = pass_word
            st.session_state.client_id = client_id
            st.session_state.client_secret = client_secret
    except Exception as e:
        st.error(f"Invalid credentials. Please try again. {e}")
        st.stop()


@st.cache_data(show_spinner="Running query...")
def run_query(params: dict):
    st.empty()
    method = params.get("method", None)
    fields = params.get("fields", None)
    parameters = params.get("parameters", None)
    limit = params.get("limit", None)
    sort = params.get("sort", None)
    df = xbrl.query(
        method=method,
        fields=fields,
        parameters=parameters,
        limit=limit,
        sort=sort,
        as_dataframe=True,
        print_query=True,
    )

    st.session_state.last_query = df
    st.session_state.pop("query_params")


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

    disable_login_btn = False
    if username == "" or password == "" or client_id == "" or client_secret == "":
        disable_login_btn = True

    verify_api = st.button(
        label="Create a New Session",
        type="primary",
        use_container_width=True,
        disabled=disable_login_btn,
    )
    if verify_api:
        # try the credentials before creating xbrl object
        try_credentials(user_name=username, pass_word=password, client_id=client_id, client_secret=client_secret)
        st.experimental_rerun()


def update_number_input(slider_key: str, number_input_key_min: str, number_input_key_max: str):
    st.session_state[number_input_key_min] = st.session_state[slider_key][0]
    st.session_state[number_input_key_max] = st.session_state[slider_key][1]


def input_number_for_integers(key):
    st.number_input(
        label=f"Input **{key}**:",
        value=0,
        key=f"{key}",
    )


def text_input_for_strings(key):
    st.text_input(
        label=f"Input **{key}**:",
        value="",
        key=f"{key}",
    )


def boolean_input_for_booleans(key):
    st.radio(
        label=f"Input **{key}**:",
        options=("true", "false"),
        horizontal=True,
        key=f"{key}",
    )


def range_and_slider_for_array_integers(key):
    st.radio(
        label=f"Input **{key}** as a range or list:",
        options=("Range", "List"),
        horizontal=True,
        key=f"{key}_input_method",
    )

    if st.session_state[f"{key}_input_method"] == "Range":
        # update_slider_range("period.fiscal-year_input")
        col1, col2 = st.columns(2)

        col1.number_input(
            label="Between",
            min_value=1952,
            max_value=9999,
            value=1952,
            key=f"{key}_min_value",
        )

        col2.number_input(
            label="And",
            min_value=1952,
            max_value=9999,
            value=2021,
            key=f"{key}_max_value",
        )

        st.slider(
            label=f"**{key}**",
            min_value=1952,
            max_value=2023,
            value=[st.session_state[f"{key}_min_value"], st.session_state[f"{key}_max_value"]],
            key=f"{key}",
            on_change=update_number_input,
            args=(
                f"{key}",
                f"{key}",
                f"{key}_max_value",
            ),
        )

        if st.session_state[f"{key}"][0] == st.session_state[f"{key}"][1]:
            st.error(f"switch to list mode and select {st.session_state[f'{key}'][0]}")
    else:
        st.multiselect(
            label=f"{key}",
            options=list(range(1952, 2024)),
            key=f"{key}",
        )


def text_box_for_array_strings_no_ops(key):
    st.text_area(
        label=f"**{key}**",
        key=f"{key}",
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="XBRL.US API Explorer",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Explore [XBRL.us](https://xbrl.us/)")

    sidebar = st.sidebar
    if "username" not in st.session_state:
        st.error("Please enter your credentials to begin.")

        with sidebar:
            show_login()
        st.stop()
    else:
        with sidebar:
            st.button(
                label="Reset Credentials",
                type="secondary",
                use_container_width=True,
                on_click=lambda: st.session_state.clear(),
                key="logout",
            )

        xbrl = XBRL(
            username=st.session_state.username,
            password=st.session_state.password,
            client_id=st.session_state.client_id,
            client_secret=st.session_state.client_secret,
        )

        st.session_state.methods = xbrl.methods()

        method = sidebar.selectbox(
            label="API Method",
            options=sorted(st.session_state.methods),
            index=19,
            key="method",
            disabled=True,
            help="""Select the method you would like to use.
            For more information on the methods,
            see the [XBRL.US API Documentation](https://xbrlus.github.io/xbrl-api/#/).""",
        )

        # get the acceptable parameters for the method
        st.session_state.method_params = xbrl.acceptable_params(method)
        # parameters_options = dict(sorted(method_params.parameters.items(), key=lambda x: x[1]['type']))
        # print the name of the method
        st.header(method)
        st.markdown(st.session_state.method_params.description)
        st.caption(f"**API end-point**: {xbrl.acceptable_params(method).url}")
        # print the url of the method

        # show the list of fields in the sidebar
        with st.container():
            sidebar.multiselect(
                label="Fields :red[*]",
                options=st.session_state.method_params.fields,
                key="fields",
            )

            sidebar.multiselect(
                label="Parameters",
                options=st.session_state.method_params.parameters,
                key="parameters",
            )

            sidebar.multiselect(
                label="Sort",
                options=st.session_state.fields,
                key="sort",
            )

            if len(st.session_state.sort) == 0:
                sidebar.warning("Please select at least one field to sort by.")

            st.session_state.limit_param = None
            # check box for limit
            sidebar.checkbox(
                label="Limit",
                key="limit_yes",
            )
            if st.session_state.limit_yes:
                for field in st.session_state.method_params.limit:
                    limit = sidebar.number_input(
                        label=f"**{field} limit:**",
                        value=100,
                    )
                    st.session_state.limit_param = limit

        with st.expander(label="**Query Criteria Details**", expanded=True):
            if len(st.session_state.parameters) == 0:
                st.info("Your query criteria will be applied to the following fields")

            st.session_state.sort_params = {}
            if len(st.session_state.sort) > 0:
                st.subheader("**Sort**:")
                for field in st.session_state.sort:
                    sort_order = st.radio(
                        label=f"Sort order for {field}:",
                        options=("Ascending", "Descending"),
                        horizontal=True,
                        key=f"{field}_sort",
                    )
                    st.session_state.sort_params[field] = "asc" if sort_order == "Ascending" else "desc"

            for param in st.session_state.parameters:
                st.subheader(f"**{param}**:")
                st.write(st.session_state.method_params.parameters[param]["description"])

                if st.session_state.method_params.parameters[param]["type"] == "boolean":
                    boolean_input_for_booleans(param)

                elif st.session_state.method_params.parameters[param]["type"] == "integer":
                    st.write(f"**{param}** is Integer")
                    input_number_for_integers(param)

                elif st.session_state.method_params.parameters[param]["type"] == "string":
                    st.write(f"**{param}** is String")
                    text_input_for_strings(param)

                elif st.session_state.method_params.parameters[param]["type"] == "array[integer]":
                    range_and_slider_for_array_integers(param)

                elif st.session_state.method_params.parameters[param]["type"] == "array[string]":
                    text_box_for_array_strings_no_ops(param)

            st.session_state.query_params = {"fields": st.session_state.fields}

            if len(st.session_state.parameters) > 0:
                st.session_state.query_params["parameters"] = {}
                for param in st.session_state.parameters:
                    st.session_state.query_params["parameters"][param] = st.session_state[param]

            if len(st.session_state.sort_params) > 0:
                st.session_state.query_params["sort"] = st.session_state.sort_params
            if st.session_state.limit_param:
                st.session_state.query_params["limit"] = st.session_state.limit_param
            st.session_state.query_params["method"] = method

    # create a checkbox to show the query parameters
    st.checkbox(
        label="Show Query Parameters",
        key="show_query_params",
        help="Show the query parameters.",
    )
    if st.session_state.show_query_params:
        st.write(st.session_state.query_params)

    # run the query
    query_btn_disabled = True
    if len(st.session_state["fields"]) > 0:
        query_btn_disabled = False

    st.button(
        label="Run Query",
        key="run_query",
        type="primary",
        use_container_width=True,
        disabled=query_btn_disabled,
        on_click=run_query,
        args=(st.session_state.query_params,),
    )

    # show the dataframe
    if "last_query" not in st.session_state:
        st.info("your data will appear here")

    else:
        st.subheader("Last Query Results")

        # show a button to show the full data
        st.checkbox(
            label="My computer rock! 🚀 Show Full Data",
            help="Show the full data.",
            key="show_full_data",
        )

        if st.session_state.show_full_data:
            st.dataframe(
                data=st.session_state.last_query,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.success(f"This query has {st.session_state.last_query.shape[0]} rows. " f"but you are only seeing the first 100 rows.")

            st.dataframe(
                data=st.session_state.last_query.head(100),
                use_container_width=True,
                hide_index=True,
            )

        # show a download button to get the data in csv format
        # box for file name
        filename = st.text_input(
            label="File Name",
            value="xbrl data",
        )

        col1_data, col2_data = st.columns(2)
        with col1_data:
            st.download_button(
                label="Download as CSV File",
                use_container_width=True,
                data=st.session_state.last_query.to_csv(index=False).encode("utf-8"),
                file_name=f"{filename}.csv",
                mime="text/csv",
                key="download_data",
            )

        with col2_data:
            st.button(
                label="Delete Query",
                key="delete_query_btn",
                on_click=lambda: st.session_state.pop("last_query"),
                type="primary",
                use_container_width=True,
            )

    # st.write(st.session_state)
