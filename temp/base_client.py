import time
from collections.abc import Iterable
from functools import wraps
from typing import ClassVar
from typing import Optional

import requests


class BaseClient:
    _ALLOWED_PARAMETERS: ClassVar[dict] = {}
    _URLS: ClassVar[dict] = {
        "base_url": "https://api.xbrl.us/oauth2/token",
        "auth_url": "https://api.xbrl.us/oauth2/token",
        "fact_search_url": "https://api.xbrl.us/api/v1/fact/search",
        "fact_id_url": "https://api.xbrl.us/api/v1/fact/{fact_id}",
    }

    def __init__(self, client_id, client_secret, username, password):
        """
        Initializes an instance of XBRL authorized connection.

        Parameters
        ----------
            client_id (str): The client ID.
            client_secret (str): The client secret.
            username (str): The username.
            password (str): The password.
        """
        self._url = "https://api.xbrl.us/oauth2/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self._access_token_expires_at = 0
        self._refresh_token_expires_at = 0

    def _get_token(self, grant_type: str = "password", refresh_token=None):
        """
        Retrieves an access token from the token URL.

        Args:
            grant_type (str): The grant type (default: "password").
            refresh_token (str): The refresh token (default: None).
        """
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

    def _make_request(self, method, url, **kwargs):
        """
        Makes an HTTP request with the provided method, URL, and additional arguments.

        Args:
            method (str): The HTTP method for the request.
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments to be passed to the requests library.

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
            function_name = func.__name__
            allowed_parameters = instance._ALLOWED_PARAMETERS.get(function_name, {})
            allowed_other = instance._ALLOWED_PARAMETERS.get("global", {})

            parameters = kwargs.get("parameters")
            fields = kwargs.get("fields")
            limit = kwargs.get("limit")
            sort = kwargs.get("sort")
            offset = kwargs.get("offset")

            allowed_params = allowed_parameters.get("parameters", set())
            allowed_fields = allowed_parameters.get("fields", set())
            allowed_limit_fields = allowed_other.get("limit_fields", set())
            allowed_sort_fields = allowed_other.get("sort_fields", set())
            allowed_offset_fields = allowed_other.get("offset_fields", set())

            # Validate fields
            if fields:
                for field in fields:
                    if not isinstance(field, str):
                        raise ValueError(f"field must be a string. {field} is {type(field)}")
                    if field not in allowed_fields:
                        raise ValueError(f"Field '{field}' is not allowed as a field. " f"Allowed fields are: {allowed_fields}.")
            else:
                raise ValueError("fields cannot be None.")

            # Validate parameters
            if parameters:
                for param in parameters:
                    if param not in allowed_params:
                        raise ValueError(f"Parameter '{param}' is not allowed. " f"Allowed parameters are: {allowed_params}.")

            # Validate limit
            if limit:
                if not isinstance(limit, dict):
                    raise ValueError(f"limit must be a dictionary not {type(limit)}. " "e.g. limit = {{'fact': 100}}.")
                for key, value in limit.items():
                    if key not in allowed_limit_fields:
                        raise ValueError(f"Limit key '{key}' is not allowed. " f"Allowed limit keys are: {allowed_limit_fields}")
                    if not isinstance(value, int):
                        raise ValueError(f"Limit value must be an integer. {value} is not an integer")
            else:
                kwargs["limit"] = {"fact": 100}

            # Validate sort
            if sort:
                if not isinstance(sort, dict):
                    raise ValueError("Sort must be a dictionary")
                for key, value in sort.items():
                    if key not in allowed_sort_fields:
                        raise ValueError(f"Sort key '{key}' is not allowed. " f"Allowed sort keys are: {allowed_sort_fields}.")
                    if value.lower() not in ["asc", "desc"]:
                        raise ValueError("Sort value should be 'asc' or 'desc' only.")
            else:
                kwargs["sort"] = {"fact.id": "asc"}

            # Validate offset
            if offset:
                if not isinstance(offset, dict):
                    raise ValueError("Offset must be a dictionary")
                for key, value in offset.items():
                    if key not in allowed_offset_fields:
                        raise ValueError(f"Offset key '{key}' is not allowed. " f"Allowed offset keys are: {allowed_offset_fields}.")
                    if not isinstance(value, int):
                        raise ValueError(f"Offset value must be an integer. {value} is not an integer.")
            else:
                kwargs["offset"] = {"fact": 0}

            return func(instance, *args, **kwargs)

        return wrapper

    @staticmethod
    def _convert_to_dataframe(json_response):
        from pandas import DataFrame

        return DataFrame.from_dict(json_response)

    @staticmethod
    def _is_non_string_iterable(obj):
        return isinstance(obj, Iterable) and not isinstance(obj, str)

    @staticmethod
    def _build_query_params_decorator(func):
        @wraps(func)
        def wrapper(instance, *args, **kwargs):
            query_params = instance._build_query_params(
                fields=kwargs.get("fields"),
                parameters=kwargs.get("parameters"),
                limit=kwargs.get("limit"),
                sort=kwargs.get("sort"),
                offset=kwargs.get("offset"),
            )
            kwargs["query_params"] = query_params
            return func(instance, *args, **kwargs)

        return wrapper

    def _build_query_params(
        self,
        fields: Optional[list] = None,
        parameters=None,
        limit: Optional[dict] = None,
        sort: Optional[dict] = None,
        offset: Optional[dict] = None,
    ):
        query_params = {}

        if parameters:
            query_params.update(
                {f"{k}": ",".join(map(str, v)) if self._is_non_string_iterable(v) else str(v) for k, v in parameters.items()}
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
