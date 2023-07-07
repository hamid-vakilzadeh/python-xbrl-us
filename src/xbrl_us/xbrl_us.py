from collections.abc import Callable
from functools import wraps
from typing import ClassVar
from typing import Optional
from typing import Union

from pandas import DataFrame

from .utils import BaseClient
from .utils import Parameters


class XBRL(BaseClient):
    _ALLOWED_PARAMETERS: ClassVar[dict] = {
        "search_fact": {
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
        },
        "get_fact_by_id": {
            "parameters": ["fact.id", "fact.text-search"],
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
        },
        "global": {
            "limit_fields": ["fact"],
            "sort_fields": ["fact"],
            "offset_fields": ["fact"],
        },
    }

    @staticmethod
    def convert_params_to_dict_decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            parameters = kwargs.get("parameters")
            if isinstance(parameters, Parameters):
                kwargs["parameters"] = parameters.get_parameters_dict()
            elif parameters and not isinstance(parameters, dict):
                raise ValueError(f"Parameters must be a dict or Parameters object. " f"Got {type(parameters)} instead.")
            return func(self, *args, **kwargs)

        return wrapper

    @convert_params_to_dict_decorator
    @BaseClient._validate_parameters
    def search_fact(
        self,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[dict] = None,
        sort: Optional[dict] = None,
        offset: Optional[dict] = None,
        as_dataframe: bool = False,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            fields:
            parameters:
            limit:
            sort:
            offset:
            as_dataframe:

        Returns:

        """
        response = self._make_request(
            method="get",
            url=self._URLS.get("fact_search_url"),
            params=self._build_query_params(
                fields=fields,
                parameters=parameters,
                limit=limit,
                sort=sort,
                offset=offset,
            ),
        )
        if as_dataframe:
            return self._convert_to_dataframe(response.json()["data"])
        else:
            return response.json()["data"]

    @BaseClient._validate_parameters
    @convert_params_to_dict_decorator
    def get_fact_by_id(
        self,
        fields: Optional[list] = None,
        parameters: Optional[Union[Parameters, dict]] = None,
        limit: Optional[dict] = None,
        sort: Optional[dict] = None,
        offset: Optional[dict] = None,
        as_dataframe: bool = False,
    ) -> Union[dict, DataFrame]:
        """

        Args:
            fields:
            parameters:
            limit:
            sort:
            offset:
            as_dataframe:

        Returns:

        """
        response = self._make_request(method="get", url="")
        if as_dataframe:
            return self._convert_to_dataframe(response.json()["data"])
        else:
            return response.json()["data"]

    def search_report(self, params=None, as_dataframe=False):
        response = self._make_request(method="get", url="")
        if as_dataframe:
            return self._convert_to_dataframe(response.json()["data"])
        else:
            return response.json()["data"]

    def get_report_by_id(self, report_id, as_dataframe=False):
        response = self._make_request(method="get", url="")
        if as_dataframe:
            return self._convert_to_dataframe(response.json()["data"])
        else:
            return response.json()["data"]
