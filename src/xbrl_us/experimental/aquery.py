import asyncio
import re
from collections.abc import Iterable
from functools import wraps
from typing import Optional
from typing import Union

import aiohttp
from pandas import DataFrame
from tqdm import tqdm

from xbrl_us import XBRL


def _remove_special_fields(fields):
    # Define the patterns to be removed
    patterns = [r"(.+)\.(sort\((.+)\))?$", r"(.+)\.(limit\((\d+)\))?$", r"(.+)\.(offset\((\d+)\))?$"]

    # For each field, check if it matches any of the patterns. If it does, remove it.
    for field in fields[:]:  # iterate over a slice copy of the list to safely modify it during iteration
        if any(re.match(pattern, field, re.IGNORECASE) for pattern in patterns):
            fields.remove(field)

    return fields


def _convert_params_to_dict_decorator():
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
            parameters = kwargs.get("parameters")
            if parameters and not isinstance(parameters, dict):
                raise ValueError(f"Parameters must be a dict or Parameters object. " f"Got {type(parameters)} instead.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _build_query_params(
    method: Optional[str] = None,
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
    """
    query_params = {}

    if parameters:
        # convert the parameters to a string and add it to the query_params
        query_params.update(
            {f"{k}": ",".join(map(str, v)) if isinstance(v, Iterable) and not isinstance(v, str) else str(v) for k, v in parameters.items()}
        )

    # Handle sort
    if sort:
        # check if the sort field is in the fields list
        for field, direction in sort.items():
            # name the field name followed by .sort(value)
            sorted_arg = f"{field}.sort({direction.upper()})"
            if field in fields:
                # if the field is in the fields list, remove the field
                fields.remove(field)
            fields.append(sorted_arg)

    # Handle limit
    if limit:
        # name and add the field name followed by .limit(value)
        limit_arg = f"{limit_field}.limit({limit})"
        if limit_field in fields:
            # if the field is in the fields list, remove the field
            fields.remove(limit_field)
        fields.append(limit_arg)

    # Handle offset
    if offset:
        # name and add the field name followed by .offset(value)
        offset_arg = f"{offset_field}.offset({offset})"
        if offset_field in fields:
            fields.remove(offset_field)
        fields.append(offset_arg)

    query_params["fields"] = ",".join(fields)

    return query_params


class XBRLAsync(XBRL):
    @_convert_params_to_dict_decorator()
    def query(
        self,
        method: str,
        fields: Optional[list] = None,
        parameters: Optional[Union[dict]] = None,
        limit: Optional[int] = None,
        sort: Optional[dict] = None,
        unique: Optional[bool] = False,
        as_dataframe: bool = False,
        print_query: Optional[bool] = False,
        timeout: Optional[int] = None,
        **kwargs,
    ) -> Union[dict, DataFrame]:
        """Asynchronous version of the query method"""
        method_url = self._get_method_url(method_name=method, parameters=parameters, unique=unique)

        query_params = _build_query_params(
            method=method,
            fields=fields,
            parameters=parameters,
            limit=limit,
            sort=sort,
        )

        account_limit = min(limit, self.account_limit) if limit is not None else self.account_limit

        query_params = _build_query_params(
            method=method,
            fields=fields,
            parameters=parameters,
            limit=account_limit,
            sort=sort,
        )

        if print_query:
            print(query_params)

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
                        method=method,
                        fields=fields,
                        parameters=parameters,
                        limit=current_limit,
                        sort=sort,
                        offset=offset,
                    )

                    tasks.append(session.get(url=method_url, params=query_params, headers=headers, timeout=timeout))
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
