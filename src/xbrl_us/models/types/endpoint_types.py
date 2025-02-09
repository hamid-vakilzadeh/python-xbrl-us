"""This module was automatically generated. Do not edit manually."""
from typing import Any
from typing import Dict
from typing import TypedDict

from typing_extensions import NotRequired


class AssertionTypedDict(TypedDict, total=False):
    """TypedDict for assertion endpoint fields"""

    """Unique code associated with a specific error. For example: DQC.US.0073.7648"""
    assertion_code: NotRequired[str]
    """Message details for the error describing the error."""
    assertion_detail: NotRequired[str]
    """Effective date of the rule. This is the date that the rule went into effect and all companies were required to follow the rule."""
    assertion_effective_date: NotRequired[str]
    """Details of fact(s) impacted by the error, in an XML format."""
    assertion_rule_focus: NotRequired[str]
    """Date that the rule was run on the filing."""
    assertion_run_date: NotRequired[str]
    """Severity of the rule, indicated as error, warning or information."""
    assertion_severity: NotRequired[str]
    """The source of rule base that generated the rule, indicated as DQC, EFM, or xbrlus-cc."""
    assertion_source: NotRequired[str]
    """The rule number of the rule. i.e. 0099"""
    assertion_type: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """Date that the report was accepted at the regulator."""
    report_accepted_timestamp: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_base_taxonomy: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    report_filing_year: NotRequired[int]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    report_zip_url: NotRequired[str]


class ConceptTypedDict(TypedDict, total=False):
    """TypedDict for concept endpoint fields"""

    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_balance_type: NotRequired[str]
    """The datatype of the concept such as monetary or string."""
    concept_datatype: NotRequired[str]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_id: NotRequired[int]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_is_abstract: NotRequired[bool]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_is_monetary: NotRequired[bool]
    """Identifies if the concept can have a nill value."""
    concept_is_nillable: NotRequired[bool]
    """Identifies if the concept is a numeric value. If yes the value is shown as true."""
    concept_is_numeric: NotRequired[bool]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_local_name: NotRequired[str]
    concept_namespace: NotRequired[str]
    """The period type of the concept. This can be either duration or instant."""
    concept_period_type: NotRequired[str]
    """The substitution group of the concept."""
    concept_substitution: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_hash: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    dts_target_namespace: NotRequired[str]
    """Unique ID of the label."""
    label_id: NotRequired[str]
    """The ISO language code used to express the label, such as en-us."""
    label_lang: NotRequired[str]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_role: NotRequired[str]
    """The suffix of the label role used to identify the label type i.e. label"""
    label_role_short: NotRequired[str]
    """The text of the label. i.e Assets, Current"""
    label_text: NotRequired[str]
    parts_local_name: NotRequired[str]
    parts_namespace: NotRequired[str]
    parts_order: NotRequired[int]
    parts_part_value: NotRequired[str]
    """Unique ID of the reference."""
    reference_id: NotRequired[int]
    """The reference role used to identify the reference type i.e. http://fasb.org/us-gaap/role/ref/legacyRef"""
    reference_role: NotRequired[str]
    """The reference definition used to identify the reference role i.e. Legacy reference"""
    reference_role_definition: NotRequired[str]
    """The reference role used to identify the reference type i.e. legacyRef"""
    reference_role_short: NotRequired[str]


class CubeTypedDict(TypedDict, total=False):
    """TypedDict for cube endpoint fields"""

    """The dts network descrition of the cube."""
    cube_description: NotRequired[str]
    """??The cube uri for the drs role."""
    cube_drs_role_uri: NotRequired[str]
    """The identifier used to identify a cube."""
    cube_id: NotRequired[int]
    cube_member_value: NotRequired[str]
    """The primary local-name of the cube."""
    cube_primary_local_name: NotRequired[str]
    """The primary namespace of the cube."""
    cube_primary_namespace: NotRequired[str]
    """The cubes local-name for it's element."""
    cube_table_local_name: NotRequired[str]
    cube_table_namespace: NotRequired[str]
    """The depth of this item within a tree."""
    cube_tree_depth: NotRequired[int]
    """Sequence order if visualized in a tree."""
    cube_tree_sequence: NotRequired[int]
    dimension_pair: NotRequired[Dict[str, Any]]
    """Returns an array of dimensions associated with the given fact."""
    dimensions: NotRequired[Dict[str, Any]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_count: NotRequired[int]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    fact_accuracy_index: NotRequired[int]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_decimals: NotRequired[str]
    """The unique identifier used to identify a fact."""
    fact_id: NotRequired[int]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_display_value: NotRequired[str]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_is_extended: NotRequired[bool]
    """The numerical value of the fact that was reported. """
    fact_numerical_value: NotRequired[float]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus: NotRequired[bool]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_calendar_period: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_period: NotRequired[str]
    """The fiscal year in which the fact is applicable."""
    period_fiscal_year: NotRequired[int]
    """The calendar year in which the facy is applicable."""
    period_year: NotRequired[int]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entity_name: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """The unit of measure associated with the fact."""
    unit: NotRequired[str]


class DocumentTypedDict(TypedDict, total=False):
    """TypedDict for document endpoint fields"""

    """The content of the document."""
    document_content: NotRequired[str]
    """Boolean attribute that indicates if the document is part of the document set, i.e. an instant document."""
    document_documentset: NotRequired[str]
    """An internal unique identifier of the document."""
    document_id: NotRequired[int]
    """Cannot be used as a return field. Search for strings within document object (ie. to locate a specific name, topic or reference within an entire document). Fields returned include document.example and document.highlighted-value. The XBRL API uses the Sphinx search engine to identify text. This powerful search engine quickly identifies a given text string. Sphinx is enabled to support stemming, which means it will also return plurals of a noun i.e. ipad will also return ipads. It will also return the present, future and past form of a verb for example the word kill will also return killed and killing. To match the word exactly the character '=' can be placed in front of the word i.e. = ipad will return the occurrence of the word ipad only."""
    document_text_search: NotRequired[str]
    """Boolean that indicates if the file in a dts is the entry point."""
    document_top_level: NotRequired[bool]
    """Level of the files in terms of which files import or reference child files."""
    document_tree_level: NotRequired[int]
    """Order of the files in terms of how the dts is compiled from the underlying documents."""
    document_tree_order: NotRequired[int]
    """Indicates if the document is a schema, linkbase or instance."""
    document_type: NotRequired[str]
    """The url at which the document comprising the dts is located."""
    document_uri: NotRequired[str]
    """Contents of the document."""
    dts_content: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]


class DtsTypedDict(TypedDict, total=False):
    """TypedDict for dts endpoint fields"""

    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entity_name: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_hash: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    dts_version: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]


class DtsConceptTypedDict(TypedDict, total=False):
    """TypedDict for dts/concept endpoint fields"""

    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entity_name: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_hash: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    dts_version: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]


class DtsNetworkTypedDict(TypedDict, total=False):
    """TypedDict for dts/network endpoint fields"""

    """The name of the entity that the DTS is applicable to. If the DTS is non company specific this value is null."""
    dts_entity_name: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The DTS identifier for a given group of taxonomies as a hex hash. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS."""
    dts_hash: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The taxonomy group that the taxonomy belongs to such as 'US GAAP' or 'IFRS'."""
    dts_taxonomy: NotRequired[str]
    """The specific taxonomy name such as 'US GAAP 2019' or 'IFRS 2019'."""
    dts_taxonomy_name: NotRequired[str]
    """The specific taxonomy version name, such as `2019` for US GAAP."""
    dts_version: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]


class EntityTypedDict(TypedDict, total=False):
    """TypedDict for entity endpoint fields"""

    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker: NotRequired[str]
    entity_ticker2: NotRequired[str]


class EntityReportTypedDict(TypedDict, total=False):
    """TypedDict for entity/report endpoint fields"""

    aspect: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_balance_type: NotRequired[str]
    """The datatype of the concept such as monetary or string."""
    concept_datatype: NotRequired[str]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_id: NotRequired[int]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_base: NotRequired[bool]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_is_monetary: NotRequired[bool]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_local_name: NotRequired[str]
    concept_namespace: NotRequired[str]
    """The period type of the concept. This can be either duration or instant."""
    concept_period_type: NotRequired[str]
    dimension_pair: NotRequired[Dict[str, Any]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_is_base: NotRequired[bool]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_local_name: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimension_namespace: NotRequired[str]
    """Returns an array of dimensions associated with the given fact."""
    dimensions: NotRequired[Dict[str, Any]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_count: NotRequired[int]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dimensions_id: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    dts_target_namespace: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker: NotRequired[str]
    entity_ticker2: NotRequired[str]
    fact_accuracy_index: NotRequired[int]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_decimals: NotRequired[str]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_has_dimensions: NotRequired[bool]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_hash: NotRequired[str]
    """The unique identifier used to identify a fact."""
    fact_id: NotRequired[int]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_display_value: NotRequired[str]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_is_hidden: NotRequired[bool]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_negated: NotRequired[bool]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_inline_scale: NotRequired[int]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_is_extended: NotRequired[bool]
    """The numerical value of the fact that was reported. """
    fact_numerical_value: NotRequired[float]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_text_search: NotRequired[str]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus: NotRequired[bool]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_ultimus_index: NotRequired[int]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value: NotRequired[str]
    """Used to define text in a text search. Will return the actual text."""
    fact_value_link: NotRequired[str]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    fact_xml_id: NotRequired[str]
    """The unique identifier to identify a footnote."""
    footnote_id: NotRequired[str]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_lang: NotRequired[str]
    """The role used for the footnote."""
    footnote_role: NotRequired[str]
    """The text content of the footnote."""
    footnote_text: NotRequired[str]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_is_base: NotRequired[bool]
    """Local name of the member."""
    member_local_name: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_member_value: NotRequired[str]
    """Namespace of the member."""
    member_namespace: NotRequired[str]
    """Typed value of the member."""
    member_typed_value: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_arcrole_uri: NotRequired[str]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_id: NotRequired[int]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_link_name: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_description_like: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    network_role_uri: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_calendar_period: NotRequired[str]
    """Period end date of the fact if applicable"""
    period_end: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_id: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_period: NotRequired[str]
    """The fiscal year in which the fact is applicable."""
    period_fiscal_year: NotRequired[int]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_id: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_instant: NotRequired[str]
    """Period start date of the fact if applicable"""
    period_start: NotRequired[str]
    """The calendar year in which the facy is applicable."""
    period_year: NotRequired[int]
    relationship_id: NotRequired[int]
    relationship_order: NotRequired[str]
    relationship_preferred_label: NotRequired[str]
    relationship_source_concept_id: NotRequired[int]
    relationship_source_is_abstract: NotRequired[bool]
    relationship_source_name: NotRequired[str]
    relationship_source_namespace: NotRequired[str]
    relationship_target_concept_id: NotRequired[int]
    relationship_target_datatype: NotRequired[str]
    relationship_target_is_abstract: NotRequired[bool]
    relationship_target_label: NotRequired[str]
    relationship_target_name: NotRequired[str]
    relationship_target_namespace: NotRequired[str]
    relationship_tree_depth: NotRequired[int]
    relationship_tree_sequence: NotRequired[int]
    relationship_weight: NotRequired[str]
    """Date that the report was accepted at the regulator."""
    report_accepted_timestamp: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """Physical address of the reporting entity."""
    report_address: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_base_taxonomy: NotRequired[str]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_checks_run: NotRequired[bool]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    report_document_index: NotRequired[int]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The number of inline xbrl documents associated with the filing."""
    report_documentset_num: NotRequired[int]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entity_name: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_type: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    report_event_items: NotRequired[str]
    """The identifier used to identify a report."""
    report_filer_category: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    report_html_url: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """A boolean indicator for whether the report is the most current (true)."""
    report_is_most_current: NotRequired[bool]
    """The period end date or balance date associated with a given report."""
    report_period_end: NotRequired[str]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_period_index: NotRequired[int]
    """The phone number of the submitter of the report."""
    report_phone: NotRequired[str]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated: NotRequired[bool]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_restated_index: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """The state of incorporation for the entity submitting the report."""
    report_state_of_incorporation: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_submission_type: NotRequired[str]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_type: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    report_zip_url: NotRequired[str]
    """The unit of measure associated with the fact."""
    unit: NotRequired[str]
    """The unit of measure used as the denominator for a fact"""
    unit_denominator: NotRequired[str]
    """the unit of measure used as the numerator for a fact"""
    unit_numerator: NotRequired[str]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""
    unit_qname: NotRequired[str]


class FactTypedDict(TypedDict, total=False):
    """TypedDict for fact endpoint fields"""

    aspect: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_balance_type: NotRequired[str]
    """The datatype of the concept such as monetary or string."""
    concept_datatype: NotRequired[str]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_id: NotRequired[int]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_base: NotRequired[bool]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_is_monetary: NotRequired[bool]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_local_name: NotRequired[str]
    concept_namespace: NotRequired[str]
    """The period type of the concept. This can be either duration or instant."""
    concept_period_type: NotRequired[str]
    dimension_pair: NotRequired[Dict[str, Any]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_is_base: NotRequired[bool]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_local_name: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimension_namespace: NotRequired[str]
    """Returns an array of dimensions associated with the given fact."""
    dimensions: NotRequired[Dict[str, Any]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_count: NotRequired[int]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dimensions_id: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    dts_target_namespace: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    fact_accuracy_index: NotRequired[int]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_decimals: NotRequired[str]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_has_dimensions: NotRequired[bool]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_hash: NotRequired[str]
    """The unique identifier used to identify a fact."""
    fact_id: NotRequired[int]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_display_value: NotRequired[str]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_is_hidden: NotRequired[bool]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_negated: NotRequired[bool]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_inline_scale: NotRequired[int]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_is_extended: NotRequired[bool]
    """The numerical value of the fact that was reported. """
    fact_numerical_value: NotRequired[float]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_text_search: NotRequired[str]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus: NotRequired[bool]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_ultimus_index: NotRequired[int]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value: NotRequired[str]
    """Used to define text in a text search. Will return the actual text."""
    fact_value_link: NotRequired[str]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    fact_xml_id: NotRequired[str]
    """The unique identifier to identify a footnote."""
    footnote_id: NotRequired[str]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_lang: NotRequired[str]
    """The role used for the footnote."""
    footnote_role: NotRequired[str]
    """The text content of the footnote."""
    footnote_text: NotRequired[str]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_is_base: NotRequired[bool]
    """Local name of the member."""
    member_local_name: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_member_value: NotRequired[str]
    """Namespace of the member."""
    member_namespace: NotRequired[str]
    """Typed value of the member."""
    member_typed_value: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_calendar_period: NotRequired[str]
    """Period end date of the fact if applicable"""
    period_end: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_id: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_period: NotRequired[str]
    """The fiscal year in which the fact is applicable."""
    period_fiscal_year: NotRequired[int]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_id: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_instant: NotRequired[str]
    """Period start date of the fact if applicable"""
    period_start: NotRequired[str]
    """The calendar year in which the facy is applicable."""
    period_year: NotRequired[int]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    report_document_index: NotRequired[int]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The number of inline xbrl documents associated with the filing."""
    report_documentset_num: NotRequired[int]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    report_event_items: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    report_html_url: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """A boolean indicator for whether the report is the most current (true)."""
    report_is_most_current: NotRequired[bool]
    """The period end date or balance date associated with a given report."""
    report_period_end: NotRequired[str]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated: NotRequired[bool]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_restated_index: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_submission_type: NotRequired[str]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_type: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The unit of measure associated with the fact."""
    unit: NotRequired[str]
    """The unit of measure used as the denominator for a fact"""
    unit_denominator: NotRequired[str]
    """the unit of measure used as the numerator for a fact"""
    unit_numerator: NotRequired[str]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""
    unit_qname: NotRequired[str]


class LabelTypedDict(TypedDict, total=False):
    """TypedDict for label endpoint fields"""

    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_id: NotRequired[int]
    """Identifies if the concept is an abstract concept. If a primary concept (Not an axis or dimension) is an abstract it cannot have a value associated with it."""
    concept_is_abstract: NotRequired[bool]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_local_name: NotRequired[str]
    concept_namespace: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """Unique ID of the label."""
    label_id: NotRequired[str]
    """The ISO language code used to express the label, such as en-us."""
    label_lang: NotRequired[str]
    """The label role used to identify the label type i.e. http://www.xbrl.org/2003/role/label, http://www.xbrl.org/2003/role/documentation"""
    label_role: NotRequired[str]
    """The suffix of the label role used to identify the label type i.e. label"""
    label_role_short: NotRequired[str]
    """The text of the label. i.e Assets, Current"""
    label_text: NotRequired[str]


class NetworkTypedDict(TypedDict, total=False):
    """TypedDict for network endpoint fields"""

    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_arcrole_uri: NotRequired[str]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_id: NotRequired[int]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_link_name: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_description_like: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    network_role_uri: NotRequired[str]


class NetworkRelationshipTypedDict(TypedDict, total=False):
    """TypedDict for network/relationship endpoint fields"""

    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_arcrole_uri: NotRequired[str]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_id: NotRequired[int]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_link_name: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_description_like: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    network_role_uri: NotRequired[str]
    relationship_id: NotRequired[int]
    relationship_order: NotRequired[str]
    relationship_preferred_label: NotRequired[str]
    relationship_source_concept_id: NotRequired[int]
    relationship_source_is_abstract: NotRequired[bool]
    relationship_source_name: NotRequired[str]
    relationship_source_namespace: NotRequired[str]
    relationship_target_concept_id: NotRequired[int]
    relationship_target_datatype: NotRequired[str]
    relationship_target_is_abstract: NotRequired[bool]
    relationship_target_label: NotRequired[str]
    relationship_target_name: NotRequired[str]
    relationship_target_namespace: NotRequired[str]
    relationship_tree_depth: NotRequired[int]
    relationship_tree_sequence: NotRequired[int]
    relationship_weight: NotRequired[str]


class RelationshipTypedDict(TypedDict, total=False):
    """TypedDict for relationship endpoint fields"""

    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_arcrole_uri: NotRequired[str]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_id: NotRequired[int]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_link_name: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_description_like: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    network_role_uri: NotRequired[str]
    relationship_id: NotRequired[int]
    relationship_order: NotRequired[str]
    relationship_preferred_label: NotRequired[str]
    relationship_source_concept_id: NotRequired[int]
    relationship_source_is_abstract: NotRequired[bool]
    relationship_source_name: NotRequired[str]
    relationship_source_namespace: NotRequired[str]
    relationship_target_concept_id: NotRequired[int]
    relationship_target_datatype: NotRequired[str]
    relationship_target_is_abstract: NotRequired[bool]
    relationship_target_label: NotRequired[str]
    relationship_target_name: NotRequired[str]
    relationship_target_namespace: NotRequired[str]
    relationship_tree_depth: NotRequired[int]
    relationship_tree_sequence: NotRequired[int]
    relationship_weight: NotRequired[str]


class ReportTypedDict(TypedDict, total=False):
    """TypedDict for report endpoint fields"""

    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker: NotRequired[str]
    entity_ticker2: NotRequired[str]
    """Date that the report was accepted at the regulator."""
    report_accepted_timestamp: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """Physical address of the reporting entity."""
    report_address: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_base_taxonomy: NotRequired[str]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_checks_run: NotRequired[bool]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    report_document_index: NotRequired[int]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The number of inline xbrl documents associated with the filing."""
    report_documentset_num: NotRequired[int]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entity_name: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_type: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    report_event_items: NotRequired[str]
    """The identifier used to identify a report."""
    report_filer_category: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    report_html_url: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """A boolean indicator for whether the report is the most current (true)."""
    report_is_most_current: NotRequired[bool]
    """The period end date or balance date associated with a given report."""
    report_period_end: NotRequired[str]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_period_index: NotRequired[int]
    """The phone number of the submitter of the report."""
    report_phone: NotRequired[str]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated: NotRequired[bool]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_restated_index: NotRequired[int]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """The state of incorporation for the entity submitting the report."""
    report_state_of_incorporation: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_submission_type: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    report_zip_url: NotRequired[str]


class ReportFactTypedDict(TypedDict, total=False):
    """TypedDict for report/fact endpoint fields"""

    aspect: NotRequired[str]
    """The balance type of a concept. This can be either debit, credit or not defined."""
    concept_balance_type: NotRequired[str]
    """The datatype of the concept such as monetary or string."""
    concept_datatype: NotRequired[str]
    """A unique identification id of the concept that can be searched on. This is a faster way to retrieve the details of a fact, however it is namespace specific and will only search for the use of a concept for a specific schema. """
    concept_id: NotRequired[int]
    """Identifies if the concept is from a base published taxonomy or from a company extension. Avalue of true indicates that it is a base taxonomy element. This attribute can be used for example to search for extension elements in a filing."""
    concept_is_base: NotRequired[bool]
    """Identifies if the concept is a monetary value. If yes the value is shown as true. A monetary value is distinguished from a numeric concept in that it has a currency associated with it."""
    concept_is_monetary: NotRequired[bool]
    """The concept name in the base schema of a taxonomy excluding the namespace, such as Assets or Liabilities. Use this to search across multiple taxonomies where the local name is known to be consistent over time."""
    concept_local_name: NotRequired[str]
    concept_namespace: NotRequired[str]
    """The period type of the concept. This can be either duration or instant."""
    concept_period_type: NotRequired[str]
    dimension_pair: NotRequired[Dict[str, Any]]
    """A boolean that indicates if the dimension concept is a base taxonomy element (true) or an extensions dimension concept (false)."""
    dimension_is_base: NotRequired[bool]
    """The dimension concept name in the taxonomy excluding the namespace, that is defined as dimension type."""
    dimension_local_name: NotRequired[str]
    """The namespace of the dimension concept used to identify a fact."""
    dimension_namespace: NotRequired[str]
    """Returns an array of dimensions associated with the given fact."""
    dimensions: NotRequired[Dict[str, Any]]
    """The number of dimensional qualifiers associated with a given fact."""
    dimensions_count: NotRequired[int]
    """The unique identifier of the dimensional aspects associated with a fact."""
    dimensions_id: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The target namespace of a discoverable taxonomy set. (DTS)."""
    dts_target_namespace: NotRequired[str]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The name of the entity reporting."""
    entity_name: NotRequired[str]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker: NotRequired[str]
    entity_ticker2: NotRequired[str]
    fact_accuracy_index: NotRequired[int]
    """The decimal value associated with a fact. This can be either a number representing decimal places or be infinite. There are two values returned for this field the first is a decimal and the second is a boolean. The first indicates the decimal places if applicable and the second identifies if the value is infinite(t) or not (f)."""
    fact_decimals: NotRequired[str]
    """This boolean field indicates if the fact has any dimensions associated with it."""
    fact_has_dimensions: NotRequired[bool]
    """The fact hash is derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time however different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. the fact hash is used to determine the ultimus index. By searching on the hash you can identify all identical facts that were reported."""
    fact_hash: NotRequired[str]
    """The unique identifier used to identify a fact."""
    fact_id: NotRequired[int]
    """The original value that was shown in the inline filing prior to be transformed to an XBRL value."""
    fact_inline_display_value: NotRequired[str]
    """Boolean that indicates if the fact was hidden in the inline document."""
    fact_inline_is_hidden: NotRequired[bool]
    """Boolean that indicates if the fact was negated in the inline document."""
    fact_inline_negated: NotRequired[bool]
    """Integer that indicates the scale used on the fact in the inline document."""
    fact_inline_scale: NotRequired[int]
    """This indicates if the fact is comprised of either an extension concept, extension axis or extension member."""
    fact_is_extended: NotRequired[bool]
    """The numerical value of the fact that was reported. """
    fact_numerical_value: NotRequired[float]
    """Used to define text in a text search. Cannot be output as a field."""
    fact_text_search: NotRequired[str]
    """A boolean that indicates if the fact is the latest value reported.  A value of true represents that it's the latest value reported.  A value of false represents that the value has been superseded with a more recent fact."""
    fact_ultimus: NotRequired[bool]
    """An integer that records the incarnation of the fact. The same fact is reported many times and the ultimus field captures the incarnation that was reported. A value of 1 indicates that this is the latest value of the fact. A value of 6 for example would indicate that the value has been reported 6 times subsequently to this fact being reported. If requesting values from a specific report the ultimus filed would not be used as a search parameter as you will not get all the fact values if there has been a subsequent report filed, as the ultimus value on these facts in a specific report will be updated as additional reports come in."""
    fact_ultimus_index: NotRequired[int]
    """The value of the fact as a text value. This included numerical as well as non numerical values reported."""
    fact_value: NotRequired[str]
    """Used to define text in a text search. Will return the actual text."""
    fact_value_link: NotRequired[str]
    """The xml-id included in the filing. Many facts may not have this identifier as it is dependent ofn the filer adding it. In inline filings it can be used to go directly to the fact value in the filing."""
    fact_xml_id: NotRequired[str]
    """The unique identifier to identify a footnote."""
    footnote_id: NotRequired[str]
    """ThThe ISO language code used to express the footnote. i.e. en-us."""
    footnote_lang: NotRequired[str]
    """The role used for the footnote."""
    footnote_role: NotRequired[str]
    """The text content of the footnote."""
    footnote_text: NotRequired[str]
    """A boolean value that indicates if the member is a base element in the reporting taxonomy or a company extension."""
    member_is_base: NotRequired[bool]
    """Local name of the member."""
    member_local_name: NotRequired[str]
    """Typed value or local-name of the member depending on the dimension type."""
    member_member_value: NotRequired[str]
    """Namespace of the member."""
    member_namespace: NotRequired[str]
    """Typed value of the member."""
    member_typed_value: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The calendar period aligns the periods with a calendar year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a calendar quarter of Q3."""
    period_calendar_period: NotRequired[str]
    """Period end date of the fact if applicable"""
    period_end: NotRequired[str]
    """The identifier of the fiscal period. Each period has an assigned hash which identifies the fiscal period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_fiscal_id: NotRequired[str]
    """The period identifier for the fact such as year(Y) quarters such as (Q1,Q2,Q3,Q4), cumulative quarters such as 3QCUM, and half years such as H1 and H2. The fiscal period aligns the periods with a fiscal year. A company with a year end of 30 September would have a fiscal 4th quarter which would be a fiscal quarter of Q4 and a calender quarter of Q3."""
    period_fiscal_period: NotRequired[str]
    """The fiscal year in which the fact is applicable."""
    period_fiscal_year: NotRequired[int]
    """The identifier of the calender period. Each period has an assigned hash which identifies the period. The hash can be used to search for periods that are identical. Periods with the same period and year in fact nay be different as the fiscal periods and years are approximations. """
    period_id: NotRequired[str]
    """Instant in time at which the fact was measured, inly applicable for facts with a period type of instant."""
    period_instant: NotRequired[str]
    """Period start date of the fact if applicable"""
    period_start: NotRequired[str]
    """The calendar year in which the facy is applicable."""
    period_year: NotRequired[int]
    """Date that the report was accepted at the regulator."""
    report_accepted_timestamp: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """Physical address of the reporting entity."""
    report_address: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_base_taxonomy: NotRequired[str]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_checks_run: NotRequired[bool]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    report_document_index: NotRequired[int]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The number of inline xbrl documents associated with the filing."""
    report_documentset_num: NotRequired[int]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entity_name: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_type: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    report_event_items: NotRequired[str]
    """The identifier used to identify a report."""
    report_filer_category: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    report_html_url: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """A boolean indicator for whether the report is the most current (true)."""
    report_is_most_current: NotRequired[bool]
    """The period end date or balance date associated with a given report."""
    report_period_end: NotRequired[str]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_period_index: NotRequired[int]
    """The phone number of the submitter of the report."""
    report_phone: NotRequired[str]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated: NotRequired[bool]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_restated_index: NotRequired[str]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """The state of incorporation for the entity submitting the report."""
    report_state_of_incorporation: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_submission_type: NotRequired[str]
    """The report type indicates if the report was filed in inline XBRL or XBRL format. The values can be either instance or inline."""
    report_type: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    report_zip_url: NotRequired[str]
    """The unit of measure associated with the fact."""
    unit: NotRequired[str]
    """The unit of measure used as the denominator for a fact"""
    unit_denominator: NotRequired[str]
    """the unit of measure used as the numerator for a fact"""
    unit_numerator: NotRequired[str]
    """The full qname of the unit of measure, includes the namespace of the unit in clark notation."""
    unit_qname: NotRequired[str]


class ReportNetworkTypedDict(TypedDict, total=False):
    """TypedDict for report/network endpoint fields"""

    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. A taxonomy can have multiple entry points and the resulting set of taxonomies of using an entry point is called a dts."""
    dts_entry_point: NotRequired[str]
    """The dts identifier for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a dts."""
    dts_id: NotRequired[int]
    """The CIK is the SEC identifier used to identify a reporting entity. This is the CIK associated with a given fact, DTS or report."""
    entity_cik: NotRequired[str]
    """The entity identifier for whatever source it is associated with.  All entity identifiers are in this field. This is the CIK associated with a given fact, DTS or report."""
    entity_code: NotRequired[str]
    """The internal identifier used to identify an entity. This will be replaced with the LEI when teh SEC supports the LEI standard."""
    entity_id: NotRequired[int]
    """The scheme of the identifier associated with a fact, report or DTS. A fact could have multiple entity identifiers and this indicates the identifier that was used."""
    entity_scheme: NotRequired[str]
    """The stock exchange ticker of the entity filing the report. Although a company may have multiple tickers this returns a single value."""
    entity_ticker: NotRequired[str]
    entity_ticker2: NotRequired[str]
    """URI that identifies the link types, such as parent-child. However, this is the full uri of http://www.xbrl.org/2003/arcrole/parent-child."""
    network_arcrole_uri: NotRequired[str]
    """Unique identifier used to identify a specific network. A different identifier is used for networks with the same role but different linkbase types."""
    network_id: NotRequired[int]
    """Name that identifies the link type. This corresponds to a linkbase i.e. presentationLink, calculationLink, definitionLink."""
    network_link_name: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks."""
    network_role_description: NotRequired[str]
    """The human readable description of the network role. In some filing regimes this is used to order the networks. This is used to do a text search on components of the text string."""
    network_role_description_like: NotRequired[str]
    """The URI of the network role. This would appear as a URI describing the reporting group i.e. http://www.bc.com/role/DisclosureBalanceSheetComponentsDetails."""
    network_role_uri: NotRequired[str]
    """Date that the report was accepted at the regulator."""
    report_accepted_timestamp: NotRequired[str]
    """The identifier used by the SEC to identify a report."""
    report_accession: NotRequired[str]
    """Physical address of the reporting entity."""
    report_address: NotRequired[str]
    """Base taxonomy used for the filing. e.g. US-GAAP 2020."""
    report_base_taxonomy: NotRequired[str]
    """Boolean flag that indicates if the Data Quality Committee checks (see assertion object details - dqcfiling) have run for this report."""
    report_checks_run: NotRequired[bool]
    """The creation software that was used to create a report/"""
    report_creation_software: NotRequired[str]
    report_document_index: NotRequired[int]
    """The document type of the report e.g. 10-K, 10-Q."""
    report_document_type: NotRequired[str]
    """The number of inline xbrl documents associated with the filing."""
    report_documentset_num: NotRequired[int]
    """The name of the entity submitting the report. To search enter the full entity name, or a portion of the entity name."""
    report_entity_name: NotRequired[str]
    """Identifies filer size associated with the report. Can be one of the following:
            - Large Accelerated Filer
            - Accelerated Filer
            - Non-accelerated Filer"""
    report_entry_type: NotRequired[str]
    """The url entry point of a discoverable taxonomy set. This is also referred to as the entry point for a taxonomy. This represents the DTS entry point for a specific report."""
    report_entry_url: NotRequired[str]
    report_event_items: NotRequired[str]
    """The identifier used to identify a report."""
    report_filer_category: NotRequired[str]
    """The date that the filing was published."""
    report_filing_date: NotRequired[str]
    """The document type of the FERC report e.g. 1, 2-A."""
    report_form_type: NotRequired[str]
    """A hash of all the filings information, facts, footnotes, etc.  Unique to each filing."""
    report_hash: NotRequired[str]
    report_html_url: NotRequired[str]
    """The identifier used to identify a report."""
    report_id: NotRequired[int]
    """A boolean indicator for whether the report is the most current (true)."""
    report_is_most_current: NotRequired[bool]
    """The period end date or balance date associated with a given report."""
    report_period_end: NotRequired[str]
    """The period the report was reported for."""
    report_period_focus: NotRequired[str]
    """Allows the retrieval of reports other than most current. A value of 1 gets the latest report. A value of 2 gets the second to last report etc."""
    report_period_index: NotRequired[int]
    """The phone number of the submitter of the report."""
    report_phone: NotRequired[str]
    """A boolean that indicates if the report has been subsequently restated.  A value of true represents that the report has been subsequently restated by another report.  A value of false means that this report has not been subsequently restated by another report."""
    report_restated: NotRequired[bool]
    """A numerical indicator that can be used to identify if a report has been restated. If the value is 1 it indicates that this is the latest report. If the value is 2 it means that an updated copy of the report has been filed."""
    report_restated_index: NotRequired[int]
    """The url at which the details of a filing can be accessed from the SEC Edgar system."""
    report_sec_url: NotRequired[str]
    """Integer that represents the Standard Industrial Classification (SIC) code used by the SEC in the United States."""
    report_sic_code: NotRequired[str]
    report_source_id: NotRequired[int]
    """Name of the source of the data such as SEC."""
    report_source_name: NotRequired[str]
    """The state of incorporation for the entity submitting the report."""
    report_state_of_incorporation: NotRequired[str]
    """A FERC filing identifier indicating if it's the first time it was filed or a subsequent one.  (O = Original; R = Restated)"""
    report_submission_type: NotRequired[str]
    """The year the report was reported for."""
    report_year_focus: NotRequired[str]
    """The url where the zip containing all the files of a filing can be accessed from the SEC Edgar system."""
    report_zip_url: NotRequired[str]
