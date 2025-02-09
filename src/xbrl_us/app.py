from pathlib import Path

import streamlit as st

from xbrl_us import XBRL

user_info_path = Path.home() / ".xbrl-us"


def try_credentials(user_name: str, pass_word: str, client_id: str, client_secret: str, store: bool = False):
    try:
        if store:
            store = "y"
        else:
            store = "n"
        with st.spinner(text="Validating credentials..."):
            XBRL(username=user_name, password=pass_word, client_id=client_id, client_secret=client_secret)._get_token(store=store)
            st.session_state.username = user_name
            st.session_state.password = pass_word
            st.session_state.client_id = client_id
            st.session_state.client_secret = client_secret
            st.session_state.returning_user = True
    except Exception as e:
        st.error(f"Invalid credentials. Please try again. {e}")
        st.stop()


@st.cache_data(show_spinner=False)
def cache_params(params: dict):
    cached_params = {
        "method": params.get("method", None),
        "fields": params.get("fields", None),
        "parameters": params.get("parameters", None),
        "limit": params.get("limit", None),
        "sort": params.get("sort", None),
        "unique": params.get("unique", False),
        "print_query": params.get("print_query", True),
        "as_dataframe": params.get("as_dataframe", True),
        "streamlit": params.get("streamlit", True),
    }

    st.session_state.cached_params = cached_params


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

    # checkbox for remember me
    remember_me = st.checkbox(
        label="Remember me",
        value=False,
        key="remember_me",
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
        try_credentials(user_name=username, pass_word=password, client_id=client_id, client_secret=client_secret, store=remember_me)
        st.experimental_rerun()


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
        label_visibility="collapsed",
    )


def boolean_input_for_booleans(key):
    st.radio(
        label=f"Input **{key}**:",
        options=("true", "false"),
        horizontal=True,
        key=f"{key}",
        label_visibility="collapsed",
    )


def range_and_slider_for_array_integers(key, values):
    st.radio(
        label=f"Input **{key}** as a range or list:",
        options=("Range", "List"),
        horizontal=True,
        key=f"{key}_input_method",
        label_visibility="collapsed",
        on_change=lambda: st.session_state.pop(f"{key}"),
    )

    if st.session_state[f"{key}_input_method"] == "Range":
        # update_slider_range("period.fiscal-year_input")
        col1, col2 = st.columns(2)

        if values["max"] - values["min"] > 200:
            col1.number_input(
                label="Between",
                min_value=values["min"],
                max_value=values["max"],
                value=values["min"],
                key=f"{key}_min_value",
            )

            col2.number_input(
                label="And",
                min_value=values["min"],
                max_value=values["max"],
                value=values["max"],
                key=f"{key}_max_value",
            )

            st.session_state[key] = range(st.session_state[f"{key}_min_value"], st.session_state[f"{key}_max_value"] + 1)

        else:
            st.slider(
                label=f"**{key}**",
                min_value=values["min"],
                max_value=values["max"],
                value=(values["min"], values["max"]),
                label_visibility="collapsed",
                key=f"{key}_selector",
            )

            if st.session_state[f"{key}_selector"][0] == st.session_state[f"{key}_selector"][1]:
                st.error(f"switch to list mode and select {st.session_state[f'{key}'][0]}")

            st.session_state[key] = range(st.session_state[f"{key}_selector"][0], st.session_state[f"{key}_selector"][1] + 1)

    else:
        st.multiselect(
            label=f"{key}",
            options=list(range(values["min"], values["max"])),
            key=f"{key}",
            label_visibility="collapsed",
        )


def text_box_for_array_strings_no_ops(key, palceholder):
    st.text_area(
        label=f"**{key}**",
        placeholder=f"{palceholder}",
        key=f"{key}",
    )


def restart_everything():
    st.session_state.clear()
    st.session_state.update({"returning_user": False})


if __name__ == "__main__":
    st.set_page_config(
        page_title="XBRL.US API Explorer",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.title("Explore XBRL.us Data")

    sidebar = st.sidebar
    if user_info_path.exists():
        if "returning_user" not in st.session_state:
            st.session_state.returning_user = True
            temp_xbrl = XBRL()
            # show button to continue with the username
            st.session_state.username = temp_xbrl.username
            st.session_state.password = temp_xbrl.password
            st.session_state.client_id = temp_xbrl.client_id
            st.session_state.client_secret = temp_xbrl.client_secret

    if "returning_user" not in st.session_state or not st.session_state.returning_user:
        st.error("Please enter your credentials to begin.")

        with sidebar:
            show_login()
        st.stop()
    if "returning_user" in st.session_state and st.session_state.returning_user:
        with sidebar:
            st.success(f"Logged in as {st.session_state.username}")
            st.button(
                label="Log out",
                type="secondary",
                use_container_width=True,
                on_click=lambda: restart_everything(),
                key="logout",
            )

        xbrl = XBRL(
            username=st.session_state.username,
            password=st.session_state.password,
            client_id=st.session_state.client_id,
            client_secret=st.session_state.client_secret,
        )
        if "account_limit" in st.session_state:
            xbrl.account_limit = st.session_state.account_limit

        st.session_state.methods = xbrl.methods()

        method = sidebar.selectbox(
            label="API Method",
            options=[
                "fact search",
                "report search",
                "entity search",
            ],  # sorted(st.session_state.methods), TODO: This is hard coded. Need to fix it.
            index=0,
            key="method",
            disabled=False,
            help="""Select the method you would like to use.
            For more information on the methods,
            see the [XBRL.US API Documentation](https://xbrlus.github.io/xbrl-api/#/).""",
        )

        # get the acceptable parameters for the method
        st.session_state.method_params = xbrl.acceptable_params(method)
        # parameters_options = dict(sorted(method_params.parameters.items(), key=lambda x: x[1]['type']))
        # print the name of the method
        st.header(method)

        # two tabs
        method_summary, definitions = st.tabs(["Summary", "Field Definition"])

        with method_summary:
            st.markdown(st.session_state.method_params.description)
            st.markdown(
                f"{st.session_state.method_params.long_description} <sup>[1]({st.session_state.method_params.reference})</sup>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**Glossary**: {st.session_state.method_params.reference}")
            st.caption(f"**API end-point**: {xbrl.acceptable_params(method).url}")
            # print the url of the method

        with definitions:
            with st.expander("Search Definitions", expanded=True):
                if "fields" in st.session_state and len(st.session_state.fields) > 0:
                    st.markdown(f"**Field Name**: *{st.session_state.fields[-1]}*")
                    st.markdown(f"**Description**: {xbrl.define(st.session_state.fields[-1])['description']}")
                else:
                    st.info("Select a field to see the definition")

        # show the list of fields in the sidebar
        with st.container():
            sidebar.multiselect(
                label="Parameters",
                options=st.session_state.method_params.parameters,
                key="parameters",
            )

            sidebar.multiselect(
                label="Fields :red[*]",
                options=st.session_state.method_params.fields,
                key="fields",
            )

            sidebar.multiselect(
                label="Sort",
                options=st.session_state.fields,
                key="sort",
            )

            if len(st.session_state.sort) == 0:
                sidebar.warning("It is recommended to choose at least one field to sort")

            # check box for unique
            sidebar.checkbox(
                label="Unique",
                key="unique_yes",
                help="Return unique rows from the results",
            )

            st.session_state.limit_param = None

            if st.session_state.method_params.limit:
                # check box for limit
                sidebar.toggle(
                    label="Download All",
                    value=False,
                    key="download_all",
                )
                if not st.session_state.download_all:
                    limit = sidebar.number_input(
                        label=f"**{st.session_state.method_params.limit[0]} limit:**",
                        value=100,
                    )
                    st.session_state.limit_param = limit
                else:
                    st.session_state.limit_param = "all"
                    sidebar.error(
                        """This may take a long time to run. Only use this option if you are sure you want to retrieve all the data."""
                    )

        query_button_placeholder = st.empty()
        show_criteria = True
        show_criteria_placeholder = st.empty()
        if len(st.session_state.parameters) == 0 and len(st.session_state.sort) == 0:
            st.info("No **Sort** or search criteria (**Parameters**) has been selected")
        else:
            # a checkbox to expand the query criteria
            query_button = show_criteria_placeholder.checkbox(
                label="Show Query Criteria",
                key="query_button",
                value=True,
            )
            if not query_button:
                show_criteria = False
        with st.expander(label="**Query Criteria Details**", expanded=show_criteria):
            st.session_state.sort_params = {}
            if len(st.session_state.sort) > 0:
                st.subheader("**Sort**:")
                for field in st.session_state.sort:
                    sort_order = st.radio(
                        label=f"**{field}**:",
                        options=("Ascending", "Descending"),
                        horizontal=True,
                        key=f"{field}_sort",
                    )
                    st.session_state.sort_params[field] = "asc" if sort_order == "Ascending" else "desc"
                st.markdown("---")

            for param in st.session_state.parameters:
                st.subheader(f"**{param}**:")
                param_info = xbrl.define(param)
                st.markdown(param_info["description"])
                type = param_info["type"]

                if type == "boolean":
                    boolean_input_for_booleans(param)

                elif type == "integer":
                    input_number_for_integers(param)

                elif type == "string":
                    text_input_for_strings(param)

                elif type == "array[integer]":
                    range_and_slider_for_array_integers(
                        param,
                        param_info["values"],
                    )

                elif type == "array[string]":
                    text_box_for_array_strings_no_ops(
                        param,
                        param_info["placeholder"],
                    )

            st.session_state.query_params = {"fields": st.session_state.fields}

            if len(st.session_state.parameters) > 0:
                st.session_state.query_params["parameters"] = {}
                for param in st.session_state.parameters:
                    st.session_state.query_params["parameters"][param] = st.session_state[param]

            if len(st.session_state.sort_params) > 0:
                st.session_state.query_params["sort"] = st.session_state.sort_params
            if st.session_state.limit_param:
                st.session_state.query_params["limit"] = st.session_state.limit_param
            if st.session_state.unique_yes:
                st.session_state.query_params["unique"] = True
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

        query_button_placeholder.button(
            label="Run Query",
            key="run_query",
            type="primary",
            use_container_width=True,
            disabled=query_btn_disabled,
        )
        new_results_placeholder = st.empty()
        if st.session_state.run_query:
            try:
                with st.spinner("Running query..."):
                    st.session_state.pop("last_query", None)
                    st.session_state.last_query = xbrl.query(
                        **st.session_state.query_params, as_dataframe=True, print_query=True, streamlit=True, timeout=10
                    )
                    if "account_limit" not in st.session_state:
                        st.session_state.account_limit = xbrl.account_limit

            except Exception as e:
                new_results_placeholder.error(f"{e}")
                st.stop()

        with new_results_placeholder.container():
            # show the dataframe
            st.subheader("Last Query Results")
            if "last_query" not in st.session_state:
                st.info("No **Query** has been submitted yet")

            else:
                # show a download button to get the data in csv format
                # box for file name
                filename = st.text_input(
                    label="File Name",
                    value="xbrl data",
                )
                dwnld_btn_place, del_btn_place = st.columns(2)

                # show a button to show the full data
                st.checkbox(
                    label="My computer rocks! 🚀 Show Full Data",
                    help="Show the full data.",
                    key="show_full_data",
                )
                if st.session_state.show_full_data:
                    st.success(
                        f"""Viewing full data: **{st.session_state.last_query.shape[0]}**
                        rows and **{st.session_state.last_query.shape[1]}** columns."""
                    )

                    st.dataframe(
                        data=st.session_state.last_query,
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.success(
                        f"""Query has **{st.session_state.last_query.shape[0]}** rows.
                        You are viewing **{min(100, st.session_state.last_query.shape[0])}** rows
                        and **{st.session_state.last_query.shape[1]}** columns.
                        You can try **Show Full Data** or **Download** the full data instead."""
                    )

                    st.dataframe(
                        data=st.session_state.last_query.head(100),
                        use_container_width=True,
                        hide_index=True,
                    )

                with dwnld_btn_place:
                    st.download_button(
                        label="Download as CSV File",
                        use_container_width=True,
                        data=st.session_state.last_query.to_csv(index=False).encode("utf-8"),
                        file_name=f"{filename}.csv",
                        mime="text/csv",
                        key="download_data",
                    )

                with del_btn_place:
                    st.button(
                        label="Delete Query",
                        key="delete_query_btn",
                        on_click=lambda: st.session_state.pop("last_query"),
                        type="primary",
                        use_container_width=True,
                    )

        # st.write(st.session_state)
