from typing import List
from typing import Literal
from typing import TypedDict

from typing_extensions import NotRequired


class UniversalFieldMap:
    """Universal mapping between snake_case field names and original API format.

    This class provides conversion methods between snake_case field names used in Python
    and the original dot/hyphen notation used in the API (e.g. 'fact.value' -> 'fact_value').
    """

    @classmethod
    def to_original(cls, snake_name: str) -> str:
        """Convert a snake_case field name to the original API format with dots/hyphens"""
        # Convert snake_case back to dot notation
        parts = snake_name.split("_")
        if len(parts) == 1:
            return snake_name

        if len(parts) == 2:
            return f"{parts[0]}.{parts[1]}"

        if len(parts) > 2:
            return f"{parts[0]}.{'-'.join(parts[1:])}"

    @classmethod
    def to_snake(cls, original_name: str) -> str:
        """Convert an original API field name to snake_case"""
        return original_name.replace(".", "_").replace("-", "_")


class AssertionParameters(TypedDict, total=False):
    """Parameters for assertion endpoint response data

    Example:
        >>> data: AssertionParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    assertion_code: NotRequired[str]
    """Unique code associated with a specific error. For example: DQC.US.0073.7648"""
    assertion_severity: NotRequired[str]
    """Severity of the rule, indicated as error, warning or information."""
    assertion_source: NotRequired[str]
    """The source of rule base that generated the rule, indicated as DQC, EFM, or xbrlus-cc."""
    assertion_type: NotRequired[str]
    """The rule number of the rule. i.e. 0099"""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_name: NotRequired[str]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_filing_year: NotRequired[int]
    """No definition provided"""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    report_zip_url: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""


AssertionFields = List[
    Literal[
        "assertion.code",
        "assertion.detail",
        "assertion.effective-date",
        "assertion.rule-focus",
        "assertion.run-date",
        "assertion.severity",
        "assertion.source",
        "assertion.type",
        "entity.cik",
        "entity.code",
        "entity.name",
        "entity.scheme",
        "report.accepted-timestamp",
        "report.accession",
        "report.base-taxonomy",
        "report.creation-software",
        "report.document-type",
        "report.entry-url",
        "report.filing-date",
        "report.filing-year",
        "report.form-type",
        "report.id",
        "report.period-focus",
        "report.sec-url",
        "report.sic-code",
        "report.year-focus",
        "report.zip-url",
    ]
]
"""All fields with type information for the assertion endpoint."""


AssertionEndpoint = Literal["/assertion/search"]
"""Valid endpoint identifiers for the assertion endpoint.
Can be either the endpoint key or the full path."""


class AssertionSorts(TypedDict, total=False):
    """Sort Fields for assertion endpoint response data

    Example:
        >>> data: AssertionSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    assertion_code: NotRequired[Literal["asc", "desc"]]
    """Unique code associated with a specific error. For example: DQC.US.0073.7648"""
    assertion_detail: NotRequired[Literal["asc", "desc"]]
    """Message details for the error describing the error."""
    assertion_effective_date: NotRequired[Literal["asc", "desc"]]
    """Effective date of the rule. This is the date that the rule went into effect and all companies were required to follow the rule."""
    assertion_rule_focus: NotRequired[Literal["asc", "desc"]]
    """Details of fact(s) impacted by the error, in an XML format."""
    assertion_run_date: NotRequired[Literal["asc", "desc"]]
    """Date that the rule was run on the filing."""
    assertion_severity: NotRequired[Literal["asc", "desc"]]
    """Severity of the rule, indicated as error, warning or information."""
    assertion_source: NotRequired[Literal["asc", "desc"]]
    """The source of rule base that generated the rule, indicated as DQC, EFM, or xbrlus-cc."""
    assertion_type: NotRequired[Literal["asc", "desc"]]
    """The rule number of the rule. i.e. 0099"""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    report_accepted_timestamp: NotRequired[Literal["asc", "desc"]]
    """Date that the report was accepted at the regulator."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_filing_year: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    report_zip_url: NotRequired[Literal["asc", "desc"]]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""


class ConceptParameters(TypedDict, total=False):
    """Parameters for concept endpoint response data

    Example:
        >>> data: ConceptParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_id: NotRequired[int]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_abstract: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_is_monetary: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[str]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[str]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    label_role: NotRequired[str]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_text: NotRequired[str]
    """The text of the label. i.e Assets, Current"""
    reference_id: NotRequired[int]
    """Unique ID of the reference."""
    reference_role: NotRequired[str]
    """The reference role used to identify the reference type i.e. http://fasb.org/us-gaap/role/ref/legacyRef"""


ConceptFields = List[
    Literal[
        "concept.balance-type",
        "concept.datatype",
        "concept.id",
        "concept.is-abstract",
        "concept.is-monetary",
        "concept.is-nillable",
        "concept.is-numeric",
        "concept.local-name",
        "concept.namespace",
        "concept.period-type",
        "concept.substitution",
        "dts.entry-point",
        "dts.hash",
        "dts.id",
        "dts.target-namespace",
        "label.id",
        "label.lang",
        "label.role",
        "label.role-short",
        "label.text",
        "parts.local-name",
        "parts.namespace",
        "parts.order",
        "parts.part-value",
        "reference.id",
        "reference.role",
        "reference.role-definition",
        "reference.role-short",
    ]
]
"""All fields with type information for the concept endpoint."""


ConceptEndpoint = Literal["/concept/search", "/concept/{concept.local-name}/search"]
"""Valid endpoint identifiers for the concept endpoint.
Can be either the endpoint key or the full path."""


class ConceptSorts(TypedDict, total=False):
    """Sort Fields for concept endpoint response data

    Example:
        >>> data: ConceptSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[Literal["asc", "desc"]]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_datatype: NotRequired[Literal["asc", "desc"]]
    """The datatype of the concept such as monetary or string."""
    concept_id: NotRequired[Literal["asc", "desc"]]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_abstract: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_is_monetary: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_is_nillable: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept can have a nill value."""
    concept_is_numeric: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is a numeric value. If yes the value is shown as true."""
    concept_local_name: NotRequired[Literal["asc", "desc"]]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    concept_period_type: NotRequired[Literal["asc", "desc"]]
    """The period type of the concept. This can be either duration or instant."""
    concept_substitution: NotRequired[Literal["asc", "desc"]]
    """The substitution group of the concept."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[Literal["asc", "desc"]]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[Literal["asc", "desc"]]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    label_id: NotRequired[Literal["asc", "desc"]]
    """Unique ID of the label."""
    label_lang: NotRequired[Literal["asc", "desc"]]
    """The ISO language code used to express the label, such as en-us."""
    label_role: NotRequired[Literal["asc", "desc"]]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_role_short: NotRequired[Literal["asc", "desc"]]
    """The suffix of the label role used to identify the label type i.e. label"""
    label_text: NotRequired[Literal["asc", "desc"]]
    """The text of the label. i.e Assets, Current"""
    parts_local_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    parts_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    parts_order: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    parts_part_value: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    reference_id: NotRequired[Literal["asc", "desc"]]
    """Unique ID of the reference."""
    reference_role: NotRequired[Literal["asc", "desc"]]
    """The reference role used to identify the reference type i.e. http://fasb.org/us-gaap/role/ref/legacyRef"""
    reference_role_definition: NotRequired[Literal["asc", "desc"]]
    """The reference definition used to identify the reference role i.e. Legacy reference"""
    reference_role_short: NotRequired[Literal["asc", "desc"]]
    """The reference role used to identify the reference type i.e. legacyRef"""


class CubeParameters(TypedDict, total=False):
    """Parameters for cube endpoint response data

    Example:
        >>> data: CubeParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    cube_description: NotRequired[str]
    """The dts network descrition of the cube."""
    cube_drs_role_uri: NotRequired[str]
    """??The cube uri for the drs role."""
    cube_id: NotRequired[int]
    """The identifier used to identify a cube."""
    cube_member_value: NotRequired[str]
    """No definition provided"""
    cube_primary_local_name: NotRequired[str]
    """The primary local-name of the cube."""
    cube_primary_namespace: NotRequired[str]
    """The primary namespace of the cube."""
    cube_table_local_name: NotRequired[str]
    """The cubes local-name for it's element."""
    cube_table_namespace: NotRequired[str]
    """No definition provided"""
    cube_tree_depth: NotRequired[int]
    """The depth of this item within a tree."""
    cube_tree_sequence: NotRequired[int]
    """Sequence order if visualized in a tree."""
    dimensions_count: NotRequired[int]
    """The number of dimensional qualifiers associated with a given fact."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    fact_accuracy_index: NotRequired[int]
    """No definition provided"""
    fact_id: NotRequired[int]
    """The unique identifier used to identify a fact."""
    fact_is_extended: NotRequired[Literal["true", "false"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_numerical_value: NotRequired[float]
    """The numerical value of the fact that was reported. """
    fact_ultimus: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_value: NotRequired[str]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    period_calendar_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_fiscal_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[int]
    """The fiscal year in which the fact is applicable."""
    period_year: NotRequired[int]
    """The calendar year in which the facy is applicable."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    unit: NotRequired[str]
    """The unit of measure associated with the fact."""


CubeFields = List[
    Literal[
        "concept.balance-type",
        "cube.description",
        "cube.drs-role-uri",
        "cube.id",
        "cube.member-value",
        "cube.primary-local-name",
        "cube.primary-namespace",
        "cube.table-local-name",
        "cube.table-namespace",
        "cube.tree-depth",
        "cube.tree-sequence",
        "dimension-pair",
        "dimensions",
        "dimensions.count",
        "dts.id",
        "entity.code",
        "fact.accuracy-index",
        "fact.decimals",
        "fact.id",
        "fact.inline-display-value",
        "fact.inline-negated",
        "fact.is-extended",
        "fact.numerical-value",
        "fact.ultimus",
        "fact.value",
        "period.calendar-period",
        "period.fiscal-period",
        "period.fiscal-year",
        "period.year",
        "report.accession",
        "report.base-taxonomy",
        "report.document-type",
        "report.entity-name",
        "report.id",
        "report.source-id",
        "report.source-name",
        "unit",
    ]
]
"""All fields with type information for the cube endpoint."""


CubeEndpoint = Literal["/cube/search"]
"""Valid endpoint identifiers for the cube endpoint.
Can be either the endpoint key or the full path."""


class CubeSorts(TypedDict, total=False):
    """Sort Fields for cube endpoint response data

    Example:
        >>> data: CubeSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[Literal["asc", "desc"]]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    cube_description: NotRequired[Literal["asc", "desc"]]
    """The dts network descrition of the cube."""
    cube_drs_role_uri: NotRequired[Literal["asc", "desc"]]
    """??The cube uri for the drs role."""
    cube_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a cube."""
    cube_member_value: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    cube_primary_local_name: NotRequired[Literal["asc", "desc"]]
    """The primary local-name of the cube."""
    cube_primary_namespace: NotRequired[Literal["asc", "desc"]]
    """The primary namespace of the cube."""
    cube_table_local_name: NotRequired[Literal["asc", "desc"]]
    """The cubes local-name for it's element."""
    cube_table_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    cube_tree_depth: NotRequired[Literal["asc", "desc"]]
    """The depth of this item within a tree."""
    cube_tree_sequence: NotRequired[Literal["asc", "desc"]]
    """Sequence order if visualized in a tree."""
    dimension_pair: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    dimensions: NotRequired[Literal["asc", "desc"]]
    """Returns an array of dimensions associated with the given fact."""
    dimensions_count: NotRequired[Literal["asc", "desc"]]
    """The number of dimensional qualifiers associated with a given fact."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    fact_accuracy_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_decimals: NotRequired[Literal["asc", "desc"]]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier used to identify a fact."""
    fact_inline_display_value: NotRequired[Literal["asc", "desc"]]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_negated: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_is_extended: NotRequired[Literal["asc", "desc"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_numerical_value: NotRequired[Literal["asc", "desc"]]
    """The numerical value of the fact that was reported. """
    fact_ultimus: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_value: NotRequired[Literal["asc", "desc"]]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    period_calendar_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_fiscal_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[Literal["asc", "desc"]]
    """The fiscal year in which the fact is applicable."""
    period_year: NotRequired[Literal["asc", "desc"]]
    """The calendar year in which the facy is applicable."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    unit: NotRequired[Literal["asc", "desc"]]
    """The unit of measure associated with the fact."""


class DocumentParameters(TypedDict, total=False):
    """Parameters for document endpoint response data

    Example:
        >>> data: DocumentParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    document_documentset: NotRequired[str]
    """Boolean attribute that indicates if the document is part of the document set, i.e. an instant document."""
    document_id: NotRequired[int]
    """An internal unique identifier of the document."""
    document_text_search: NotRequired[str]
    """Cannot be used as a return field. Search for strings within document object (ie. to locate a specific name, topic or reference within an entire document). Fields returned include document.example and document.highlighted-value. The XBRL API uses the Sphinx search engine to identify text. This powerful search engine quickly identifies a given text string. Sphinx is enabled to support stemming, which means it will also return plurals of a noun i.e. ipad will also return ipads. It will also return the present, future and past form of a verb for example the word kill will also return killed and killing. To match the word exactly the character '=' can be placed in front of the word i.e. = ipad will return the occurrence of the word ipad only."""
    document_top_level: NotRequired[Literal["true", "false"]]
    """Boolean that indicates if the file in a dts is the entry point."""
    document_uri: NotRequired[str]
    """The url at which the document comprising the dts is located."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_name: NotRequired[str]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""


DocumentFields = List[
    Literal[
        "document.content",
        "document.documentset",
        "document.id",
        "document.text-search",
        "document.top-level",
        "document.tree-level",
        "document.tree-order",
        "document.type",
        "document.uri",
        "dts.content",
        "dts.id",
        "entity.cik",
        "entity.code",
        "entity.name",
        "entity.scheme",
        "report.filing-date",
        "report.hash",
        "report.id",
        "report.source-id",
        "report.source-name",
    ]
]
"""All fields with type information for the document endpoint."""


DocumentEndpoint = Literal["/document/search"]
"""Valid endpoint identifiers for the document endpoint.
Can be either the endpoint key or the full path."""


class DocumentSorts(TypedDict, total=False):
    """Sort Fields for document endpoint response data

    Example:
        >>> data: DocumentSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    document_content: NotRequired[Literal["asc", "desc"]]
    """The content of the document."""
    document_documentset: NotRequired[Literal["asc", "desc"]]
    """Boolean attribute that indicates if the document is part of the document set, i.e. an instant document."""
    document_id: NotRequired[Literal["asc", "desc"]]
    """An internal unique identifier of the document."""
    document_text_search: NotRequired[Literal["asc", "desc"]]
    """Cannot be used as a return field. Search for strings within document object (ie. to locate a specific name, topic or reference within an entire document). Fields returned include document.example and document.highlighted-value. The XBRL API uses the Sphinx search engine to identify text. This powerful search engine quickly identifies a given text string. Sphinx is enabled to support stemming, which means it will also return plurals of a noun i.e. ipad will also return ipads. It will also return the present, future and past form of a verb for example the word kill will also return killed and killing. To match the word exactly the character '=' can be placed in front of the word i.e. = ipad will return the occurrence of the word ipad only."""
    document_top_level: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the file in a dts is the entry point."""
    document_tree_level: NotRequired[Literal["asc", "desc"]]
    """Level of the files in terms of which files import or reference child files."""
    document_tree_order: NotRequired[Literal["asc", "desc"]]
    """Order of the files in terms of how the dts is compiled from the underlying documents."""
    document_type: NotRequired[Literal["asc", "desc"]]
    """Indicates if the document is a schema, linkbase or instance."""
    document_uri: NotRequired[Literal["asc", "desc"]]
    """The url at which the document comprising the dts is located."""
    dts_content: NotRequired[Literal["asc", "desc"]]
    """Contents of the document."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""


class DtsParameters(TypedDict, total=False):
    """Parameters for dts endpoint response data

    Example:
        >>> data: DtsParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[str]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[str]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""


DtsFields = List[
    Literal[
        "dts.entity-name",
        "dts.entry-point",
        "dts.hash",
        "dts.id",
        "dts.taxonomy",
        "dts.taxonomy-name",
        "dts.version",
        "report.accession",
        "report.hash",
        "report.id",
    ]
]
"""All fields with type information for the dts endpoint."""


DtsEndpoint = Literal["/dts/search"]
"""Valid endpoint identifiers for the dts endpoint.
Can be either the endpoint key or the full path."""


class DtsSorts(TypedDict, total=False):
    """Sort Fields for dts endpoint response data

    Example:
        >>> data: DtsSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[Literal["asc", "desc"]]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[Literal["asc", "desc"]]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""


class DtsConceptParameters(TypedDict, total=False):
    """Parameters for dts/concept endpoint response data

    Example:
        >>> data: DtsConceptParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[str]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[str]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""


DtsConceptFields = List[
    Literal[
        "dts.entity-name",
        "dts.entry-point",
        "dts.hash",
        "dts.id",
        "dts.taxonomy",
        "dts.taxonomy-name",
        "dts.version",
        "report.accession",
        "report.hash",
        "report.id",
    ]
]
"""All fields with type information for the dts/concept endpoint."""


DtsConceptEndpoint = Literal[
    "/dts/{dts-id}/concept/{concept.local-name}",
    "/dts/{dts.id}/concept/search",
    "/dts/{dts.id}/concept/{concept.local-name}/label",
    "/dts/{dts.id}/concept/{concept.local-name}/reference",
]
"""Valid endpoint identifiers for the dts/concept endpoint.
Can be either the endpoint key or the full path."""


class DtsConceptSorts(TypedDict, total=False):
    """Sort Fields for dts/concept endpoint response data

    Example:
        >>> data: DtsConceptSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[Literal["asc", "desc"]]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[Literal["asc", "desc"]]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""


class DtsNetworkParameters(TypedDict, total=False):
    """Parameters for dts/network endpoint response data

    Example:
        >>> data: DtsNetworkParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[str]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[str]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""


DtsNetworkFields = List[
    Literal[
        "dts.entity-name",
        "dts.entry-point",
        "dts.hash",
        "dts.id",
        "dts.taxonomy",
        "dts.taxonomy-name",
        "dts.version",
        "report.accession",
        "report.hash",
        "report.id",
    ]
]
"""All fields with type information for the dts/network endpoint."""


DtsNetworkEndpoint = Literal["/dts/{dts.id}/network", "/dts/{dts.id}/network/search"]
"""Valid endpoint identifiers for the dts/network endpoint.
Can be either the endpoint key or the full path."""


class DtsNetworkSorts(TypedDict, total=False):
    """Sort Fields for dts/network endpoint response data

    Example:
        >>> data: DtsNetworkSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_hash: NotRequired[Literal["asc", "desc"]]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_taxonomy: NotRequired[Literal["asc", "desc"]]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy_name: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_version: NotRequired[Literal["asc", "desc"]]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""


class EntityParameters(TypedDict, total=False):
    """Parameters for entity endpoint response data

    Example:
        >>> data: EntityParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_name: NotRequired[str]
    """The name of the entity reporting."""
    entity_ticker: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[str]
    """No definition provided"""


EntityFields = List[Literal["entity.cik", "entity.code", "entity.id", "entity.name", "entity.scheme", "entity.ticker", "entity.ticker2"]]
"""All fields with type information for the entity endpoint."""


EntityEndpoint = Literal["/entity/search", "/entity/{entity.id}"]
"""Valid endpoint identifiers for the entity endpoint.
Can be either the endpoint key or the full path."""


class EntitySorts(TypedDict, total=False):
    """Sort Fields for entity endpoint response data

    Example:
        >>> data: EntitySorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[Literal["asc", "desc"]]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""


class EntityReportParameters(TypedDict, total=False):
    """Parameters for entity/report endpoint response data

    Example:
        >>> data: EntityReportParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_id: NotRequired[int]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[str]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[str]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[str]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions_count: NotRequired[int]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[str]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[str]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_ticker: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[str]
    """No definition provided"""
    fact_accuracy_index: NotRequired[int]
    """No definition provided"""
    fact_has_dimensions: NotRequired[Literal["true", "false"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[str]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[int]
    """The unique identifier used to identify a fact."""
    fact_is_extended: NotRequired[Literal["true", "false"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_text_search: NotRequired[str]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[int]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[str]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    member_is_base: NotRequired[Literal["true", "false"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[str]
    """Local name of the member."""
    member_member_value: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[str]
    """Namespace of the member."""
    member_typed_value: NotRequired[str]
    """Typed value of the member."""
    network_arcrole_uri: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[int]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[str]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    period_calendar_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_fiscal_id: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[int]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[str]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_year: NotRequired[int]
    """The calendar year in which the facy is applicable."""
    relationship_id: NotRequired[int]
    """No definition provided"""
    relationship_order: NotRequired[str]
    """No definition provided"""
    relationship_preferred_label: NotRequired[str]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_source_name: NotRequired[str]
    """No definition provided"""
    relationship_source_namespace: NotRequired[str]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["true", "false"]]
    """No definition provided"""
    relationship_target_label: NotRequired[str]
    """No definition provided"""
    relationship_target_name: NotRequired[str]
    """No definition provided"""
    relationship_target_namespace: NotRequired[str]
    """No definition provided"""
    relationship_tree_depth: NotRequired[int]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[int]
    """No definition provided"""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["true", "false"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[int]
    """No definition provided"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[int]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[str]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[str]
    """No definition provided"""
    report_filer_category: NotRequired[str]
    """The identifier used to identify a report."""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[str]
    """No definition provided"""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["true", "false"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_period_index: NotRequired[int]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_restated: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[str]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    report_zip_url: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    unit: NotRequired[str]
    """The unit of measure associated with the fact."""


EntityReportFields = List[
    Literal[
        "concept.balance-type",
        "concept.datatype",
        "concept.id",
        "concept.is-base",
        "concept.is-monetary",
        "concept.local-name",
        "concept.namespace",
        "concept.period-type",
        "dimension-pair",
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
        "entity.code",
        "entity.id",
        "entity.name",
        "entity.scheme",
        "entity.ticker",
        "entity.ticker2",
        "fact.accuracy-index",
        "fact.decimals",
        "fact.has-dimensions",
        "fact.hash",
        "fact.id",
        "fact.inline-display-value",
        "fact.inline-is-hidden",
        "fact.inline-negated",
        "fact.inline-scale",
        "fact.is-extended",
        "fact.numerical-value",
        "fact.text-search",
        "fact.ultimus",
        "fact.ultimus-index",
        "fact.value",
        "fact.value-link",
        "fact.xml-id",
        "footnote.id",
        "footnote.lang",
        "footnote.role",
        "footnote.text",
        "member.is-base",
        "member.local-name",
        "member.member-value",
        "member.namespace",
        "member.typed-value",
        "network.arcrole-uri",
        "network.id",
        "network.link-name",
        "network.role-description",
        "network.role-description-like",
        "network.role-uri",
        "period.calendar-period",
        "period.end",
        "period.fiscal-id",
        "period.fiscal-period",
        "period.fiscal-year",
        "period.id",
        "period.instant",
        "period.start",
        "period.year",
        "relationship.id",
        "relationship.order",
        "relationship.preferred-label",
        "relationship.source-concept-id",
        "relationship.source-is-abstract",
        "relationship.source-name",
        "relationship.source-namespace",
        "relationship.target-concept-id",
        "relationship.target-datatype",
        "relationship.target-is-abstract",
        "relationship.target-label",
        "relationship.target-name",
        "relationship.target-namespace",
        "relationship.tree-depth",
        "relationship.tree-sequence",
        "relationship.weight",
        "report.accepted-timestamp",
        "report.accession",
        "report.address",
        "report.base-taxonomy",
        "report.checks-run",
        "report.creation-software",
        "report.document-index",
        "report.document-type",
        "report.documentset-num",
        "report.entity-name",
        "report.entry-type",
        "report.entry-url",
        "report.event-items",
        "report.filer-category",
        "report.filing-date",
        "report.form-type",
        "report.hash",
        "report.html-url",
        "report.id",
        "report.is-most-current",
        "report.period-end",
        "report.period-focus",
        "report.period-index",
        "report.phone",
        "report.restated",
        "report.restated-index",
        "report.sec-url",
        "report.sic-code",
        "report.source-id",
        "report.source-name",
        "report.state-of-incorporation",
        "report.submission-type",
        "report.type",
        "report.year-focus",
        "report.zip-url",
        "unit",
        "unit.denominator",
        "unit.numerator",
        "unit.qname",
    ]
]
"""All fields with type information for the entity/report endpoint."""


EntityReportEndpoint = Literal["/entity/report/search", "/entity/{entity.id}/report/search"]
"""Valid endpoint identifiers for the entity/report endpoint.
Can be either the endpoint key or the full path."""


class EntityReportSorts(TypedDict, total=False):
    """Sort Fields for entity/report endpoint response data

    Example:
        >>> data: EntityReportSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[Literal["asc", "desc"]]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_datatype: NotRequired[Literal["asc", "desc"]]
    """The datatype of the concept such as monetary or string."""
    concept_id: NotRequired[Literal["asc", "desc"]]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[Literal["asc", "desc"]]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    concept_period_type: NotRequired[Literal["asc", "desc"]]
    """The period type of the concept. This can be either duration or instant."""
    dimension_pair: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[Literal["asc", "desc"]]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[Literal["asc", "desc"]]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions: NotRequired[Literal["asc", "desc"]]
    """Returns an array of dimensions associated with the given fact."""
    dimensions_count: NotRequired[Literal["asc", "desc"]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[Literal["asc", "desc"]]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[Literal["asc", "desc"]]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_accuracy_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_decimals: NotRequired[Literal["asc", "desc"]]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_has_dimensions: NotRequired[Literal["asc", "desc"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[Literal["asc", "desc"]]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier used to identify a fact."""
    fact_inline_display_value: NotRequired[Literal["asc", "desc"]]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_is_hidden: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_negated: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_scale: NotRequired[Literal["asc", "desc"]]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_is_extended: NotRequired[Literal["asc", "desc"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_numerical_value: NotRequired[Literal["asc", "desc"]]
    """The numerical value of the fact that was reported. """
    fact_text_search: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[Literal["asc", "desc"]]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[Literal["asc", "desc"]]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value_link: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Will return the actual text."""
    fact_xml_id: NotRequired[Literal["asc", "desc"]]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    footnote_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier to identify a footnote."""
    footnote_lang: NotRequired[Literal["asc", "desc"]]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_role: NotRequired[Literal["asc", "desc"]]
    """The role used for the footnote."""
    footnote_text: NotRequired[Literal["asc", "desc"]]
    """The text content of the footnote."""
    member_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[Literal["asc", "desc"]]
    """Local name of the member."""
    member_member_value: NotRequired[Literal["asc", "desc"]]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[Literal["asc", "desc"]]
    """Namespace of the member."""
    member_typed_value: NotRequired[Literal["asc", "desc"]]
    """Typed value of the member."""
    network_arcrole_uri: NotRequired[Literal["asc", "desc"]]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[Literal["asc", "desc"]]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[Literal["asc", "desc"]]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[Literal["asc", "desc"]]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    period_calendar_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_end: NotRequired[Literal["asc", "desc"]]
    """Period end date of the fact if applicable"""
    period_fiscal_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[Literal["asc", "desc"]]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[Literal["asc", "desc"]]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_start: NotRequired[Literal["asc", "desc"]]
    """Period start date of the fact if applicable"""
    period_year: NotRequired[Literal["asc", "desc"]]
    """The calendar year in which the facy is applicable."""
    relationship_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_order: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_preferred_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_datatype: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_depth: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_weight: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_accepted_timestamp: NotRequired[Literal["asc", "desc"]]
    """Date that the report was accepted at the regulator."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_address: NotRequired[Literal["asc", "desc"]]
    """Physical address of the reporting entity."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["asc", "desc"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[Literal["asc", "desc"]]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[Literal["asc", "desc"]]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_filer_category: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["asc", "desc"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_end: NotRequired[Literal["asc", "desc"]]
    """The period end date or balance date associated with a given report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_period_index: NotRequired[Literal["asc", "desc"]]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_phone: NotRequired[Literal["asc", "desc"]]
    """The phone number of the submitter of the report."""
    report_restated: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[Literal["asc", "desc"]]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    report_state_of_incorporation: NotRequired[Literal["asc", "desc"]]
    """The state of incorporation for the entity submitting the report."""
    report_submission_type: NotRequired[Literal["asc", "desc"]]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_type: NotRequired[Literal["asc", "desc"]]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    report_zip_url: NotRequired[Literal["asc", "desc"]]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    unit: NotRequired[Literal["asc", "desc"]]
    """The unit of measure associated with the fact."""
    unit_denominator: NotRequired[Literal["asc", "desc"]]
    """The unit of measure used as the denominator for a fact"""
    unit_numerator: NotRequired[Literal["asc", "desc"]]
    """the unit of measure used as the numerator for a fact"""
    unit_qname: NotRequired[Literal["asc", "desc"]]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""


class FactParameters(TypedDict, total=False):
    """Parameters for fact endpoint response data

    Example:
        >>> data: FactParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_id: NotRequired[int]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[str]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[str]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[str]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions_count: NotRequired[int]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[str]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[str]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    fact_accuracy_index: NotRequired[int]
    """No definition provided"""
    fact_has_dimensions: NotRequired[Literal["true", "false"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[str]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[int]
    """The unique identifier used to identify a fact."""
    fact_is_extended: NotRequired[Literal["true", "false"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_text_search: NotRequired[str]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[int]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[str]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    member_is_base: NotRequired[Literal["true", "false"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[str]
    """Local name of the member."""
    member_member_value: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[str]
    """Namespace of the member."""
    member_typed_value: NotRequired[str]
    """Typed value of the member."""
    period_calendar_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_fiscal_id: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[int]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[str]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_year: NotRequired[int]
    """The calendar year in which the facy is applicable."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[int]
    """No definition provided"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[int]
    """The number of inline xbrl documents associated with the filing."""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[str]
    """No definition provided"""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[str]
    """No definition provided"""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["true", "false"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_restated: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[str]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    unit: NotRequired[str]
    """The unit of measure associated with the fact."""


FactFields = List[
    Literal[
        "concept.balance-type",
        "concept.datatype",
        "concept.id",
        "concept.is-base",
        "concept.is-monetary",
        "concept.local-name",
        "concept.namespace",
        "concept.period-type",
        "dimension-pair",
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
        "entity.code",
        "entity.id",
        "entity.name",
        "entity.scheme",
        "fact.accuracy-index",
        "fact.decimals",
        "fact.has-dimensions",
        "fact.hash",
        "fact.id",
        "fact.inline-display-value",
        "fact.inline-is-hidden",
        "fact.inline-negated",
        "fact.inline-scale",
        "fact.is-extended",
        "fact.numerical-value",
        "fact.text-search",
        "fact.ultimus",
        "fact.ultimus-index",
        "fact.value",
        "fact.value-link",
        "fact.xml-id",
        "footnote.id",
        "footnote.lang",
        "footnote.role",
        "footnote.text",
        "member.is-base",
        "member.local-name",
        "member.member-value",
        "member.namespace",
        "member.typed-value",
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
        "report.document-index",
        "report.document-type",
        "report.documentset-num",
        "report.entry-url",
        "report.event-items",
        "report.filing-date",
        "report.form-type",
        "report.hash",
        "report.html-url",
        "report.id",
        "report.is-most-current",
        "report.period-end",
        "report.period-focus",
        "report.restated",
        "report.restated-index",
        "report.sec-url",
        "report.sic-code",
        "report.source-id",
        "report.source-name",
        "report.submission-type",
        "report.type",
        "report.year-focus",
        "unit",
        "unit.denominator",
        "unit.numerator",
        "unit.qname",
    ]
]
"""All fields with type information for the fact endpoint."""


FactEndpoint = Literal["/fact/oim/search", "/fact/search", "/fact/{fact.id}"]
"""Valid endpoint identifiers for the fact endpoint.
Can be either the endpoint key or the full path."""


class FactSorts(TypedDict, total=False):
    """Sort Fields for fact endpoint response data

    Example:
        >>> data: FactSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[Literal["asc", "desc"]]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_datatype: NotRequired[Literal["asc", "desc"]]
    """The datatype of the concept such as monetary or string."""
    concept_id: NotRequired[Literal["asc", "desc"]]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[Literal["asc", "desc"]]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    concept_period_type: NotRequired[Literal["asc", "desc"]]
    """The period type of the concept. This can be either duration or instant."""
    dimension_pair: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[Literal["asc", "desc"]]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[Literal["asc", "desc"]]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions: NotRequired[Literal["asc", "desc"]]
    """Returns an array of dimensions associated with the given fact."""
    dimensions_count: NotRequired[Literal["asc", "desc"]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[Literal["asc", "desc"]]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    fact_accuracy_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_decimals: NotRequired[Literal["asc", "desc"]]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_has_dimensions: NotRequired[Literal["asc", "desc"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[Literal["asc", "desc"]]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier used to identify a fact."""
    fact_inline_display_value: NotRequired[Literal["asc", "desc"]]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_is_hidden: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_negated: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_scale: NotRequired[Literal["asc", "desc"]]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_is_extended: NotRequired[Literal["asc", "desc"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_numerical_value: NotRequired[Literal["asc", "desc"]]
    """The numerical value of the fact that was reported. """
    fact_text_search: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[Literal["asc", "desc"]]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[Literal["asc", "desc"]]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value_link: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Will return the actual text."""
    fact_xml_id: NotRequired[Literal["asc", "desc"]]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    footnote_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier to identify a footnote."""
    footnote_lang: NotRequired[Literal["asc", "desc"]]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_role: NotRequired[Literal["asc", "desc"]]
    """The role used for the footnote."""
    footnote_text: NotRequired[Literal["asc", "desc"]]
    """The text content of the footnote."""
    member_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[Literal["asc", "desc"]]
    """Local name of the member."""
    member_member_value: NotRequired[Literal["asc", "desc"]]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[Literal["asc", "desc"]]
    """Namespace of the member."""
    member_typed_value: NotRequired[Literal["asc", "desc"]]
    """Typed value of the member."""
    period_calendar_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_end: NotRequired[Literal["asc", "desc"]]
    """Period end date of the fact if applicable"""
    period_fiscal_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[Literal["asc", "desc"]]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[Literal["asc", "desc"]]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_start: NotRequired[Literal["asc", "desc"]]
    """Period start date of the fact if applicable"""
    period_year: NotRequired[Literal["asc", "desc"]]
    """The calendar year in which the facy is applicable."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[Literal["asc", "desc"]]
    """The number of inline xbrl documents associated with the filing."""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["asc", "desc"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_end: NotRequired[Literal["asc", "desc"]]
    """The period end date or balance date associated with a given report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_restated: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[Literal["asc", "desc"]]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[Literal["asc", "desc"]]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_type: NotRequired[Literal["asc", "desc"]]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    unit: NotRequired[Literal["asc", "desc"]]
    """The unit of measure associated with the fact."""
    unit_denominator: NotRequired[Literal["asc", "desc"]]
    """The unit of measure used as the denominator for a fact"""
    unit_numerator: NotRequired[Literal["asc", "desc"]]
    """the unit of measure used as the numerator for a fact"""
    unit_qname: NotRequired[Literal["asc", "desc"]]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""


class LabelParameters(TypedDict, total=False):
    """Parameters for label endpoint response data

    Example:
        >>> data: LabelParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_id: NotRequired[int]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_abstract: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_local_name: NotRequired[str]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    label_role: NotRequired[str]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_text: NotRequired[str]
    """The text of the label. i.e Assets, Current"""


LabelFields = List[
    Literal[
        "concept.id",
        "concept.is-abstract",
        "concept.local-name",
        "concept.namespace",
        "dts.entry-point",
        "dts.id",
        "label.id",
        "label.lang",
        "label.role",
        "label.role-short",
        "label.text",
    ]
]
"""All fields with type information for the label endpoint."""


LabelEndpoint = Literal["/label/search", "/label/{label.id}/search"]
"""Valid endpoint identifiers for the label endpoint.
Can be either the endpoint key or the full path."""


class LabelSorts(TypedDict, total=False):
    """Sort Fields for label endpoint response data

    Example:
        >>> data: LabelSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_id: NotRequired[Literal["asc", "desc"]]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_abstract: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_local_name: NotRequired[Literal["asc", "desc"]]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    label_id: NotRequired[Literal["asc", "desc"]]
    """Unique ID of the label."""
    label_lang: NotRequired[Literal["asc", "desc"]]
    """The ISO language code used to express the label, such as en-us."""
    label_role: NotRequired[Literal["asc", "desc"]]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_role_short: NotRequired[Literal["asc", "desc"]]
    """The suffix of the label role used to identify the label type i.e. label"""
    label_text: NotRequired[Literal["asc", "desc"]]
    """The text of the label. i.e Assets, Current"""


class NetworkParameters(TypedDict, total=False):
    """Parameters for network endpoint response data

    Example:
        >>> data: NetworkParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[int]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[str]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""


NetworkFields = List[
    Literal[
        "dts.entry-point",
        "dts.id",
        "network.arcrole-uri",
        "network.id",
        "network.link-name",
        "network.role-description",
        "network.role-description-like",
        "network.role-uri",
    ]
]
"""All fields with type information for the network endpoint."""


NetworkEndpoint = Literal["/network/{network.id}"]
"""Valid endpoint identifiers for the network endpoint.
Can be either the endpoint key or the full path."""


class NetworkSorts(TypedDict, total=False):
    """Sort Fields for network endpoint response data

    Example:
        >>> data: NetworkSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[Literal["asc", "desc"]]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[Literal["asc", "desc"]]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[Literal["asc", "desc"]]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[Literal["asc", "desc"]]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""


class NetworkRelationshipParameters(TypedDict, total=False):
    """Parameters for network/relationship endpoint response data

    Example:
        >>> data: NetworkRelationshipParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[int]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[str]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    relationship_id: NotRequired[int]
    """No definition provided"""
    relationship_order: NotRequired[str]
    """No definition provided"""
    relationship_preferred_label: NotRequired[str]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_source_name: NotRequired[str]
    """No definition provided"""
    relationship_source_namespace: NotRequired[str]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["true", "false"]]
    """No definition provided"""
    relationship_target_label: NotRequired[str]
    """No definition provided"""
    relationship_target_name: NotRequired[str]
    """No definition provided"""
    relationship_target_namespace: NotRequired[str]
    """No definition provided"""
    relationship_tree_depth: NotRequired[int]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[int]
    """No definition provided"""


NetworkRelationshipFields = List[
    Literal[
        "dts.entry-point",
        "dts.id",
        "network.arcrole-uri",
        "network.id",
        "network.link-name",
        "network.role-description",
        "network.role-description-like",
        "network.role-uri",
        "relationship.id",
        "relationship.order",
        "relationship.preferred-label",
        "relationship.source-concept-id",
        "relationship.source-is-abstract",
        "relationship.source-name",
        "relationship.source-namespace",
        "relationship.target-concept-id",
        "relationship.target-datatype",
        "relationship.target-is-abstract",
        "relationship.target-label",
        "relationship.target-name",
        "relationship.target-namespace",
        "relationship.tree-depth",
        "relationship.tree-sequence",
        "relationship.weight",
    ]
]
"""All fields with type information for the network/relationship endpoint."""


NetworkRelationshipEndpoint = Literal["/network/relationship/search", "/network/{network.id}/relationship/search"]
"""Valid endpoint identifiers for the network/relationship endpoint.
Can be either the endpoint key or the full path."""


class NetworkRelationshipSorts(TypedDict, total=False):
    """Sort Fields for network/relationship endpoint response data

    Example:
        >>> data: NetworkRelationshipSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[Literal["asc", "desc"]]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[Literal["asc", "desc"]]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[Literal["asc", "desc"]]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[Literal["asc", "desc"]]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    relationship_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_order: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_preferred_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_datatype: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_depth: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_weight: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""


class RelationshipParameters(TypedDict, total=False):
    """Parameters for relationship endpoint response data

    Example:
        >>> data: RelationshipParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[int]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[str]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    relationship_id: NotRequired[int]
    """No definition provided"""
    relationship_order: NotRequired[str]
    """No definition provided"""
    relationship_preferred_label: NotRequired[str]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_source_name: NotRequired[str]
    """No definition provided"""
    relationship_source_namespace: NotRequired[str]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[int]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["true", "false"]]
    """No definition provided"""
    relationship_target_label: NotRequired[str]
    """No definition provided"""
    relationship_target_name: NotRequired[str]
    """No definition provided"""
    relationship_target_namespace: NotRequired[str]
    """No definition provided"""
    relationship_tree_depth: NotRequired[int]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[int]
    """No definition provided"""


RelationshipFields = List[
    Literal[
        "dts.id",
        "network.arcrole-uri",
        "network.id",
        "network.link-name",
        "network.role-description",
        "network.role-description-like",
        "network.role-uri",
        "relationship.id",
        "relationship.order",
        "relationship.preferred-label",
        "relationship.source-concept-id",
        "relationship.source-is-abstract",
        "relationship.source-name",
        "relationship.source-namespace",
        "relationship.target-concept-id",
        "relationship.target-datatype",
        "relationship.target-is-abstract",
        "relationship.target-label",
        "relationship.target-name",
        "relationship.target-namespace",
        "relationship.tree-depth",
        "relationship.tree-sequence",
        "relationship.weight",
    ]
]
"""All fields with type information for the relationship endpoint."""


RelationshipEndpoint = Literal["/relationship/search", "/relationship/tree/search"]
"""Valid endpoint identifiers for the relationship endpoint.
Can be either the endpoint key or the full path."""


class RelationshipSorts(TypedDict, total=False):
    """Sort Fields for relationship endpoint response data

    Example:
        >>> data: RelationshipSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    network_arcrole_uri: NotRequired[Literal["asc", "desc"]]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[Literal["asc", "desc"]]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[Literal["asc", "desc"]]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[Literal["asc", "desc"]]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    relationship_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_order: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_preferred_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_source_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_concept_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_datatype: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_is_abstract: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_label: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_name: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_target_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_depth: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_tree_sequence: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    relationship_weight: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""


class ReportParameters(TypedDict, total=False):
    """Parameters for report endpoint response data

    Example:
        >>> data: ReportParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_scheme: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[str]
    """No definition provided"""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["true", "false"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[int]
    """No definition provided"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[int]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[str]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[str]
    """No definition provided"""
    report_filer_category: NotRequired[str]
    """The identifier used to identify a report."""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[str]
    """No definition provided"""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["true", "false"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_period_index: NotRequired[int]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_restated: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[int]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    report_zip_url: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""


ReportFields = List[
    Literal[
        "dts.id",
        "entity.cik",
        "entity.code",
        "entity.id",
        "entity.scheme",
        "entity.ticker",
        "entity.ticker2",
        "report.accepted-timestamp",
        "report.accession",
        "report.address",
        "report.base-taxonomy",
        "report.checks-run",
        "report.creation-software",
        "report.document-index",
        "report.document-type",
        "report.documentset-num",
        "report.entity-name",
        "report.entry-type",
        "report.entry-url",
        "report.event-items",
        "report.filer-category",
        "report.filing-date",
        "report.form-type",
        "report.hash",
        "report.html-url",
        "report.id",
        "report.is-most-current",
        "report.period-end",
        "report.period-focus",
        "report.period-index",
        "report.phone",
        "report.restated",
        "report.restated-index",
        "report.sec-url",
        "report.sic-code",
        "report.source-id",
        "report.source-name",
        "report.state-of-incorporation",
        "report.submission-type",
        "report.year-focus",
        "report.zip-url",
    ]
]
"""All fields with type information for the report endpoint."""


ReportEndpoint = Literal["/report/search", "/report/{report.id}"]
"""Valid endpoint identifiers for the report endpoint.
Can be either the endpoint key or the full path."""


class ReportSorts(TypedDict, total=False):
    """Sort Fields for report endpoint response data

    Example:
        >>> data: ReportSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[Literal["asc", "desc"]]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_accepted_timestamp: NotRequired[Literal["asc", "desc"]]
    """Date that the report was accepted at the regulator."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_address: NotRequired[Literal["asc", "desc"]]
    """Physical address of the reporting entity."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["asc", "desc"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[Literal["asc", "desc"]]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[Literal["asc", "desc"]]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_filer_category: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["asc", "desc"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_end: NotRequired[Literal["asc", "desc"]]
    """The period end date or balance date associated with a given report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_period_index: NotRequired[Literal["asc", "desc"]]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_phone: NotRequired[Literal["asc", "desc"]]
    """The phone number of the submitter of the report."""
    report_restated: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[Literal["asc", "desc"]]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    report_state_of_incorporation: NotRequired[Literal["asc", "desc"]]
    """The state of incorporation for the entity submitting the report."""
    report_submission_type: NotRequired[Literal["asc", "desc"]]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    report_zip_url: NotRequired[Literal["asc", "desc"]]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""


class ReportFactParameters(TypedDict, total=False):
    """Parameters for report/fact endpoint response data

    Example:
        >>> data: ReportFactParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_id: NotRequired[int]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["true", "false"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[str]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[str]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[str]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions_count: NotRequired[int]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[str]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[str]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_ticker: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[str]
    """No definition provided"""
    fact_accuracy_index: NotRequired[int]
    """No definition provided"""
    fact_has_dimensions: NotRequired[Literal["true", "false"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[str]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[int]
    """The unique identifier used to identify a fact."""
    fact_is_extended: NotRequired[Literal["true", "false"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_text_search: NotRequired[str]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[int]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[str]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    member_is_base: NotRequired[Literal["true", "false"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[str]
    """Local name of the member."""
    member_member_value: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[str]
    """Namespace of the member."""
    member_typed_value: NotRequired[str]
    """Typed value of the member."""
    period_calendar_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_fiscal_id: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[int]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[str]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_year: NotRequired[int]
    """The calendar year in which the facy is applicable."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["true", "false"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[int]
    """No definition provided"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[int]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[str]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[str]
    """No definition provided"""
    report_filer_category: NotRequired[str]
    """The identifier used to identify a report."""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[str]
    """No definition provided"""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["true", "false"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_period_index: NotRequired[int]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_restated: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[str]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    report_zip_url: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    unit: NotRequired[str]
    """The unit of measure associated with the fact."""


ReportFactFields = List[
    Literal[
        "concept.balance-type",
        "concept.datatype",
        "concept.id",
        "concept.is-base",
        "concept.is-monetary",
        "concept.local-name",
        "concept.namespace",
        "concept.period-type",
        "dimension-pair",
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
        "entity.code",
        "entity.id",
        "entity.name",
        "entity.scheme",
        "entity.ticker",
        "entity.ticker2",
        "fact.accuracy-index",
        "fact.decimals",
        "fact.has-dimensions",
        "fact.hash",
        "fact.id",
        "fact.inline-display-value",
        "fact.inline-is-hidden",
        "fact.inline-negated",
        "fact.inline-scale",
        "fact.is-extended",
        "fact.numerical-value",
        "fact.text-search",
        "fact.ultimus",
        "fact.ultimus-index",
        "fact.value",
        "fact.value-link",
        "fact.xml-id",
        "footnote.id",
        "footnote.lang",
        "footnote.role",
        "footnote.text",
        "member.is-base",
        "member.local-name",
        "member.member-value",
        "member.namespace",
        "member.typed-value",
        "period.calendar-period",
        "period.end",
        "period.fiscal-id",
        "period.fiscal-period",
        "period.fiscal-year",
        "period.id",
        "period.instant",
        "period.start",
        "period.year",
        "report.accepted-timestamp",
        "report.accession",
        "report.address",
        "report.base-taxonomy",
        "report.checks-run",
        "report.creation-software",
        "report.document-index",
        "report.document-type",
        "report.documentset-num",
        "report.entity-name",
        "report.entry-type",
        "report.entry-url",
        "report.event-items",
        "report.filer-category",
        "report.filing-date",
        "report.form-type",
        "report.hash",
        "report.html-url",
        "report.id",
        "report.is-most-current",
        "report.period-end",
        "report.period-focus",
        "report.period-index",
        "report.phone",
        "report.restated",
        "report.restated-index",
        "report.sec-url",
        "report.sic-code",
        "report.source-id",
        "report.source-name",
        "report.state-of-incorporation",
        "report.submission-type",
        "report.type",
        "report.year-focus",
        "report.zip-url",
        "unit",
        "unit.denominator",
        "unit.numerator",
        "unit.qname",
    ]
]
"""All fields with type information for the report/fact endpoint."""


ReportFactEndpoint = Literal["/report/fact/search", "/report/{report.id}/fact/search"]
"""Valid endpoint identifiers for the report/fact endpoint.
Can be either the endpoint key or the full path."""


class ReportFactSorts(TypedDict, total=False):
    """Sort Fields for report/fact endpoint response data

    Example:
        >>> data: ReportFactSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    concept_balance_type: NotRequired[Literal["asc", "desc"]]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_datatype: NotRequired[Literal["asc", "desc"]]
    """The datatype of the concept such as monetary or string."""
    concept_id: NotRequired[Literal["asc", "desc"]]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_is_base: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_monetary: NotRequired[Literal["asc", "desc"]]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_local_name: NotRequired[Literal["asc", "desc"]]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_namespace: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    concept_period_type: NotRequired[Literal["asc", "desc"]]
    """The period type of the concept. This can be either duration or instant."""
    dimension_pair: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    dimension_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_local_name: NotRequired[Literal["asc", "desc"]]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_namespace: NotRequired[Literal["asc", "desc"]]
    """The namespace of the dimension concept used to identify a fact."""
    dimensions: NotRequired[Literal["asc", "desc"]]
    """Returns an array of dimensions associated with the given fact."""
    dimensions_count: NotRequired[Literal["asc", "desc"]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_target_namespace: NotRequired[Literal["asc", "desc"]]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity reporting."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[Literal["asc", "desc"]]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_accuracy_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    fact_decimals: NotRequired[Literal["asc", "desc"]]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_has_dimensions: NotRequired[Literal["asc", "desc"]]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_hash: NotRequired[Literal["asc", "desc"]]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier used to identify a fact."""
    fact_inline_display_value: NotRequired[Literal["asc", "desc"]]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_is_hidden: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_negated: NotRequired[Literal["asc", "desc"]]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_scale: NotRequired[Literal["asc", "desc"]]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_is_extended: NotRequired[Literal["asc", "desc"]]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_numerical_value: NotRequired[Literal["asc", "desc"]]
    """The numerical value of the fact that was reported. """
    fact_text_search: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_ultimus: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus_index: NotRequired[Literal["asc", "desc"]]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_value: NotRequired[Literal["asc", "desc"]]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value_link: NotRequired[Literal["asc", "desc"]]
    """Used to define text in a text search. Will return the actual text."""
    fact_xml_id: NotRequired[Literal["asc", "desc"]]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    footnote_id: NotRequired[Literal["asc", "desc"]]
    """The unique identifier to identify a footnote."""
    footnote_lang: NotRequired[Literal["asc", "desc"]]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_role: NotRequired[Literal["asc", "desc"]]
    """The role used for the footnote."""
    footnote_text: NotRequired[Literal["asc", "desc"]]
    """The text content of the footnote."""
    member_is_base: NotRequired[Literal["asc", "desc"]]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_local_name: NotRequired[Literal["asc", "desc"]]
    """Local name of the member."""
    member_member_value: NotRequired[Literal["asc", "desc"]]
    """Typed value or local-name of the member depending on the dimension type."""
    member_namespace: NotRequired[Literal["asc", "desc"]]
    """Namespace of the member."""
    member_typed_value: NotRequired[Literal["asc", "desc"]]
    """Typed value of the member."""
    period_calendar_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_end: NotRequired[Literal["asc", "desc"]]
    """Period end date of the fact if applicable"""
    period_fiscal_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_period: NotRequired[Literal["asc", "desc"]]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_year: NotRequired[Literal["asc", "desc"]]
    """The fiscal year in which the fact is applicable."""
    period_id: NotRequired[Literal["asc", "desc"]]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_instant: NotRequired[Literal["asc", "desc"]]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_start: NotRequired[Literal["asc", "desc"]]
    """Period start date of the fact if applicable"""
    period_year: NotRequired[Literal["asc", "desc"]]
    """The calendar year in which the facy is applicable."""
    report_accepted_timestamp: NotRequired[Literal["asc", "desc"]]
    """Date that the report was accepted at the regulator."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_address: NotRequired[Literal["asc", "desc"]]
    """Physical address of the reporting entity."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["asc", "desc"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[Literal["asc", "desc"]]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[Literal["asc", "desc"]]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_filer_category: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["asc", "desc"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_end: NotRequired[Literal["asc", "desc"]]
    """The period end date or balance date associated with a given report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_period_index: NotRequired[Literal["asc", "desc"]]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_phone: NotRequired[Literal["asc", "desc"]]
    """The phone number of the submitter of the report."""
    report_restated: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[Literal["asc", "desc"]]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    report_state_of_incorporation: NotRequired[Literal["asc", "desc"]]
    """The state of incorporation for the entity submitting the report."""
    report_submission_type: NotRequired[Literal["asc", "desc"]]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_type: NotRequired[Literal["asc", "desc"]]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    report_zip_url: NotRequired[Literal["asc", "desc"]]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    unit: NotRequired[Literal["asc", "desc"]]
    """The unit of measure associated with the fact."""
    unit_denominator: NotRequired[Literal["asc", "desc"]]
    """The unit of measure used as the denominator for a fact"""
    unit_numerator: NotRequired[Literal["asc", "desc"]]
    """the unit of measure used as the numerator for a fact"""
    unit_qname: NotRequired[Literal["asc", "desc"]]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""


class ReportNetworkParameters(TypedDict, total=False):
    """Parameters for report/network endpoint response data

    Example:
        >>> data: ReportNetworkParameters = {
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[int]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_scheme: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[str]
    """No definition provided"""
    network_arcrole_uri: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[int]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[str]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    report_accession: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_base_taxonomy: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["true", "false"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[int]
    """No definition provided"""
    report_document_type: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[int]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[str]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[str]
    """No definition provided"""
    report_filer_category: NotRequired[str]
    """The identifier used to identify a report."""
    report_form_type: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[str]
    """No definition provided"""
    report_id: NotRequired[int]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["true", "false"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_focus: NotRequired[str]
    """The period the report was reported for."""
    report_period_index: NotRequired[int]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_restated: NotRequired[Literal["true", "false"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[int]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[int]
    """No definition provided"""
    report_source_name: NotRequired[str]
    """Name of the source of the data such as SEC."""
    report_submission_type: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[str]
    """The year the report was reported for."""
    report_zip_url: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""


ReportNetworkFields = List[
    Literal[
        "dts.entry-point",
        "dts.id",
        "entity.cik",
        "entity.code",
        "entity.id",
        "entity.scheme",
        "entity.ticker",
        "entity.ticker2",
        "network.arcrole-uri",
        "network.id",
        "network.link-name",
        "network.role-description",
        "network.role-description-like",
        "network.role-uri",
        "report.accepted-timestamp",
        "report.accession",
        "report.address",
        "report.base-taxonomy",
        "report.checks-run",
        "report.creation-software",
        "report.document-index",
        "report.document-type",
        "report.documentset-num",
        "report.entity-name",
        "report.entry-type",
        "report.entry-url",
        "report.event-items",
        "report.filer-category",
        "report.filing-date",
        "report.form-type",
        "report.hash",
        "report.html-url",
        "report.id",
        "report.is-most-current",
        "report.period-end",
        "report.period-focus",
        "report.period-index",
        "report.phone",
        "report.restated",
        "report.restated-index",
        "report.sec-url",
        "report.sic-code",
        "report.source-id",
        "report.source-name",
        "report.state-of-incorporation",
        "report.submission-type",
        "report.year-focus",
        "report.zip-url",
    ]
]
"""All fields with type information for the report/network endpoint."""


ReportNetworkEndpoint = Literal["/report/network/search"]
"""Valid endpoint identifiers for the report/network endpoint.
Can be either the endpoint key or the full path."""


class ReportNetworkSorts(TypedDict, total=False):
    """Sort Fields for report/network endpoint response data

    Example:
        >>> data: ReportNetworkSorts = {
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """

    dts_entry_point: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_id: NotRequired[Literal["asc", "desc"]]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    entity_cik: NotRequired[Literal["asc", "desc"]]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[Literal["asc", "desc"]]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_id: NotRequired[Literal["asc", "desc"]]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_scheme: NotRequired[Literal["asc", "desc"]]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_ticker: NotRequired[Literal["asc", "desc"]]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker2: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    network_arcrole_uri: NotRequired[Literal["asc", "desc"]]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_id: NotRequired[Literal["asc", "desc"]]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_link_name: NotRequired[Literal["asc", "desc"]]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_role_description: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description_like: NotRequired[Literal["asc", "desc"]]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_uri: NotRequired[Literal["asc", "desc"]]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    report_accepted_timestamp: NotRequired[Literal["asc", "desc"]]
    """Date that the report was accepted at the regulator."""
    report_accession: NotRequired[Literal["asc", "desc"]]
    """The identifier used by the SEC to identify a report."""
    report_address: NotRequired[Literal["asc", "desc"]]
    """Physical address of the reporting entity."""
    report_base_taxonomy: NotRequired[Literal["asc", "desc"]]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_checks_run: NotRequired[Literal["asc", "desc"]]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_creation_software: NotRequired[Literal["asc", "desc"]]
    """The creation software that was used to create a report/"""
    report_document_index: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_document_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_documentset_num: NotRequired[Literal["asc", "desc"]]
    """The number of inline xbrl documents associated with the filing."""
    report_entity_name: NotRequired[Literal["asc", "desc"]]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entry_type: NotRequired[Literal["asc", "desc"]]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_url: NotRequired[Literal["asc", "desc"]]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_event_items: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_filer_category: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_filing_date: NotRequired[Literal["asc", "desc"]]
    """The date that the filing was published."""
    report_form_type: NotRequired[Literal["asc", "desc"]]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_hash: NotRequired[Literal["asc", "desc"]]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_html_url: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_id: NotRequired[Literal["asc", "desc"]]
    """The identifier used to identify a report."""
    report_is_most_current: NotRequired[Literal["asc", "desc"]]
    """A boolean indicator for whether the report is the most current (true)."""
    report_period_end: NotRequired[Literal["asc", "desc"]]
    """The period end date or balance date associated with a given report."""
    report_period_focus: NotRequired[Literal["asc", "desc"]]
    """The period the report was reported for."""
    report_period_index: NotRequired[Literal["asc", "desc"]]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_phone: NotRequired[Literal["asc", "desc"]]
    """The phone number of the submitter of the report."""
    report_restated: NotRequired[Literal["asc", "desc"]]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated_index: NotRequired[Literal["asc", "desc"]]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_sec_url: NotRequired[Literal["asc", "desc"]]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sic_code: NotRequired[Literal["asc", "desc"]]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_source_id: NotRequired[Literal["asc", "desc"]]
    """No definition provided"""
    report_source_name: NotRequired[Literal["asc", "desc"]]
    """Name of the source of the data such as SEC."""
    report_state_of_incorporation: NotRequired[Literal["asc", "desc"]]
    """The state of incorporation for the entity submitting the report."""
    report_submission_type: NotRequired[Literal["asc", "desc"]]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_year_focus: NotRequired[Literal["asc", "desc"]]
    """The year the report was reported for."""
    report_zip_url: NotRequired[Literal["asc", "desc"]]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
