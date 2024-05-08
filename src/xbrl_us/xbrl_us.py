import logging
import re
import time
import warnings
from collections.abc import Iterable
from functools import wraps
from pathlib import Path
from typing import Optional
from typing import Union

import requests
from pandas import DataFrame
from retry import retry
from tqdm import tqdm
from yaml import safe_load

from .utils import Parameters
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


def _remove_special_fields(fields):
    # Define the patterns to be removed
    patterns = [r"(.+)\.(sort\((.+)\))?$", r"(.+)\.(limit\((\d+)\))?$", r"(.+)\.(offset\((\d+)\))?$"]

    # For each field, check if it matches any of the patterns. If it does, remove it.
    for field in fields[:]:  # iterate over a slice copy of the list to safely modify it during iteration
        if any(re.match(pattern, field, re.IGNORECASE) for pattern in patterns):
            fields.remove(field)

    return fields


def _methods():
    """
    Get the names of the attributes that are allowed to be used for
        the given method.
    """
    # location of all method files
    file_path = _dir.parent / "methods"

    # list all the files in the directory
    method_files = Path(file_path).glob("*.yml")

    return [file_path.stem for file_path in method_files]


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
            method_name = kwargs.get("method")

            if not method_name:
                raise exceptions.XBRLMissingValueError(param="method", expected_value=_methods())
            elif method_name not in _methods():
                raise exceptions.XBRLInvalidValueError(key=method_name, param="method", expected_value=_methods())

            elif not isinstance(method_name, str):
                raise exceptions.XBRLInvalidTypeError(key=method_name, received_type=type(method_name), expected_type=str)

            # load the yaml file that has allowed parameters for the method
            file_path = _dir.parent / "methods" / f"{method_name.lower()}.yml"

            with file_path.open("r") as file:
                allowed_for_query = safe_load(file)

            # get the parameters, fields, limit, sort, and offset from kwargs that the user passed in
            parameters = kwargs.get("parameters")
            fields = kwargs.get("fields")
            limit = kwargs.get("limit")
            sort = kwargs.get("sort")
            offset = kwargs.get("offset")
            kwargs.get("print_query")

            # get the allowed parameters, fields, limit, sort, and offset from the yaml file
            allowed_params = allowed_for_query.get("parameters", set())
            allowed_fields = allowed_for_query.get("fields", set())
            allowed_limit_fields = allowed_for_query.get("limit", set())
            allowed_sort_fields = [field for field in allowed_fields if "*" not in field]
            allowed_offset_fields = allowed_limit_fields

            # Validate fields
            if not fields:
                raise exceptions.XBRLMissingValueError(param="fields", expected_value=allowed_fields)

            # clear the conditions from the previous query
            # this could happen when the limit is greater than account limit or
            # when the user passes in a field with a condition
            fields = _remove_special_fields(fields)
            for field in fields:
                if not isinstance(field, str):
                    raise exceptions.XBRLInvalidTypeError(key=field, expected_type=str, received_type=type(field))

                if field not in allowed_fields:
                    raise exceptions.XBRLInvalidValueError(key=field, param="fields", expected_value=allowed_fields, method=method_name)

            # Validate parameters
            if parameters:
                for param in parameters:
                    if param not in allowed_params:
                        raise exceptions.XBRLInvalidValueError(
                            key=param, param="parameters", expected_value=allowed_params, method=method_name
                        )

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
                for key, value in sort.items():
                    if key not in allowed_sort_fields:
                        raise exceptions.XBRLInvalidValueError(
                            key=key, param="sort", expected_value=allowed_sort_fields, method=method_name
                        )
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
                    raise exceptions.XBRLInvalidTypeError(key=offset, expected_type=int, received_type=type(offset))

            limit_field = None
            offset_field = None

            if allowed_limit_fields:
                limit_field = next(iter(allowed_limit_fields), None)
            if allowed_offset_fields:
                offset_field = next(iter(allowed_offset_fields), None)

            return func(
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                offset=offset,
                limit_field=limit_field,
                offset_field=offset_field,
            )

        return wrapper

    return decorator


def _convert_params_to_dict_decorator():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Convert the Parameters object to a dictionary before building the query.
            This is a decorator for the ``query`` method in XBRL class.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the wrapped function.
            """
            parameters = kwargs.get("parameters")
            if isinstance(parameters, Parameters):
                kwargs["parameters"] = parameters.get_parameters_dict()
            elif parameters and not isinstance(parameters, dict):
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

        # If the class was initiated without any arguments, try finding the user info file
        if not (client_id and client_secret and username and password):
            self._get_user()

    @staticmethod
    def methods():
        """
        Get the names of the methods that are allowed to be used for
            as a ``method`` name. A list of available methods along with
            their corresponding API endpoints is shown below.

            ===================================  ==================================================
            Method                               API Endpoint
            ===================================  ==================================================
            ``assertion search``                  */api/v1/assertion/search*
            ``concept name search``               */api/v1/concept/{concept.local-name}/search*
            ``concept search``                    */api/v1/concept/search*
            ``cube search``                       */api/v1/cube/search*
            ``dimension search``                  */api/v1/dimension/search*
            ``document search``                   */api/v1/document/search*
            ``dts id concept label``              */api/v1/dts/{dts.id}/concept/{concept.local-name}/label*
            ``dts id concept name``               */api/v1/dts/{dts.id}/concept/{concept.local-name}*
            ``dts id concept reference``          */api/v1/dts/{dts.id}/concept/{concept.local-name}/reference*
            ``dts id concept search``             */api/v1/dts/{dts.id}/concept/search*
            ``dts id network``                    */api/v1/dts/{dts.id}/network*
            ``dts id network search``             */api/v1/dts/{dts.id}/network/search*
            ``dts search``                        */api/v1/dts/search*
            ``entity id``                         */api/v1/entity/{entity.id}*
            ``entity id report search``           */api/v1/entity/{entity.id}/report/search*
            ``entity report search``              */api/v1/entity/report/search*
            ``entity search``                     */api/v1/entity/search*
            ``fact id``                           */api/v1/fact/{fact.id}*
            ``fact search``                       */api/v1/fact/search*
            ``fact search oim``                   */api/v1/fact/oim/search*
            ``label dts id search``               */api/v1/label/{dts.id}/search*
            ``label search``                      */api/v1/label/search*
            ``network id``                        */api/v1/network/{network.id}*
            ``network id relationship search``    */api/v1/network/{network.id}/relationship/search*
            ``network relationship search``       */api/v1/network/relationship/search*
            ``relationship search``               */api/v1/relationship/search*
            ``relationship tree search``          */api/v1/relationship/tree/search*
            ``report fact search``                */api/v1/report/fact/search*
            ``report id``                         */api/v1/report/{report.id}*
            ``report id fact search``             */api/v1/report/{report.id}/fact/search*
            ``report search``                     */api/v1/report/search*
            ===================================  ==================================================

        """
        # TODO: add support for report delete, assertion validate,
        return _methods()

    @staticmethod
    def acceptable_params(method: str):
        """
        Get the names of the attributes (e.g. acceptable ``fields``, ``parameters``, ``sort``, ``limit``, etc.)
            that are allowed to be used for a given ``method``.

        Args:
            method (str): The name of the API method to get the acceptable parameters for (e.g. "fact search").

        Returns:
            A class where the attributes are the acceptable parameters for the given ``method``.

        """
        file_path = _dir.parent / "methods" / f"{method.lower()}.yml"

        with file_path.open("r") as file:
            method_features = safe_load(file)

        _attributes = {"method_name": method}
        for key, _value in method_features.items():
            _attributes[f"{key}"] = method_features.get(key)

        _attributes["sort"] = [value for value in _attributes["fields"] if "*" not in value]

        # Create the dynamic class using type()
        _class = type(method, (), _attributes)
        return _class()

    @staticmethod
    def define(parameter: str):
        """
        Get the definition of any parameter.
        Args:
            parameter:

        Returns:
            dict: The definition of the parameter with the type, description, etc.
        """
        # load definitions file
        file_path = _dir.parent / "methods" / "_definitions.yaml"

        with file_path.open("r") as file:
            definitions = safe_load(file)

        return definitions.get(parameter)

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

    def _ensure_access_token(self):
        if not self.access_token or self._is_access_token_expired():
            if self.refresh_token and not self._is_refresh_token_expired():
                self._get_token(grant_type="refresh_token", refresh_token=self.refresh_token)
            else:
                self._get_token()

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
        url: str,
        params: dict,
    ):
        # Query the API with a limit of more than 5000.
        fields = params["fields"]
        new_fields = ",".join([fields, "fact.limit(5001)"])
        params["fields"] = new_fields

        response = self._make_request(
            method="get",
            url=url,
            params=params,
        )

        # Extract the limit from the response message.
        match = re.search(r"user limit amount is (\d+)", response.text)
        if match:
            self.account_limit = int(match.group(1))
        else:
            print(f"Error: {response.status_code}")
            self.account_limit = None

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

    def _get_method_url(self, method_name: str, parameters: dict, unique: bool) -> str:
        """
        Get the URL for the specified method from the YAML file.

        Args:
            method_name (str): The name of the method.
            parameters: The parameters for the method.

        Returns:
            str: The URL for the method.
        """
        file_path = _dir.parent / "methods" / f"{method_name.lower()}.yml"

        # get the url for this method
        with file_path.open("r") as file:
            url = safe_load(file)["url"]

        # check if the link requires parameters
        keys = [key.strip("{}") for key in re.findall(r"{(.*?)}", url)]
        if len(keys) > 0:
            if not parameters:
                raise exceptions.XBRLRequiredValueError(key=keys, method=method_name)

            values = {key: parameters[key] for key in keys if key in parameters}

            # check if all required parameters are present
            if len(values) != len(keys):
                missing_keys = [key for key in keys if key not in values]
                for key in missing_keys:
                    raise exceptions.XBRLRequiredValueError(key=key, method=method_name)

            # get the required parameters for this method
            for key, value in values.items():
                placeholder = "{" + key + "}"
                url = url.replace(placeholder, str(value))
        if unique:
            return f"https://api.xbrl.us{url}?unique"

        return f"https://api.xbrl.us{url}?"

    @_convert_params_to_dict_decorator()
    def query(
        self,
        method: str,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[int] = None,
        sort: Optional[dict] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = 5,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            method (str): The name of the method to query.
            fields (list): The fields query parameter establishes the details of the data to return for the specific query.
            parameters (Optional[dict | Parameters]): The search parameters for the query.
            limit (Optional[int]): A limit restricts the number of results returned by the query.
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

        method_url = self._get_method_url(method_name=method, parameters=parameters, unique=unique)
        # if limit is all
        if limit == "all":
            # arbitrary large number
            limit = 999999999

        query_params = _build_query_params(method=method, fields=fields, parameters=parameters, sort=sort, limit=100)

        # check if the account limit has been set
        if not self.account_limit:
            self._get_account_limit(url=method_url, params=query_params)

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
            method=method,
            fields=fields,
            parameters=parameters,
            limit=chunk_limit,
            sort=sort,
        )

        if print_query:
            print(f"\n{query_params}")

        try:
            response = self._make_request(
                method="get",
                url=method_url,
                params=query_params,
                timeout=timeout,
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
                    method=method,
                    fields=fields,
                    parameters=parameters,
                    limit=current_limit,
                    sort=sort,
                    offset=offset,
                )

                response = self._make_request(
                    method="get",
                    url=method_url,
                    params=query_params,
                    timeout=timeout,
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
