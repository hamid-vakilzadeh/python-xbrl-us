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
from yaml import safe_load

from .utils import Parameters
from .utils import exceptions

logging.basicConfig()

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

    _query_exceptions = (requests.exceptions.ConnectionError, requests.exceptions.Timeout, requests.exceptions.ReadTimeout)

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

        _attributes["sort"] = [value for value in _attributes["fields"] if "*" not in value]

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

    @retry(exceptions=_query_exceptions, tries=5, delay=2, backoff=2)
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

        response = requests.request(method, url, timeout=60, **kwargs)
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

            if not method_name:
                raise exceptions.XBRLMissingValueError(param="method", expected_value=instance.methods())
            elif method_name not in instance.methods():
                raise exceptions.XBRLInvalidValueError(key=method_name, param="method", expected_value=instance.methods())

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
            allowed_params = list(allowed_for_query.get("parameters", set()).keys())
            allowed_fields = allowed_for_query.get("fields", set())
            allowed_limit_fields = allowed_for_query.get("limit", set())
            allowed_sort_fields = [field for field in allowed_fields if "*" not in field]
            allowed_offset_fields = allowed_limit_fields

            # Validate fields
            if not fields:
                raise exceptions.XBRLMissingValueError(param="fields", expected_value=allowed_fields)

            for field in fields:
                if not isinstance(field, str):
                    raise exceptions.XBRLInvalidTypeError(key=field, expected_type=str, received_type=type(field))

                # handle validation if the user passes in a field with a sort
                pattern = r"(.+)\.(sort\((asc|desc)\))?$"
                field_name = (
                    re.match(pattern, field, flags=re.IGNORECASE).group(1) if re.match(pattern, field, flags=re.IGNORECASE) else field
                )

                if field_name not in allowed_fields:
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
                # if limit is all
                if limit == "all" and not sort:
                    warnings.warn(
                        "getting all the data without a sort is not recommended; please pass a sort field",
                        UserWarning,
                        stacklevel=2,
                    )
                    limit = 999999999
                # if not dict or an int, raise an error
                elif not isinstance(limit, int):
                    raise exceptions.XBRLInvalidTypeError(key=limit, expected_type=int, received_type=type(limit))

            else:
                warnings.warn(
                    "You have not set a limit; returning the first page only.",
                    UserWarning,
                    stacklevel=2,
                )

            # Validate sort
            if sort:
                if not isinstance(sort, dict):
                    raise ValueError("Sort must be a dictionary")
                for key, value in sort.items():
                    if key not in allowed_sort_fields:
                        raise exceptions.XBRLInvalidValueError(
                            key=key, param="sort", expected_value=allowed_sort_fields, method=method_name
                        )
                    if value.lower() not in ["asc", "desc"]:
                        raise exceptions.XBRLInvalidValueError(key=value, param="sort", expected_value=["asc", "desc"])

            # Validate offset
            if offset:
                if not isinstance(offset, int):
                    raise exceptions.XBRLInvalidTypeError(key=offset, expected_type=int, received_type=type(offset))

            limit_field = next(iter(allowed_limit_fields))
            offset_field = next(iter(allowed_offset_fields))

            return func(
                instance,
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                offset=offset,
                limit_field=limit_field,
                offset_field=offset_field,
            )

        return wrapper

    @staticmethod
    @_validate_parameters
    def _build_query_params(
        fields: Optional[list] = None,
        parameters: Optional[dict] = None,
        limit: Optional[int] = None,
        sort: Optional[dict] = None,
        offset: Optional[int] = 0,
        limit_field: Optional[str] = None,
        offset_field: Optional[str] = None,
        **kwargs,
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
            # check if the sort field is in the fields list
            for field, direction in sort.items():
                # if the field is not in the fields list add the field name followed by .sort(value)
                sorted_value = f"{field}.sort({direction.upper()})"
                if sorted_value not in fields:
                    if field not in fields:
                        fields.append(sorted_value)
                        warnings.warn(
                            f"Sort field '{field}' is not in the fields list. Adding '{field}' to the fields list.",
                            UserWarning,
                            stacklevel=2,
                        )
                    # if the field is in the fields list, remove the field
                    else:
                        fields.remove(field)
                        fields.append(sorted_value)

        # Handle limit
        if limit:
            # check if the limit field is in the fields list
            fields[:] = [s for s in fields if not (s.startswith(f"{limit_field}.limit") and s[len(f"{limit_field}.limit") :].isdigit())]

            # name and add the field name followed by .limit(value)
            limit_arg = f"{limit_field}.limit({limit})"
            if limit_field not in fields:
                fields.append(limit_arg)
                logging.info(f"Adding '{limit_field}' to the fields list.", UserWarning, stacklevel=2)
                # if the field is in the fields list, remove the field
            else:
                fields.remove(limit_field)
                # name and add the field name followed by .limit(value)
                fields.append(limit_arg)

        # Handle offset
        if offset:
            fields[:] = [s for s in fields if not (s.startswith(f"{offset_field}.offset") and s[len(f"{offset_field}.offset") :].isdigit())]

            # name and add the field name followed by .offset(value)
            offset_arg = f"{offset_field}.offset({offset})"
            if offset_field not in fields:
                fields.append(offset_arg)
                logging.info(f"Adding '{offset_field}' to the fields list.")
            # if the field is in the fields list, remove the field
            else:
                fields.remove(offset_field)
                # name and add the field name followed by .offset(value)
                fields.append(offset_arg)

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
        return f"https://api.xbrl.us{url}?"

    @_convert_params_to_dict_decorator
    def query(
        self,
        method: str,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[int] = None,
        sort: Optional[dict] = None,
        return_type: Optional[str] = "json",
        print_query: Optional[bool] = False,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            method (str): The name of the method to query.
            fields (list): The fields query parameter establishes the details of the data to return for the specific query.
            parameters (dict | Parameters): The parameters for the query.
            limit (int): A limit restricts the number of results returned by the query.
                The limit attribute can only be added to an object type and not a property.
                For example, to limit the number of facts in a query, {"fact": 10}.
            sort (dict): Any returned value can be sorted in ascending or descending order,
                using ``ASC`` or ``DESC`` (i.e. {"report.document-type": "DESC"}.
                Multiple sort criteria can be defined and the sort sequence is determined by
                the order of the items in the dictionary.
            return_type (str): Whether to return the results as a ``DataFrame`` or ``json``. You can also use the
                ``response`` to return the raw response from the API.
            print_query (bool=False): Whether to print the query.

        Returns:
            dict | DataFrame: The results of the query.
        """

        query_params = self._build_query_params(
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
        )

        if print_query:
            print(query_params)

        response = self._make_request(
            method="get",
            url=self._get_method_url(method, parameters),
            params=query_params,
        )

        response_data = response.json()

        if response.status_code != 200:
            raise response_data["message"]
        elif "data" not in response_data:
            warnings.warn("No data returned from the query.", UserWarning, stacklevel=2)
            return response_data

        data = response_data["data"]

        if limit is None or len(data) < limit:
            # Return the items from the first response if no user limit is provided
            if return_type == "dataframe":
                return DataFrame.from_dict(data)
            # for production only TODO: remove this
            elif return_type == "response":
                return response_data
            else:
                return data

        elif limit == "all":
            # Set the remaining limit to infinity
            limit = 999999999
            remaining_limit = limit - len(data)
        else:
            remaining_limit = limit - len(data)

        # To store all the items from the API response
        all_data = data

        offset = len(data)

        while remaining_limit > 0:
            # Determine the limit for the current request
            current_limit = min(len(data), remaining_limit)
            query_params = self._build_query_params(
                fields=fields,
                parameters=parameters,
                limit=current_limit,
                sort=sort,
                offset=offset,
            )

            response = self._make_request(
                method="get",
                url=self._get_method_url(method, parameters),
                params=query_params,
            )

            response_data = response.json()
            data = response_data["data"]

            # Add the items to the overall collection
            all_data.extend(data)

            # Decrease the remaining limit by the number of items received
            remaining_limit -= len(data)

            if len(data) < current_limit:
                # If the number of items received is less than the current limit,
                # it means we have reached the end
                # of available items, so we can break out of the loop.
                break

            # Update the offset for the next request
            offset += current_limit

        if return_type == "dataframe":
            return DataFrame.from_dict(all_data)
        else:
            return all_data
