from pathlib import Path

import streamlit as st
import yaml

from xbrl_us import XBRL

user_info_path = Path.home() / ".xbrl-us"
_dir = Path(__file__).resolve().parent


TYPE_MAPPINGS = {
    "text": "text",
    "varchar": "text",
    "bigint": "number",
    "int": "number",
    "boolean": "true/false",
    "numeric": "number",
    "jsonb": "jsonb",
}


def try_credentials(user_name: str, pass_word: str, client_id: str, client_secret: str, store: bool = False):
    try:
        if store:
            store = "y"
        else:
            store = "n"
        with st.spinner(text="Validating credentials..."):
            st.session_state.xbrl = XBRL(
                username=user_name, password=pass_word, client_id=client_id, client_secret=client_secret, store=store
            )
            st.session_state.returning_user = True
    except Exception as e:
        st.error(f"Invalid credentials. Please try again. {e}")
        st.stop()


@st.cache_data(show_spinner=False)
def cache_params(params: dict):
    cached_params = {
        "endpoint": params.get("endpoint", None),
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


def restart_everything():
    st.session_state.clear()
    st.session_state.update({"returning_user": False})


def restart_endpoint():
    st.session_state.pop("endpoint_info", None)
    st.session_state.pop("endpoint_endpoint", None)
    st.session_state.pop("endpoint_parameters", None)
    st.session_state.pop("endpoint_fields", None)
    st.session_state.pop("endpoint_limit", None)
    st.session_state.pop("query_params", None)
    st.session_state.pop("fields", None)


if __name__ == "__main__":
    st.set_page_config(
        page_title="XBRL.US API Explorer",
        page_icon=":material/database_search:",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    sidebar = st.sidebar
    if user_info_path.exists():
        if "returning_user" not in st.session_state:
            st.session_state.returning_user = True
            st.session_state.xbrl = XBRL()

    if "returning_user" not in st.session_state or not st.session_state.returning_user:
        st.error("Please enter your credentials to begin.")

        with sidebar:
            show_login()
        st.stop()
    if "returning_user" in st.session_state and st.session_state.returning_user:
        with sidebar:
            st.success(f"Logged in as {st.session_state.xbrl.username}")
            st.button(
                label="Log Out",
                icon=":material/logout:",
                type="secondary",
                use_container_width=False,
                on_click=lambda: restart_everything(),
                key="logout",
            )
        if "xbrl" not in st.session_state:
            st.session_state.xbrl = XBRL()
            st.session_state.account_limit = st.session_state.xbrl.account_limit

        # list endpoints folder in the meta_endpoints directory
        if "endpoint_names" not in st.session_state:
            st.session_state.endpoint_names = [f.stem for f in (_dir / "meta_endpoints").glob("*.yml")]

        endpoint = sidebar.selectbox(
            label="API Endpoint",
            options=st.session_state.endpoint_names,
            index=9,
            key="endpoint",
            disabled=False,
            format_func=lambda x: x.upper(),
            on_change=lambda: restart_endpoint(),
            help="""Select the endpoint you would like to use.
            For more information on the endpoints,
            see the [XBRL.US API Documentation](https://xbrlus.github.io/xbrl-api/#/).""",
        )

        # get the acceptable parameters for the endpoint
        # open the yml file and get the parameters
        with Path.open(_dir / f"meta_endpoints/{st.session_state.endpoint}.yml") as f:
            st.session_state.endpoint_info = object = yaml.safe_load(f)
        # parameters_options = dict(sorted(endpoint_info.parameters.items(), key=lambda x: x[1]['type']))
        # print the name of the endpoint
        # two tabs
        main, definitions = st.tabs([f"**Build {endpoint.capitalize()} Query**", f"**Review {endpoint.capitalize()} Field Definition**"])

        # show the list of fields in the sidebar
        st.session_state.endpoint_endpoint = [
            v for k, v in st.session_state.endpoint_info["endpoints"].items() if "/search" in v and "{" not in v
        ]
        st.session_state.endpoint_parameters = [
            (k, v) for k, v in st.session_state.endpoint_info["fields"].items() if "searchable" in v and v["searchable"] == "true"
        ]
        st.session_state.endpoint_fields = [(k, v) for k, v in st.session_state.endpoint_info["fields"].items() if "type" in v]
        st.session_state.endpoint_limit = st.session_state.endpoint_endpoint[0].split("/")[1]
        st.session_state.query_params = {}

        with definitions:
            # create a dictionary of endpoint_fields based on the beginning of the field name split on "."
            all_fields = {}
            for field, values in st.session_state.endpoint_fields:
                if "." in field:
                    field_name = field.split(".")[0]
                    if field_name not in all_fields:
                        all_fields[field_name] = []
                    all_fields[field_name].append({field: values})
                # sort the fields by the first part of the field name
            all_fields = dict(sorted(all_fields.items(), key=lambda x: x[0]))
            # create a st.expander for each field
            for field, values in all_fields.items():
                with st.expander(
                    label=f"**{field.upper()}**",
                    expanded=False,
                ):
                    for item in values:
                        field_name = list(item.keys())[0]
                        field_info = item[field_name]
                        st.markdown(f"#### {field_name}:")
                        col1, col2, col3 = st.columns(3, border=False, gap="small", vertical_alignment="center")

                        # convert type with TYPE_MAPPINGS
                        if field_info["type"] in TYPE_MAPPINGS:
                            field_info["type"] = TYPE_MAPPINGS[field_info["type"]]

                        col1.badge(
                            label=field_info["type"].upper(),
                            # icon=":material/info:",
                            color="blue",
                        )
                        if field_info["searchable"] == "true":
                            col2.badge(
                                label="can be a search parameter",
                                icon=":material/search:",
                                color="green",
                            )
                        if "format" in field_info:
                            col3.badge(
                                label=f"{field_info['format'].upper()}",
                                icon=":material/data_array:",
                                color="orange",
                            )

                        st.markdown(
                            f"**Definition**: {field_info['definition'] if 'definition' in field_info else 'No Definition Provided'} "
                        )
        with main:
            with st.container():
                sidebar.badge(label=st.session_state.endpoint_endpoint[0].upper(), icon=":material/database:", color="primary")

                sidebar.multiselect(
                    label="Parameters",
                    options=st.session_state.endpoint_parameters,
                    format_func=lambda x: x[0],
                    key="parameters",
                )

                sidebar.multiselect(
                    label="Fields :red[*]",
                    options=st.session_state.endpoint_fields,
                    format_func=lambda x: x[0],
                    key="fields",
                )

                sidebar.multiselect(
                    label="Sort",
                    options=st.session_state.fields,
                    format_func=lambda x: x[0],
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

                if st.session_state.endpoint_limit:
                    # check box for limit
                    sidebar.toggle(
                        label="Download All",
                        value=False,
                        key="download_all",
                    )
                    if not st.session_state.download_all:
                        limit = sidebar.number_input(
                            label=f"**{st.session_state.endpoint_limit} limit:**",
                            value=100,
                        )
                        st.session_state.limit_param = limit
                    else:
                        st.session_state.limit_param = "all"
                        sidebar.error(
                            """This may take a long time to run. Only use this option if you are sure you want to retrieve all the data."""
                        )

            query_button_placeholder = sidebar.empty()
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
                            label=f"**{field[0]}**:",
                            options=("Ascending", "Descending"),
                            horizontal=True,
                            key=f"{field}_sort",
                        )
                        st.session_state.sort_params[field[0]] = "asc" if sort_order == "Ascending" else "desc"
                    st.markdown("---")

                for param in st.session_state.parameters:
                    st.write(f"**{param[0].capitalize()}**:")
                    st.badge(param[1]["type"].upper(), color="blue")
                    st.markdown(param[1]["definition"])
                    type = param[1]["type"]

                    if type == "boolean":
                        st.radio(
                            label=f"Input **{param[0]}**:",
                            options=("true", "false"),
                            horizontal=True,
                            key=f"{param[0]}",
                            label_visibility="collapsed",
                        )

                    else:
                        st.text_area(
                            label=f"Input **{param[0]}**:",
                            value="",
                            key=f"{param[0]}",
                            label_visibility="collapsed",
                        )
                    st.divider()

                if len(st.session_state.parameters) > 0:
                    st.session_state.query_params["parameters"] = {}
                    for param in st.session_state.parameters:
                        st.session_state.query_params["parameters"][param[0]] = st.session_state[param[0]]
                if len(st.session_state.fields) > 0:
                    st.session_state.query_params["fields"] = [field[0] for field in st.session_state.fields]
                if len(st.session_state.sort_params) > 0:
                    st.session_state.query_params["sort"] = st.session_state.sort_params
                if st.session_state.limit_param:
                    st.session_state.query_params["limit"] = st.session_state.limit_param
                if st.session_state.unique_yes:
                    st.session_state.query_params["unique"] = True
                st.session_state.query_params["endpoint"] = st.session_state.endpoint_endpoint[0]

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
                label="RUN",
                key="run_query",
                type="primary",
                icon=":material/play_arrow:",
                use_container_width=True,
                disabled=query_btn_disabled,
            )
            new_results_placeholder = st.empty()
            if st.session_state.run_query:
                try:
                    with st.spinner("Running query..."):
                        st.session_state.pop("last_query", None)
                        st.session_state.last_query = st.session_state.xbrl.query(
                            **st.session_state.query_params, as_dataframe=True, print_query=True, streamlit=True, timeout=None
                        )

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
