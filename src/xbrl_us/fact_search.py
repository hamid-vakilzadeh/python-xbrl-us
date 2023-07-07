from collections.abc import Iterable
from typing import ClassVar
from typing import Optional
from typing import Union

import requests

from .shared import fact_search_url
from .utils import AuthorizationGrant
from .utils import Parameters


class FactSearch:
    """
    A class for performing fact search and retrieving XBRL data.

    Args:
        authorization (AuthorizationGrant): An instance of the authentication class for accessing the XBRL API.
        fields (list): A list of fields to be returned in the response.
        parameters (Optional[Union[Parameters, dict]]): A dictionary containing the parameters for fact search.
        limit (dict): A limit restricts the number of results returned by the query.
            The limit attribute can only be added to an object type and not a property.
            For example, to limit the number of reports in a query,
            the limit property is added to the fields to return as follows: default to {"fact": 100}.
        sort (dict): A dictionary containing the fields to sort by and the sort order.
            Any returned value can be sorted in ascending or descending order,
            by adding an attribute ("ASC" or "DESC") to a field value (i.e. {"report.document-type": "DESC"}).
            Multiple sort criteria can be defined and the sort sequence is determined by the order defined
            in the "fields" parameter. defaults to {"fact.id": "asc"}
        offset (int): The offset attribute enables targeting a return to a specific starting point
            in a query return sequence (i.e. {"report": 120}).
            To work reliably, at least one sorted property should be included in the returned fields.



    """

    _base_url = fact_search_url
    _ALLOWED_PARAMETERS: ClassVar[dict] = {
        "fact_search": {
            "parameters": [
                "concept.id",
                "concept.is-base",
                "concept.is-monetary",
                "concept.local-name",
                "concept.namespace",
                "dimension.is-base",
                "dimension.local-name",
                "dimension.namespace",
                "dimensions.count",
                "dimensions.id",
                "dts.entry-point",
                "dts.id",
                "dts.target-namespace",
                "entity.cik",
                "entity.id",
                "fact.has-dimensions",
                "fact.hash",
                "fact.id",
                "fact.is-extended",
                "fact.text-search",
                "fact.ultimus",
                "fact.ultimus-index",
                "fact.value",
                "fact.value-link",
                "member.is-base",
                "member.local-name",
                "member.typed-value",
                "member.member-value",
                "member.namespace",
                "period.calendar-period",
                "period.fiscal-id",
                "period.fiscal-period",
                "period.fiscal-year",
                "period.id",
                "period.year",
                "report.accession",
                "report.creation-software",
                "report.document-type",
                "report.document-index",
                "report.entry-url",
                "report.id",
                "report.restated",
                "report.restated-index",
                "report.sec-url",
                "report.sic-code",
                "report.source-id",
                "report.source-name",
                "unit",
            ],
            "fields": [
                "concept.balance-type",
                "concept.datatype",
                "concept.id",
                "concept.is-base",
                "concept.is-monetary",
                "concept.local-name",
                "concept.namespace",
                "concept.period-type",
                "dimension.is-base",
                "dimension.local-name",
                "dimension.namespace",
                "dimensions",
                "dimensions.count",
                "dimensions.id",
                "dts.entry-point",
                "dts.id",
                "dts.target-namespace",
                "entity.cik",
                "entity.id",
                "entity.name",
                "entity.scheme",
                "fact.decimals",
                "fact.example",
                "fact.has-dimensions",
                "fact.hash",
                "fact.highlighted-value",
                "fact.id",
                "fact.inline-display-value",
                "fact.inline-is-hidden",
                "fact.inline-negated",
                "fact.inline-scale",
                "fact.is-extended",
                "fact.numerical-value",
                "fact.ultimus",
                "fact.ultimus-index",
                "fact.value",
                "fact.value-link",
                "fact.xml-id",
                "member.is-base",
                "member.local-name",
                "member.typed-value",
                "member.member-value",
                "member.namespace",
                "period.calendar-period",
                "period.end",
                "period.fiscal-id",
                "period.fiscal-period",
                "period.fiscal-year",
                "period.id",
                "period.instant",
                "period.start",
                "period.year",
                "report.accession",
                "report.creation-software",
                "report.document-type",
                "report.document-index",
                "report.entry-url",
                "report.filing-date",
                "report.id",
                "report.period-end",
                "report.restated",
                "report.restated-index",
                "report.sec-url",
                "report.sic-code",
                "report.source-id",
                "report.source-name",
                "report.type",
                "unit",
                "unit.denominator",
                "unit.numerator",
                "unit.qname",
                "fact.*",
            ],
            "limit_fields": ["fact"],
            "sort_fields": ["fact"],
            "offset_fields": ["fact"],
        }
    }

    def __init__(
        self,
        authorization: AuthorizationGrant,
        fields: list,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[dict[str, int]] = None,
        sort: Optional[dict[str, str]] = None,
        offset: Optional[dict[str, int]] = None,
    ):
        self.authorization: AuthorizationGrant = authorization
        self.fields: list = fields
        self.parameters: Optional[Union[Parameters, dict]] = self._set_parameters(parameters)
        self.limit: dict = limit
        self.sort: dict = sort
        self.offset: dict = offset
        self._validate_parameters()  # Validate the provided fields, parameters, limit, offset, and sort
        self.results = self._make_request()  # Perform the API call and store the results

    @staticmethod
    def _set_parameters(parameters):
        """
        Set the parameters to dict format.
        """
        if parameters:
            if isinstance(parameters, dict):
                return parameters
            elif isinstance(parameters, Parameters):
                return parameters.get_parameters_dict()
            else:
                raise ValueError(f"Parameters must be a dict or Parameters object. " f"Got {type(parameters)} instead.")

    def _validate_parameters(self):
        """
        Validate the provided fields, parameters, limit, offset, and sort.
        Raises:
            ValueError: If any of the provided fields or parameters are not allowed or if the values are invalid.
        """
        allowed_params = self._ALLOWED_PARAMETERS.get("fact_search", {}).get("parameters", set())
        allowed_fields = self._ALLOWED_PARAMETERS.get("fact_search", {}).get("fields", set())
        allowed_limit_fields = self._ALLOWED_PARAMETERS.get("fact_search", {}).get("limit_fields", set())
        allowed_sort_fields = self._ALLOWED_PARAMETERS.get("fact_search", {}).get("sort_fields", set())
        allowed_offset_fields = self._ALLOWED_PARAMETERS.get("fact_search", {}).get("offset_fields", set())

        # Validate fields
        if self.fields:
            for field in self.fields:
                # raise error if field is not a list
                if not isinstance(field, str):
                    raise ValueError(f"field must be a string. {field} is {type(field)}")
                # raise error if a field is not in allowed fields
                if field not in allowed_fields:
                    raise ValueError(f"Field '{field}' is not allowed as a field. " f"Allowed fields are: {allowed_fields}.")
        else:
            # raise error if fields is None
            raise ValueError("fields cannot be None.")

        if self.parameters:
            for param in self.parameters:
                if param not in allowed_params:
                    raise ValueError(f"Parameter '{param}' is not allowed. " f"Allowed parameters are: {allowed_params}.")

        if self.limit:
            if not isinstance(self.limit, dict):
                raise ValueError(f"limit must be a dictionary not {type(self.limit)}. " "e.g. limit = {{'fact': 100}}.")
            for key, value in self.limit.items():
                if key not in allowed_limit_fields:  # TODO: only objects can get limit
                    raise ValueError(f"Limit key '{key}' is not allowed. " f"Allowed limit keys are: {allowed_limit_fields}")
                if not isinstance(value, int):
                    raise ValueError(f"Limit value must be an integer. {value} is not an integer")
        else:
            self.limit = {"fact": 100}

        if self.sort:
            if not isinstance(self.sort, dict):
                raise ValueError("Sort must be a dictionary")
            for key, value in self.sort.items():
                if key not in allowed_fields:
                    raise ValueError(f"Sort key '{key}' is not allowed. " f"Allowed sort keys are: {allowed_sort_fields}.")
                if value.lower() not in ["asc", "desc"]:
                    raise ValueError("Sort value should be 'asc' or 'desc' only.")
        else:
            self.sort = {"fact.id": "asc"}

        if self.offset:
            if not isinstance(self.offset, dict):
                raise ValueError("Offset must be an integer")
            for key, value in self.offset.items():
                if key not in allowed_fields:
                    raise ValueError(f"Offset key '{key}' is not allowed. " f"Allowed offset keys are: {allowed_offset_fields}.")
                if not isinstance(value, int):
                    raise ValueError(f"Offset value must be an integer. {value} is not an integer.")
        else:
            self.offset = {"fact": 0}

    def _make_request(self):
        self.authorization.ensure_access_token()
        headers = {"Authorization": f"Bearer {self.authorization.access_token}"}

        query_params = self._build_query_params()
        response = requests.get(self._base_url, params=query_params, headers=headers, timeout=30)
        return response.json()

    def _build_query_params(self):
        query_params = {}

        if self.parameters:
            query_params.update(
                {f"{k}": ",".join(map(str, v)) if self._is_non_string_iterable(v) else str(v) for k, v in self.parameters.items()}
            )

        # Handle sort
        if self.sort:
            # TODO: verify that sort, limit, and offset work together for the same field
            # check if the sort field is in the fields list
            for field, direction in self.sort.items():
                # if the field is not in the fields list add the field name followed by .sort(value)
                if field not in self.fields:
                    self.fields.append(f"{field}.sort({direction.upper()})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .sort(value)
                else:
                    self.fields.remove(field)
                    self.fields.append(f"{field}.sort({direction.upper()})")

        # Handle limit
        if self.limit:
            # check if the limit field is in the fields list
            for field, value in self.limit.items():
                # if the field is not in the fields list add the field name followed by .limit(value)
                if field not in self.fields:
                    self.fields.append(f"{field}.limit({value})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .limit(value)
                else:
                    self.fields.remove(field)
                    self.fields.append(f"{field}.limit({value})")

        # Handle offset
        if self.offset:
            # check if the offset field is in the fields list
            for field in self.offset.items():
                # if the field is not in the fields list add the field name followed by .offset(value)
                if field not in self.fields:
                    self.fields.append(f"{field}.offset({self.offset})")
                # if the field is in the fields list, remove the field
                # name and add the field name followed by .offset(value)
                else:
                    self.fields.remove(field)
                    self.fields.append(f"{field}.offset({self.offset})")

        query_params["fields"] = ",".join(self.fields)

        return query_params

    @staticmethod
    def _is_non_string_iterable(obj):
        return isinstance(obj, Iterable) and not isinstance(obj, str)

    def __call__(self):
        return self.results
