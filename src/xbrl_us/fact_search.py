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
        fields (list): A list of fields to be returned in the response. default to [fact.*]
        parameters (Optional[Union[Parameters, dict]]): A dictionary containing the parameters for fact search.
        limit: The maximum number of results to be returned.
        sort: A dictionary containing the field to sort by and the sort order.


    Attributes:
        base_url (str): The base URL for fact search.
        ALLOWED_PARAMETERS (dict): A dictionary containing the allowed parameters and fields for fact search.

    """

    base_url = fact_search_url
    ALLOWED_PARAMETERS: ClassVar[dict] = {
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
        }
    }

    def __init__(
        self,
        authorization: AuthorizationGrant,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: int = 100,
        sort: Optional[dict] = None,
        offset: int = 0,
    ):
        self.authorization: AuthorizationGrant = authorization
        self.fields: list = fields or ["fact.*"]
        self.parameters: Optional[Union[Parameters, dict]] = self.set_parameters(parameters)
        self.limit: int = limit
        self.sort: dict = sort
        self.offset: int = offset
        self.validate_parameters()  # Validate the provided fields, parameters, limit, offset, and sort
        self.results = self._make_request()  # Perform the API call and store the results

    @staticmethod
    def set_parameters(parameters):
        """
        Set the parameters for the request.
        """
        if parameters:
            if isinstance(parameters, dict):
                return parameters
            elif isinstance(parameters, Parameters):
                return parameters.get_parameters_dict()
            else:
                raise ValueError("Parameters must be a dict or Parameters object")

    def validate_parameters(self):
        """
        Validate the provided fields, parameters, limit, offset, and sort.
        Raises:
            ValueError: If any of the provided fields or parameters are not allowed or if the values are invalid.
        """
        allowed_params = self.ALLOWED_PARAMETERS.get("fact_search", {}).get("parameters", set())
        allowed_fields = self.ALLOWED_PARAMETERS.get("fact_search", {}).get("fields", set())

        if self.fields:
            for field in self.fields:
                # raise error if field is not a list
                if not isinstance(field, str):
                    raise ValueError("Field must be a string")
                # raise error if field is not in allowed fields
                if field not in allowed_fields:
                    raise ValueError(f"Field '{field}' is not allowed")
        else:
            raise ValueError("Field cannot be None")

        if self.parameters:
            for param in self.parameters:
                if param not in allowed_params:
                    raise ValueError(f"Parameter '{param}' is not allowed")

        if self.limit and not isinstance(self.limit, int):
            raise ValueError("Limit must be an integer")

        if self.sort:
            if not isinstance(self.sort, dict):
                raise ValueError("Sort must be a dictionary")
            for key, value in self.sort.items():
                if key not in allowed_fields:
                    raise ValueError(f"Sort key '{key}' is not allowed. Allowed sort keys are: {allowed_fields}")
                if value not in ["asc", "desc"]:
                    raise ValueError("Sort value should be 'asc' or 'desc'")

        if self.offset and not isinstance(self.offset, int):
            raise ValueError("Offset must be an integer")

    def _make_request(self):
        self.authorization.ensure_access_token()
        headers = {"Authorization": f"Bearer {self.authorization.access_token}"}

        query_params = self._build_query_params()
        response = requests.get(self.base_url, params=query_params, headers=headers, timeout=30)
        return response.json()

    def _build_query_params(self):
        query_params = {"fields": ",".join(self.fields)}

        if self.parameters:
            query_params.update(
                {f"{k}": ",".join(map(str, v)) if self.is_non_string_iterable(v) else str(v) for k, v in self.parameters.items()}
            )

        # Handle sort
        if self.sort:
            for field, direction in self.sort.items():
                query_params["fields"] += f",{field}.sort({direction.upper()})"

        # Handle limit
        if self.limit:
            query_params["fields"] += f",fact.limit({self.limit})"
        else:
            query_params["fields"] += ",fact.limit(100)"

        # Handle offset
        if self.offset:
            query_params["fields"] += f",fact.offset({self.offset})"

        return query_params

    @staticmethod
    def is_non_string_iterable(obj):
        return isinstance(obj, Iterable) and not isinstance(obj, str)

    def __call__(self):
        return self.results
