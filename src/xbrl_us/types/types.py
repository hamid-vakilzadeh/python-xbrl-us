from typing import List
from typing import Literal
from typing import TypedDict
from typing import Union

from typing_extensions import NotRequired

PERIOD_FISCAL_PERIOD = Literal["Y", "Q1", "Q2", "Q3", "Q4", "3QCUM", "H1", "H2"]

# Define allowed values for method
AcceptableMethods = Literal[
    "assertion search",  # /assertion/search
    "concept name search",  # /concept/{concept.local-name}/search
    "concept search",  # /concept/search
    "cube search",  # /cube/search
    "dimension search",
    "document search",  # /document/search
    "dts id concept label",  # /dts/{dts.id}/concept/{concept.local-name}/label
    "dts id concept name",  # /dts/{dts-id}/concept/{concept.local-name}
    "dts id concept reference",  # /dts/{dts.id}/concept/{concept.local-name}/reference
    "dts id concept search",  # /dts/{dts.id}/concept/search
    "dts id network",  # /dts/{dts.id}/network
    "dts id network search",  # /dts/{dts.id}/network/search
    "dts search",  # /dts/search
    "entity id",  # /entity/{entity.id}
    "entity id report search",  # /entity/{entity.id}/report/search
    "entity report search",  # /entity/report/search
    "entity search",  # /entity/search
    "fact id",  # /fact/{fact.id}
    "fact search",  # /fact/search
    "fact search oim",  # /fact/search/oim
    "label dts id search",
    "label search",  # /label/search
    "network id",  # /network/{network.id}
    "network id relationship search",  # /network/{network.id}/relationship/search
    "network relationship search",  # /network/relationship/search
    "relationship search",  # /relationship/search
    "relationship tree search",  # /relationship/tree/search
    "report fact search",  # /report/fact/search
    "report id",  # /report/{report.id}
    "report id fact search",  # /report/{report.id}/fact/search
    "report search",  # /report/search
]
"""All fields with type information for the fact endpoint."""

FACT_SORT = TypedDict(
    "FactSort", {field: NotRequired[Union[str, List[str]]] for field in ["1", "2", "3"]}, total=False  # Makes all fields optional
)
