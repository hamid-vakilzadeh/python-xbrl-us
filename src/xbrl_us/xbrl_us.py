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
from yaml import safe_load

from .utils import Parameters

_dir = Path(__file__).resolve()


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

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
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
        self._access_token_expires_at = 0
        self._refresh_token_expires_at = 0

    @staticmethod
    def acceptable_params(method_name: str):
        """
        Get the names of the attributes that are allowed to be used for
            the given method.

        Args:
            method_name (str): The name of the API method to get the acceptable parameters for (e.g. "search_fact").

        Returns:

        """
        file_path = _dir.parent / "methods" / f"{method_name.lower()}.yml"

        with file_path.open("r") as file:
            method_features = safe_load(file)

        _attributes = {"method_name": method_name}
        for key, _value in method_features.items():
            _attributes[f"{key}"] = method_features.get(key)

        # Create the dynamic class using type()
        _class = type(method_name, (), _attributes)
        return _class()

    @staticmethod
    def methods():
        """
        Get the names of the attributes that are allowed to be used for
            the given method. A list of available methods are:

            ===================================  ==================================================
            Method                               API Endpoint
            ===================================  ==================================================
            ``assertion search``                  ``/api/v1/assertion/search``
            ``assertion validate``                ``/api/v1/assertion/validate``
            ``concept name search``               ``/api/v1/concept/{concept.local-name}/search``
            ``concept search``                    ``/api/v1/concept/search``
            ``cube search``                       ``/api/v1/cube/search``
            ``dimension search``                  ``/api/v1/dimension/search``
            ``document search``                   ``/api/v1/document/search``
            ``dts id concept label``              ``/api/v1/dts/{dts.id}/concept/{concept.local-name}/label``
            ``dts id concept name``               ``/api/v1/dts/{dts.id}/concept/{concept.local-name}``
            ``dts id concept reference``          ``/api/v1/dts/{dts.id}/concept/{concept.local-name}/reference``
            ``dts id concept search``             ``/api/v1/dts/{dts.id}/concept/search``
            ``dts id network``                    ``/api/v1/dts/{dts.id}/network``
            ``dts id network search``             ``/api/v1/dts/{dts.id}/network/search``
            ``dts search``                        ``/api/v1/dts/search``
            ``entity id``                         ``/api/v1/entity/{entity.id}``
            ``entity id report search``           ``/api/v1/entity/{entity.id}/report/search``
            ``entity report search``              ``/api/v1/entity/report/search``
            ``entity search``                     ``/api/v1/entity/search``
            ``fact id``                           ``/api/v1/fact/{fact.id}``
            ``fact search``                       ``/api/v1/fact/search``
            ``fact search oim``                   ``/api/v1/fact/oim/search``
            ``label dts id search``               ``/api/v1/label/{dts.id}/search``
            ``label search``                      ``/api/v1/label/search``
            ``network id``                        ``/api/v1/network/{network.id}``
            ``network id relationship search``    ``/api/v1/network/{network.id}/relationship/search``
            ``network relationship search``       ``/api/v1/network/relationship/search``
            ``relationship search``               ``/api/v1/relationship/search``
            ``relationship tree search``          ``/api/v1/relationship/tree/search``
            ``report fact search``                ``/api/v1/report/fact/search``
            ``report id``                         ``/api/v1/report/{report.id}``
            ``report id delete``                  ``/api/v1/report/{report.id}/delete``
            ``report id fact``                    ``/api/v1/report/{report.id}/fact/search``
            ``report search``                     ``/api/v1/report/search``
            ===================================  ==================================================

        """
        # location of all method files
        file_path = _dir.parent / "methods"

        # list all the files in the directory
        method_files = Path(file_path).glob("*.yml")

        return [file_path.stem for file_path in method_files]

    def _get_token(self, grant_type: Optional[str] = None, refresh_token=None):
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

        response = requests.request(method, url, timeout=30, **kwargs)
        return response

    @staticmethod
    def _validate_parameters(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            """
            Validate the parameters passed to the query method.

            Args:
                instance: The instance of the XBRL class.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the wrapped function.
            """
            method_name = kwargs.get("method")

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

            # get the allowed parameters, fields, limit, sort, and offset from the yaml file
            allowed_params = allowed_for_query.get("parameters", set())
            allowed_fields = allowed_for_query.get("fields", set())
            allowed_limit_fields = allowed_for_query.get("limit", set())
            allowed_sort_fields = allowed_for_query.get("sort", set())
            allowed_offset_fields = allowed_for_query.get("offset", set())

            # Validate fields
            if not fields:
                raise ValueError("fields cannot be None.")

            for field in fields:
                if not isinstance(field, str):
                    raise ValueError(f"field must be a string. {field} is {type(field)}")
                if field not in allowed_fields:
                    raise ValueError(
                        f"""Field
                        '{field}' is not allowed as a field for '{method_name}'. Allowed fields are:
                        '{allowed_fields}'.
                        """
                    )

            # Validate parameters
            if parameters:
                for param in parameters:
                    if param not in allowed_params:
                        raise ValueError(
                            f"""
                        Parameter '{param}' is not allowed for '{method_name}'. Allowed parameters are:
                        {allowed_params}.
                        """
                        )

            # Validate limit
            if limit:
                if not isinstance(limit, dict):
                    raise ValueError(f"""limit must be a dictionary not {type(limit)}. e.g. limit = {{'fact': 100}}.""")
                for key, value in limit.items():
                    if key not in allowed_limit_fields:
                        raise ValueError(f"""Limit key '{key}' is not allowed. Allowed limit keys are: {allowed_limit_fields}""")
                    if not isinstance(value, int):
                        raise ValueError(f"Limit value must be an integer. {value} is not an integer")
            else:
                warnings.warn(
                    """You have not set a limit. This will return the first 100 results by default.
                    """,
                    UserWarning,
                    stacklevel=2,
                )

            # Validate sort
            if sort:
                if not isinstance(sort, dict):
                    raise ValueError("Sort must be a dictionary")
                for key, value in sort.items():
                    if key not in allowed_sort_fields:
                        raise ValueError(f"""Sort key '{key}' is not allowed. Allowed sort keys are: {allowed_sort_fields}.""")
                    if value.lower() not in ["asc", "desc"]:
                        raise ValueError("Sort value should be 'asc' or 'desc' only.")

            elif offset:
                warnings.warn(
                    "You have set an offset but not a sort method. "
                    "When using offset, it is recommended that you set a sort method "
                    "to get reliable results.",
                    UserWarning,
                    stacklevel=2,
                )

            # Validate offset
            if offset:
                if not isinstance(offset, dict):
                    raise ValueError("Offset must be a dictionary")
                for key, value in offset.items():
                    if key not in allowed_offset_fields:
                        raise ValueError(f"""Offset key '{key}' is not allowed. Allowed offset keys are: {allowed_offset_fields}.""")
                    if not isinstance(value, int):
                        raise ValueError(f"Offset value must be an integer. {value} is not an integer.")

            return func(instance, *args, **kwargs)

        return wrapper

    @staticmethod
    def _build_query_params(
        fields: Optional[list] = None,
        parameters=None,
        limit: Optional[dict] = None,
        sort: Optional[dict] = None,
        offset: Optional[dict] = None,
    ) -> dict:
        """
        Build the query parameters for the API request in the format required by the API.

        Args:
            fields (list): The list of fields to include in the query.
            parameters (dict): The parameters for the query.
            limit (dict): The limit parameters for the query.
            sort (dict): The sort parameters for the query.
            offset (dict): The offset parameters for the query.

        Returns:
            dict: The query parameters.
        """
        query_params = {}

        if parameters:
            query_params.update(
                {
                    f"{k}": ",".join(map(str, v)) if isinstance(v, Iterable) and not isinstance(v, str) else str(v)
                    for k, v in parameters.items()
                }
            )

        # Handle sort
        if sort:
            # TODO: verify that sort, limit, and offset work together for the same field
            # check if the sort field is in the fields list
            for field, direction in sort.items():
                # if the field is not in the fields list add the field name followed by .sort(value)
                if field not in fields:
                    fields.append(f"{field}.sort({direction.upper()})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .sort(value)
                else:
                    fields.remove(field)
                    fields.append(f"{field}.sort({direction.upper()})")

        # Handle limit
        if limit:
            # check if the limit field is in the fields list
            for field, value in limit.items():
                # if the field is not in the fields list add the field name followed by .limit(value)
                if field not in fields:
                    fields.append(f"{field}.limit({value})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .limit(value)
                else:
                    fields.remove(field)
                    fields.append(f"{field}.limit({value})")
        else:
            fields.append("fact.limit(100)")

        # Handle offset
        if offset:
            # check if the offset field is in the fields list
            for field in offset.items():
                # if the field is not in the fields list add the field name followed by .offset(value)
                if field not in fields:
                    fields.append(f"{field}.offset({offset})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .offset(value)
                else:
                    fields.remove(field)
                    fields.append(f"{field}.offset({offset})")

        query_params["fields"] = ",".join(fields)

        return query_params

    @staticmethod
    def _convert_params_to_dict_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            """
            Convert the Parameters object to a dictionary before building the query.

            Args:
                self: The instance of the XBRL class.
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
            return func(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def _get_method_url(method_name: str, parameters) -> str:
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
            values = {key: parameters[key] for key in keys if key in parameters}

            # get the required parameters for this method
            for key, value in values.items():
                placeholder = "{" + key + "}"
                url = url.replace(placeholder, str(value))
        return f"https://api.xbrl.us{url}"

    @_convert_params_to_dict_decorator
    @_validate_parameters
    def query(
        self,
        method: str,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[dict] = None,
        sort: Optional[dict] = None,
        offset: Optional[dict] = None,
        as_dataframe: bool = False,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            method (str): The name of the method to query.
            fields (list): The fields query parameter establishes the details of the data to return for the specific query.
            parameters (dict | Parameters): The parameters for the query.
            limit (dict): A limit restricts the number of results returned by the query.
                The limit attribute can only be added to an object type and not a property.
                For example, to limit the number of facts in a query, {"fact": 10}.
            sort (dict): Any returned value can be sorted in ascending or descending order,
                using ``ASC`` or ``DESC`` (i.e. {"report.document-type": "DESC"}.
                Multiple sort criteria can be defined and the sort sequence is determined by
                the order of the items in the dictionary.
            offset: This attribute enables targeting a return to a specific starting point in a
                query return sequence (i.e. {"report": 100}. To work reliably,
                at least one sorted property should be included in the returned fields.
            as_dataframe (bool=False): Whether to return the results as a DataFrame or json.

        Returns:
            dict | DataFrame: The results of the query.
        """
        response = self._make_request(
            method="get",
            url=self._get_method_url(method, parameters),
            params=self._build_query_params(
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                offset=offset,
            ),
        )

        if as_dataframe:
            return DataFrame.from_dict(response.json()["data"])
        else:
            return response.json()["data"]
