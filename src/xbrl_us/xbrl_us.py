import asyncio
import logging
import re
import time
import warnings
from collections.abc import Iterable
from functools import wraps
from pathlib import Path
from typing import Optional
from typing import Union

import aiohttp
import nest_asyncio
import requests
from pandas import DataFrame
from retry import retry
from tqdm import tqdm

from .types import AssertionEndpoint
from .types import AssertionFields
from .types import AssertionParameters
from .types import AssertionSorts
from .types import ConceptEndpoint
from .types import ConceptFields
from .types import ConceptParameters
from .types import ConceptSorts
from .types import CubeEndpoint
from .types import CubeFields
from .types import CubeParameters
from .types import CubeSorts
from .types import DocumentEndpoint
from .types import DocumentFields
from .types import DocumentParameters
from .types import DocumentSorts
from .types import DtsConceptEndpoint
from .types import DtsConceptFields
from .types import DtsConceptParameters
from .types import DtsConceptSorts
from .types import DtsEndpoint
from .types import DtsFields
from .types import DtsNetworkEndpoint
from .types import DtsNetworkFields
from .types import DtsNetworkParameters
from .types import DtsNetworkSorts
from .types import DtsParameters
from .types import DtsSorts
from .types import EntityEndpoint
from .types import EntityFields
from .types import EntityParameters
from .types import EntityReportEndpoint
from .types import EntityReportFields
from .types import EntityReportParameters
from .types import EntityReportSorts
from .types import EntitySorts
from .types import FactEndpoint
from .types import FactFields
from .types import FactParameters
from .types import FactSorts
from .types import LabelEndpoint
from .types import LabelFields
from .types import LabelParameters
from .types import LabelSorts
from .types import NetworkEndpoint
from .types import NetworkFields
from .types import NetworkParameters
from .types import NetworkRelationshipEndpoint
from .types import NetworkRelationshipFields
from .types import NetworkRelationshipParameters
from .types import NetworkRelationshipSorts
from .types import NetworkSorts
from .types import RelationshipEndpoint
from .types import RelationshipFields
from .types import RelationshipParameters
from .types import RelationshipSorts
from .types import ReportEndpoint
from .types import ReportFactEndpoint
from .types import ReportFactFields
from .types import ReportFactParameters
from .types import ReportFactSorts
from .types import ReportFields
from .types import ReportNetworkEndpoint
from .types import ReportNetworkFields
from .types import ReportNetworkParameters
from .types import ReportNetworkSorts
from .types import ReportParameters
from .types import ReportSorts
from .types import UniversalFieldMap
from .utils import exceptions

_dir = Path(__file__).resolve()

# Get the home directory path as a Path object
_home_directory = Path.home()

# Join the home directory path with the file name to get the full file path
user_info_path = _home_directory / ".xbrl-us"


# logging.basicConfig()
class OneTimeWarningFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.msgs = set()

    def filter(self, record):
        if record.msg not in self.msgs:
            self.msgs.add(record.msg)
            return True
        return False


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.addFilter(OneTimeWarningFilter())
logger.addHandler(handler)
logger.setLevel(logging.WARNING)


# Apply patch when the module is imported
try:
    nest_asyncio.apply()
except Exception as e:
    logger.warning(f"An exception occurred: {e}")  # Or debug/info/error as appropriate


def _remove_special_fields(fields):
    # Define the patterns to be removed
    patterns = [r"(.+)\.(sort\((.+)\))?$", r"(.+)\.(limit\((\d+)\))?$", r"(.+)\.(offset\((\d+)\))?$"]

    # For each field, check if it matches any of the patterns. If it does, remove it.
    for field in fields[:]:  # iterate over a slice copy of the list to safely modify it during iteration
        if any(re.match(pattern, field, re.IGNORECASE) for pattern in patterns):
            fields.remove(field)

    return fields


def _validate_parameters():
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            """
            Validate the parameters passed to the query method including fields, parameters, sort, limit, and offset.
            This is a decorator for the ``_build_query_params`` method in XBRL class.

            Args:
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the wrapped function.
            """
            endpoint_name = kwargs.get("endpoint", None)
            if not endpoint_name:
                raise ValueError("No endpoint name provided. Please provide an endpoint name.")

            if not isinstance(endpoint_name, str):
                raise TypeError(f"{endpoint_name} is not a string. Please provide a string.")

            # get the parameters, fields, limit, sort, and offset from kwargs that the user passed in
            parameters = kwargs.get("parameters")
            fields = kwargs.get("fields")
            limit = kwargs.get("limit")
            sort = kwargs.get("sort")
            offset = kwargs.get("offset")
            kwargs.get("print_query")

            if fields:
                fields = [UniversalFieldMap.to_original(item) for item in fields]
            if parameters:
                parameters = {UniversalFieldMap.to_original(key): value for key, value in parameters.items()} if parameters else {}
            if sort:
                sort = {UniversalFieldMap.to_original(key): value for key, value in sort.items()} if sort else {}

            # get the allowed parameters, fields, limit, sort, and offset from the yaml file
            allowed_limit_fields = endpoint_name.lower().replace("/", " ").strip().split(" ")[0]
            allowed_offset_fields = allowed_limit_fields

            # Validate fields
            if not fields:
                raise ValueError("No fields provided. Please provide at least one field.")

            # clear the conditions from the previous query
            # this could happen when the limit is greater than account limit or
            # when the user passes in a field with a condition
            fields = _remove_special_fields(fields)
            for field in fields:
                if not isinstance(field, str):
                    raise TypeError(f"{field} is not a string. Please provide a string.")

            # Validate limit
            if limit:
                # if not dict or an int, raise an error
                if not isinstance(limit, int):
                    raise exceptions.XBRLInvalidTypeError(key=limit, expected_type=int, received_type=type(limit))

            else:
                logger.warning(
                    "No limit set: this will automatically limit the number of results to your account limit."
                    " if you want more results, set the limit.",
                    stacklevel=2,
                )

            # Validate sort
            if sort:
                if not isinstance(sort, dict):
                    raise ValueError("Sort must be a dictionary")
                sort = {_remove_special_fields(key): value for key, value in sort.items()}
                for _key, value in sort.items():
                    if value.lower() not in ["asc", "desc"]:
                        raise exceptions.XBRLInvalidValueError(key=value, param="sort", expected_value=["asc", "desc"])
            else:
                logger.warning(
                    "No sort field: It is recommended to sort by a field for reliable results.",
                    stacklevel=2,
                )

            # Validate offset
            if offset:
                if not isinstance(offset, int):
                    raise TypeError(f"{offset} is not an int. Please provide an int.")

            limit_field = None
            offset_field = None

            if allowed_limit_fields:
                limit_field = allowed_limit_fields
            if allowed_offset_fields:
                offset_field = allowed_offset_fields

            return func(
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                offset=offset,
                limit_field=limit_field,
                offset_field=offset_field,
                unique=kwargs.get("unique"),
            )

        return wrapper

    return decorator


def _type_check_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Check if the parameters passed to the query method are in dictionary format.
            This is a decorator for the ``query`` method in XBRL class.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the wrapped function.
            """
            if kwargs.get("method"):
                raise KeyError("`method` is no longer supported. Please use `endpoint` instead.")

            if not kwargs.get("endpoint"):
                raise ValueError("No endpoint name provided. Please provide an endpoint name.")

            parameters = kwargs.get("parameters")
            if parameters and not isinstance(parameters, dict):
                raise ValueError(f"Parameters must be a dict or Parameters object. " f"Got {type(parameters)} instead.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@_validate_parameters()
def _build_query_params(
    fields: Optional[list] = None,
    parameters: Optional[dict] = None,
    limit: Optional[int] = None,
    sort: Optional[dict] = None,
    offset: Optional[int] = 0,
    limit_field: Optional[str] = None,
    offset_field: Optional[str] = None,
    unique: Optional[bool] = False,
) -> dict:
    """
    Build the query parameters for the API request in the format required by the API.

    Args:
        fields (list): The list of fields to include in the query.
        parameters (dict): The parameters for the query.
        limit (dict): The limit parameters for the query.
        sort (dict): The sort parameters for the query.
        offset (dict): dynamically set if needed
        limit_field (str): The limit field accepted for the chosen method.
        offset_field (str): The offset field accepted for the chosen method (which is usually the same as the
            ``limit_filed``).

    Returns:
        dict: The query parameters that will be submitted to the API.
    """
    query_params = {}
    fields_copy = fields[:]
    if parameters:
        # convert the parameters to a string and add it to the query_params
        query_params.update(
            {f"{k}": ",".join(map(str, v)) if isinstance(v, Iterable) and not isinstance(v, str) else str(v) for k, v in parameters.items()}
        )

    # Handle sort
    if sort:
        sort_copy = dict(sort)

        # check if the sort field is in the fields list
        for field, direction in sort_copy.items():
            # name the field name followed by .sort(value)
            sorted_arg = f"{field}.sort({direction.upper()})"
            if field in fields_copy:
                # if the field is in the fields list, remove the field
                field_index = fields_copy.index(field)
                fields_copy.remove(field)
                fields_copy.insert(field_index, sorted_arg)
            else:
                fields_copy.append(sorted_arg)

    # Handle limit
    if limit:
        if limit_field is not None:
            # name and add the field name followed by .limit(value)
            limit_arg = f"{limit_field}.limit({limit})"
            if limit_field in fields_copy:
                # if the field is in the fields list, remove the field
                fields_copy.remove(limit_field)
            fields_copy.append(limit_arg)

    # Handle offset
    if offset:
        if offset_field is not None:
            # name and add the field name followed by .offset(value)
            offset_arg = f"{offset_field}.offset({offset})"
            if offset_field in fields_copy:
                fields_copy.remove(offset_field)
            fields_copy.append(offset_arg)

    query_params["fields"] = ",".join(fields_copy)
    # Handle unique
    if unique:
        query_params["unique"] = "true"
    return query_params


class XBRL:
    """
    XBRL US API client. Initializes an instance of XBRL authorized connection.

    Args:
        client_id (str): Unique identifier agreed upon by XBRL US and the 3rd party client.
        client_secret (str): Base64 key used to authenticate the 3rd party client.
        username (str): Unique identifier for a given user.
        password (str): Password used to authenticate the 3rd party user.
        grant_type (str): Used to identify which credentials the authorization server needs to check

            * client_credentials - Requires a client_id and client_secret only
            * password - Requires a username and password as well as client_id and client_secret
            * default - "password"
    """

    _query_exceptions = (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ReadTimeout)

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        grant_type: str = "password",
        store: Optional[str] = "n",
    ):
        self._url = "https://api.xbrl.us/oauth2/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.access_token = None
        self.refresh_token = None
        self.account_limit = None
        self._access_token_expires_at = 0
        self._refresh_token_expires_at = 0
        self._ensure_access_token(store=store)
        # If the class was initiated without any arguments, try finding the user info file
        if not (client_id and client_secret and username and password):
            self._get_user()

    def _get_token(self, grant_type: Optional[str] = None, refresh_token=None, **kwargs):
        """
        Retrieves an access token from the token URL.

        Args:
            grant_type (str): The grant type (default: "password").
            refresh_token (str): The refresh token (default: None).
        """
        grant_type = self.grant_type or grant_type
        payload = {"grant_type": grant_type, "client_id": self.client_id, "client_secret": self.client_secret, "platform": "pc"}

        if grant_type == "password":
            payload.update(
                {
                    "username": self.username,
                    "password": self.password,
                }
            )
        elif grant_type == "refresh_token":
            payload.update({"refresh_token": refresh_token})

        response = requests.post(self._url, data=payload, timeout=5)

        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info["access_token"]
            self.refresh_token = token_info["refresh_token"]
            self._access_token_expires_at = time.time() + token_info["expires_in"]
            self._refresh_token_expires_at = time.time() + token_info["refresh_token_expires_in"]
            if not user_info_path.exists():
                store = kwargs.get("store", None)
                if store is None:
                    store = input("Do you want to store your credentials for future use on this computer? (y/n): ")
                if store.lower() == "y":
                    self._set_user()
        else:
            raise ValueError(f"Unable to retrieve token: {response.json()}. Please check your credentials.")

    def _is_access_token_expired(self):
        return time.time() >= self._access_token_expires_at

    def _is_refresh_token_expired(self):
        return time.time() >= self._refresh_token_expires_at

    def _ensure_access_token(self, **kwargs):
        if not self.access_token or self._is_access_token_expired():
            if self.refresh_token and not self._is_refresh_token_expired():
                self._get_token(grant_type="password", refresh_token=self.refresh_token, **kwargs)
            else:
                self._get_token(**kwargs)
        if self.account_limit is None:
            self._get_account_limit()

    @retry(exceptions=_query_exceptions, tries=3, delay=2, backoff=2, logger=None)
    def _make_request(self, method, url, **kwargs) -> requests.Response:
        """
        Makes an HTTP request with the provided method, URL, and additional arguments.

        Args:
            method (str): The HTTP method for the request.
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to be passed to the requests' library.

        Returns:
            requests.Response: The response object.
        """
        self._ensure_access_token()

        headers = kwargs.get("headers", {})
        headers.update({"Authorization": f"Bearer {self.access_token}"})
        kwargs["headers"] = headers
        if kwargs.get("print_query"):
            print(f"Query Endpoint:{url}")
            print(f"Query Parameters: {kwargs.get('params')}")

        # Remove the print_query argument from kwargs
        kwargs.pop("print_query", None)

        response = requests.request(method, url, **kwargs)
        if response.status_code == 200:
            if "error" not in response.json():
                return response
            else:
                if "user limit amount" in response.text:
                    return response
                else:
                    raise ValueError(
                        f"Unable to retrieve data! {response.json()['error']}: {response.json()['error_description']}"
                    ) from None

        elif response.status_code == 503:
            raise f"Error {response.status_code}: {response.text}"
        elif response.status_code == 404:
            raise ValueError(f"Error {response.status_code}: {response.json()['error_description']}") from None
        else:
            raise ValueError(f"Error {response.status_code}: {response.text}") from None

    def _get_account_limit(
        self,
    ):
        # Query the API with a limit of more than 5000.
        params = "fields=fact.value,fact.limit(5001)"
        url = "https://api.xbrl.us/api/v1/fact/search"

        response = requests.get(url=url, params=params, headers={"Authorization": f"Bearer {self.access_token}"}, timeout=5)

        # Extract the limit from the response message.
        match = re.search(r"user limit amount is (\d+)", response.text)
        if match:
            self.account_limit = int(match.group(1))
        else:
            raise f"Error: {response.status_code}"

    def _set_user(self):
        # Write info file
        with user_info_path.open("w") as file:
            file.write("\n".join([self.username, self.password, self.client_id, self.client_secret]))

        print("Remember me enabled.")

    def _get_user(self):
        try:
            with user_info_path.open("r") as file:
                lines = file.readlines()

            self.username = lines[0].strip()  # set username
            self.password = lines[1].strip()  # set password
            self.client_id = lines[2].strip()  # set client id
            self.client_secret = lines[3].strip()  # set client secret

        except FileNotFoundError:
            raise FileNotFoundError("Credentials file not found. Please initialize the client with your credentials.") from None
        except Exception as e:
            raise ValueError("Error reading credentials from file:", str(e)) from None

    def _get_endpoints_info(self, force_refresh=False):
        """
        Get the endpoints from Meta API and cache them to meta/endpoints.yml.
        Additionally caches each endpoint's metadata and generates type definitions.
        Only fetches from API if cache is older than 24h or force_refresh=True.

        Args:
            force_refresh (bool): If True, force a refresh of the cache regardless of age

        Returns:
            dict: The endpoints metadata
        """
        from datetime import datetime
        from datetime import timedelta
        from datetime import timezone

        import yaml

        from .utils.generator import generate_all_types

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Create required directories
        meta_dir = Path("meta")
        meta_dir.mkdir(exist_ok=True)

        methods_dir = Path(meta_dir, "meta_endpoints")
        methods_dir.mkdir(exist_ok=True)

        types_dir = Path("models", "types")
        types_dir.mkdir(exist_ok=True, parents=True)

        # Create necessary __init__.py files
        for dir_path in [Path("models"), types_dir]:
            init_file = Path(dir_path, "__init__.py")
            if not init_file.exists():
                init_file.touch()

        cache_file = Path(meta_dir, "endpoints.yml")

        # Check if we should use cached data
        if not force_refresh and cache_file.exists():
            cache_stat = cache_file.stat()
            cache_age = datetime.now(tz=timezone.utc) - datetime.fromtimestamp(cache_stat.st_mtime, tz=timezone.utc)

            if cache_age < timedelta(hours=24):
                logger.info("Using cached endpoints data (age: %s hours)", round(cache_age.total_seconds() / 3600, 1))
                with cache_file.open("r") as f:
                    return yaml.safe_load(f)

        # Fetch fresh data from API
        logger.info("Fetching fresh endpoints data from API...")
        self._ensure_access_token()
        response = requests.get("https://api.xbrl.us/api/v1/meta", headers={"Authorization": f"Bearer {self.access_token}"}, timeout=5)

        if response.status_code != 200:
            raise exceptions.XBRLError(f"Failed to fetch Meta endpoints: {response.text}")

        # Convert to YAML and save main endpoints file
        endpoints = response.json()
        logger.info("Found %d endpoints", len(endpoints))

        with cache_file.open("w") as f:
            yaml.dump(endpoints, f, sort_keys=False)

        # Dictionary to store all endpoint metadata
        all_endpoint_metadata = {}

        logger.info("Fetching metadata for each endpoint...")
        # Fetch and cache metadata for each endpoint
        with tqdm(total=len(endpoints), desc="Processing endpoints", unit="endpoint") as pbar:
            for endpoint_name, endpoint_data in endpoints.items():
                if "link" not in endpoint_data:
                    logger.warning("Skipping %s - no link found", endpoint_name)
                    pbar.update(1)
                    continue

                # Get metadata for this endpoint
                try:
                    response = requests.get(endpoint_data["link"], headers={"Authorization": f"Bearer {self.access_token}"}, timeout=5)

                    if response.status_code != 200:
                        logger.warning("Failed to fetch metadata for %s: %s", endpoint_name, response.text)
                        pbar.update(1)
                        continue

                    endpoint_meta = response.json()
                    all_endpoint_metadata[endpoint_name] = endpoint_meta

                    # Cache the metadata
                    filename = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", " ")
                    if not filename.endswith(".yml"):
                        filename += ".yml"

                    method_file = methods_dir / filename
                    with method_file.open("w") as f:
                        yaml.dump(endpoint_meta, f, sort_keys=False)

                except requests.exceptions.RequestException as e:
                    logger.error("Error fetching metadata for %s: %s", endpoint_name, str(e))

                pbar.update(1)

        # Generate all type definitions
        logger.info("Generating type definitions...")
        generated_files = generate_all_types(all_endpoint_metadata)

        # Write types files
        types_file = types_dir / "endpoint_types.py"
        types_file.write_text(generated_files["endpoint_types.py"])

        init_file = types_dir / "__init__.py"
        init_file.write_text(generated_files["__init__.py"])

        logger.info("Endpoints metadata and type definitions generated successfully")

    @_type_check_decorator()
    def query(
        self,
        endpoint: str,
        fields: Optional[list] = None,
        parameters: Optional[dict] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[dict] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            endpoint (str): The name of the endpoint to query.
            fields (list): The fields query parameter establishes the details of the data to return for the specific query.
            parameters (Optional[dict | Parameters]): The search parameters for the query.
            limit (Optional[Union[int, "all"]]): A limit restricts the number of results returned by the query.
                For example, in a *"fact search"* ``limit=10`` would return 10 observations.
                You can also use ``limit="all"`` to return all results (which is not recommended unless
                you know what you are doing!). The default is *None* which returns one response with
                upto your account limit. For example, if your account limit is 5000, then the default
                will return the smallest of 5000 or the number of results.
            sort (Optional[dict]): Any returned value can be sorted in ascending or descending order,
                using *ASC* or *DESC* (i.e. ``{"report.document-type": "DESC"}``.
                Multiple sort criteria can be defined and the sort sequence is determined by
                the order of the items in the dictionary.
            unique (Optional[bool]=False): If *True* returns only unique values. Default is *False*.
            as_dataframe (Optional[bool]=False): If *True* returns the results as a *DataFrame* else returns the data
                as *json*. The default is *False* which returns the results in *json* format
            print_query (bool=False): Whether to print the query text.
            timeout (int=5): The number of seconds to wait for a response from the server. Defaults to 5 seconds.
                If *None* will wait indefinitely.


        Returns:
            json | DataFrame: The results of the query.
        """

        endpoint_url = f"https://api.xbrl.us/api/v1{endpoint}?"

        # if limit is all
        if limit == "all":
            # arbitrary large number
            limit = 999999999

        # ensure the limit is not greater than the account limit
        chunk_limit = min(limit, self.account_limit) if limit is not None else self.account_limit

        streamlit_indicator = kwargs.get("streamlit", False)
        if streamlit_indicator:
            from stqdm import stqdm

            pbar = stqdm(total=None, desc="Running Query, Please Wait", ncols=80)
        else:
            # create a progress bar
            pbar = tqdm(total=None, desc="Running Query, Please Wait", ncols=80, position=0, leave=True)

        # update the limit in the query params with the new limit
        query_params = _build_query_params(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=chunk_limit,
            sort=sort,
            unique=unique,
        )

        try:
            response = self._make_request(
                method="get",
                url=endpoint_url,
                params=query_params,
                timeout=timeout,
                print_query=print_query,
            )
        except Exception as e:
            raise e

        response_data = response.json()

        if response.status_code != 200:
            raise response_data["message"]
        elif "data" not in response_data:
            warnings.warn("No data returned from the query.", UserWarning, stacklevel=2)
            return response_data

        data = response_data["data"]

        # update the progress bar
        pbar.update(len(data))

        if limit is None:
            # Return the items from the first response if no user limit is provided
            if as_dataframe:
                return DataFrame.from_dict(data)
            else:
                return data
        elif chunk_limit > len(data):
            # Return the items from the first response if the user limit is greater than the number of items
            if as_dataframe:
                return DataFrame.from_dict(data)
            else:
                return data

        else:
            remaining_limit = limit - len(data)

        # To store all the items from the API response
        all_data = data
        offset = len(data)
        del data, response_data, response

        while remaining_limit > 0:
            # Determine the limit for the current request
            try:
                current_limit = min(chunk_limit, remaining_limit)
                query_params = _build_query_params(
                    endpoint=endpoint,
                    fields=fields,
                    parameters=parameters,
                    limit=current_limit,
                    sort=sort,
                    offset=offset,
                    unique=unique,
                )

                response = self._make_request(
                    method="get",
                    url=endpoint_url,
                    params=query_params,
                    timeout=timeout,
                    print_query=print_query,
                )

                response_data = response.json()
                data = response_data["data"]

                # Add the items to the overall collection
                all_data.extend(data)

                # Decrease the remaining limit by the number of items received
                remaining_limit -= len(data)

                # update the progress bar
                pbar.update(len(data))

                if len(data) < current_limit:
                    # If the number of items received is less than the current limit,
                    # it means we have reached the end
                    # of available items, so we can break out of the loop.
                    break

                # Update the offset for the next request
                offset += len(data)

            except requests.exceptions.ReadTimeout as e:
                raise exceptions.XBRLTimeOutError(e) from e

        if as_dataframe:
            return DataFrame.from_dict(all_data)
        else:
            return all_data

    @_type_check_decorator()
    def aquery(
        self,
        endpoint: str,
        fields: Optional[list] = None,
        parameters: Optional[dict] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[dict] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """Asynchronous version of the query method"""
        endpoint_url = f"https://api.xbrl.us/api/v1{endpoint}?"

        # if limit is all
        if limit == "all":
            # arbitrary large number
            limit = 999999999

        remaining_limit = limit
        all_data = []
        offset = len(all_data)

        async def execute_remaining_queries():
            nonlocal all_data, remaining_limit, offset
            self._ensure_access_token()
            headers = {"Authorization": f"Bearer {self.access_token}"}

            async with aiohttp.ClientSession() as session:
                tasks = []
                while remaining_limit > 0:
                    current_limit = min(self.account_limit, remaining_limit)
                    query_params = _build_query_params(
                        endpoint=endpoint,
                        fields=fields,
                        parameters=parameters,
                        limit=current_limit,
                        sort=sort,
                        offset=offset,
                        unique=unique,
                    )

                    tasks.append(session.get(url=endpoint_url, params=query_params, headers=headers, timeout=timeout))
                    remaining_limit -= current_limit
                    offset += current_limit

                with tqdm(total=len(tasks)) as pbar:
                    for task in asyncio.as_completed(tasks):
                        response_data = await task
                        all_data.append(await response_data.json())
                        pbar.update(1)

        asyncio.run(execute_remaining_queries())
        data = []
        for item in all_data:
            if "data" in item:
                data.extend(item["data"])

        if as_dataframe:
            return DataFrame.from_dict(data)
        else:
            return data

    def fact(
        self,
        endpoint: FactEndpoint,
        fields: Optional[FactFields] = None,
        parameters: Optional[FactParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[FactSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/fact/search", "/fact/{fact.id}", or "/fact/search/oim".
            fields (FactFields, required): The fields to include in the query.
            parameters (FactParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (FactSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def report(
        self,
        endpoint: ReportEndpoint,
        fields: Optional[ReportFields] = None,
        parameters: Optional[ReportParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[ReportSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/report/search" or "/report/{report.id}".
            fields (ReportFields, required): The fields to include in the query.
            parameters (ReportParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (ReportSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def assertion(
        self,
        endpoint: AssertionEndpoint,
        fields: Optional[AssertionFields] = None,
        parameters: Optional[AssertionParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[AssertionSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/assertion/search".
            fields (AssertionFields, required): The fields to include in the query.
            parameters (AssertionParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (AssertionSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def concept(
        self,
        endpoint: ConceptEndpoint,
        fields: Optional[ConceptFields] = None,
        parameters: Optional[ConceptParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[ConceptSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/concept/{concept.local-name}/search" or "/concept/search".
            fields (ConceptFields, required): The fields to include in the query.
            parameters (ConceptParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (ConceptSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def cube(
        self,
        endpoint: CubeEndpoint,
        fields: Optional[CubeFields] = None,
        parameters: Optional[CubeParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[CubeSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/cube/search".
            fields (CubeFields, required): The fields to include in the query.
            parameters (CubeParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (CubeSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def document(
        self,
        endpoint: DocumentEndpoint,
        fields: Optional[DocumentFields] = None,
        parameters: Optional[DocumentParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[DocumentSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/document/search".
            fields (DocumentFields, required): The fields to include in the query.
            parameters (DocumentParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (DocumentSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def dts_concept(
        self,
        endpoint: DtsConceptEndpoint,
        fields: Optional[DtsConceptFields] = None,
        parameters: Optional[DtsConceptParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[DtsConceptSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/dts/{dts.id}/concept/search", "/dts/{dts-id}/concept/{concept.local-name}", "/dts/{dts.id}/concept/{concept.local-name}/label", "/dts/{dts.id}/concept/{concept.local-name}/reference".
            fields (DtsConceptFields, required): The fields to include in the query.
            parameters (DtsConceptParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (DtsConceptSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def dts_network(
        self,
        endpoint: DtsNetworkEndpoint,
        fields: Optional[DtsNetworkFields] = None,
        parameters: Optional[DtsNetworkParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[DtsNetworkSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/dts/{dts.id}/network", "/dts/{dts.id}/network/search".
            fields (DtsNetworkFields, required): The fields to include in the query.
            parameters (DtsNetworkParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (DtsNetworkSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def dts(
        self,
        endpoint: DtsEndpoint,
        fields: Optional[DtsFields] = None,
        parameters: Optional[DtsParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[DtsSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/dts/search".
            fields (DtsFields, required): The fields to include in the query.
            parameters (DtsParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (DtsSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def entity_report(
        self,
        endpoint: EntityReportEndpoint,
        fields: Optional[EntityReportFields] = None,
        parameters: Optional[EntityReportParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[EntityReportSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/entity/{entity.id}/report/search" or "/entity/report/search".
            fields (EntityReportFields, required): The fields to include in the query.
            parameters (EntityReportParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (EntityReportSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def entity(
        self,
        endpoint: EntityEndpoint,
        fields: Optional[EntityFields] = None,
        parameters: Optional[EntityParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[EntitySorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/entity/{entity.id}" or "/entity/search".
            fields (EntityFields, required): The fields to include in the query.
            parameters (EntityParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (EntitySorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def label(
        self,
        endpoint: LabelEndpoint,
        fields: Optional[LabelFields] = None,
        parameters: Optional[LabelParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[LabelSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/label/search" or "/label/{label.id}/search".
            fields (LabelFields, required): The fields to include in the query.
            parameters (LabelParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (LabelSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def network_relationship(
        self,
        endpoint: NetworkRelationshipEndpoint,
        fields: Optional[NetworkRelationshipFields] = None,
        parameters: Optional[NetworkRelationshipParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[NetworkRelationshipSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/network/{network.id}/relationship/search" or "/network/relationship/search".
            fields (NetworkRelationshipFields, required): The fields to include in the query.
            parameters (NetworkRelationshipParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (NetworkRelationshipSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def network(
        self,
        endpoint: NetworkEndpoint,
        fields: Optional[NetworkFields] = None,
        parameters: Optional[NetworkParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[NetworkSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/network/{network.id}".
            fields (NetworkFields, required): The fields to include in the query.
            parameters (NetworkParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (NetworkSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def relationship(
        self,
        endpoint: RelationshipEndpoint,
        fields: Optional[RelationshipFields] = None,
        parameters: Optional[RelationshipParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[RelationshipSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/relationship/search" or "/relationship/tree/search".
            fields (RelationshipFields, required): The fields to include in the query.
            parameters (RelationshipParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (RelationshipSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def report_fact(
        self,
        endpoint: ReportFactEndpoint,
        fields: Optional[ReportFactFields] = None,
        parameters: Optional[ReportFactParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[ReportFactSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/report/{report.id}/fact/search" or "/report/fact/search".
            fields (ReportFactFields, required): The fields to include in the query.
            parameters (ReportFactParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (ReportFactSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )

    def report_network(
        self,
        endpoint: ReportNetworkEndpoint,
        fields: Optional[ReportNetworkFields] = None,
        parameters: Optional[ReportNetworkParameters] = None,
        limit: Optional[Union[int, "all"]] = None,
        sort: Optional[ReportNetworkSorts] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 100,
        async_mode: Optional[bool] = False,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """
        Args:
            endpoint (str, required): The API endpoint to query.
                Options are "/report/{report.id}/network/search" or "/report/network/search".
            fields (ReportNetworkFields, required): The fields to include in the query.
            parameters (ReportNetworkParameters, optional): The search parameters for the query.
                Default is None.
            limit (Union[int, "all"], optional): The maximum number of results to return.
                If None, the account limit is used. Default is None.
            sort (ReportNetworkSorts, optional): The sort parameters for the query.
                Example: {"report_document_type": "desc"}. Default is None.
            unique (bool, optional): If True, returns only unique values.
                Default is False.
            as_dataframe (bool, optional): If True, returns the results as a DataFrame.
                Default is False, which returns the results as JSON.
            print_query (bool, optional): If True, prints the query text.
                Default is False.
            timeout (int, optional): The number of seconds to wait for a response from the server.
                Default is 100 seconds. If None, waits indefinitely until kicked off by the server.
            async_mode (bool, optional): If True, uses the asynchronous query method.
                This can reduce the time taken for large queries. Use with caution. Default is False.
            **kwargs: Additional keyword arguments to be passed to the request.
        Returns:
            Union[dict, DataFrame]: The results of the query.
        """
        if async_mode:
            return self.aquery(
                endpoint=endpoint,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                unique=unique,
                as_dataframe=as_dataframe,
                print_query=print_query,
                timeout=timeout,
                **kwargs,
            )

        return self.query(
            endpoint=endpoint,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
            unique=unique,
            as_dataframe=as_dataframe,
            print_query=print_query,
            timeout=timeout,
            **kwargs,
        )
