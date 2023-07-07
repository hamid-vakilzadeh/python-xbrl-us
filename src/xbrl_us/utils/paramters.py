from typing import List
from typing import Optional


class Parameters:
    """
    A class representing the parameters for searching XBRL data.

    Parameters:
        concept_id (Optional[Union[int, List[int]]]): A unique integer or list of integers representing concept IDs that
         can be searched. This is a faster way to retrieve the details of a fact, but it is namespace specific and will
         only search for the use of a concept for a specific schema.
        concept_is_base (Optional[bool]): A boolean value indicating if the concept is a base element in the reporting taxonomy or a company extension.
        concept_is_monetary (Optional[bool]): A boolean value indicating if the concept is a monetary element.
        concept_local_name (Optional[List[str]]): A list of strings representing the local names of the concepts in the base schema of a taxonomy, excluding the namespace. Use this to search across multiple taxonomies where the local name is known to be consistent over time.
        concept_namespace (Optional[str]): The namespace of the concept used to identify a fact.
        dimension_is_base (Optional[bool]): A boolean value indicating if the dimension (aspect) is a base element in the reporting taxonomy or a company extension.
        dimension_local_name (Optional[List[str]]): A list of strings representing the local names of the dimensions used with the fact.
        dimension_namespace (Optional[str]): The namespace of the dimension used with the fact.
        dimensions_count (Optional[List[int]]): A list of integers representing the number of dimensional qualifiers associated with a given fact. A comma-delimited list will return facts with 0, 1, 2, etc. dimensions.
        dimensions_id (Optional[str]): The ID of the dimension.
        dts_entry_point (Optional[str]): The URL entry point of a discoverable taxonomy set (DTS). A taxonomy can have multiple entry points, and the resulting set of taxonomies using an entry point is called a DTS.
        dts_id (Optional[List[int]]): A list of integers representing the unique identifiers for a given group of taxonomies. XBRL facts and linkbases are typically associated with a given report that is associated with a DTS.
        dts_target_namespace (Optional[str]): The target namespace of a discoverable taxonomy set (DTS).
        entity_cik (Optional[List[str]]): A list of strings representing the SEC identifiers used to identify reporting entities. This is the CIK associated with a given fact, DTS, or report.
        entity_id (Optional[List[int]]): A list of integers representing the internal identifiers used to identify entities. This will be replaced with the LEI when the SEC supports the LEI standard.
        fact_has_dimensions (Optional[bool]): A boolean field indicating if the fact has any dimensions associated with it.
        fact_hash (Optional[str]): The fact hash derived from the aspect properties of the fact. Each fact will have a different hash in a given report. Over time, different facts may have the same hash if they are identical. The hash does not take into account the value reported for the fact. The fact hash is used to determine the ultimus index. By searching on the hash, you can identify all identical facts that were reported.
        fact_id (Optional[List[int]]): A list of integers representing the internal identifiers used to identify facts.
        fact_is_extended (Optional[bool]): A boolean value indicating if the fact is comprised of either an extension concept, extension axis, or extension member.
        fact_text_search (Optional[str]): A string used to search for specific text within the fact value data. The XBRL API uses the Sphinx search engine for text search.
        fact_ultimus (Optional[bool]): A boolean indicating if the fact is the latest value reported. A value of True represents the latest value reported, while a value of False indicates that the value has been superseded by a more recent fact.
        fact_ultimus_index (Optional[List[int]]): A list of integers representing the incarnation of the fact. The same fact may be reported many times, and the ultimus index represents the reverse order of incarnation for the fact's reporting. A value of 1 indicates that this is the latest value of the fact, while a higher value indicates that the value has been reported multiple times subsequent to the fact's most recent reporting.
        fact_value (Optional[str]): The value of the fact as a text value. This includes numerical as well as non-numerical values reported.
        fact_value_link (Optional[str]): A URL to the rendered fact value data. For data encoded as HTML, the URL will display the formatted data excerpted from the full report.
        member_is_base (Optional[bool]): A boolean value indicating if the member is a base element in the reporting taxonomy or a company extension.
        member_local_name (Optional[List[str]]): A list of strings representing the local names of the members.
        member_typed_value (Optional[List[str]]): A list of strings representing the typed member values.
        member_member_value (Optional[List[str]]): A list of strings representing the typed member or explicit member values.
        member_namespace (Optional[str]): The namespace of the member.
        period_calendar_period (Optional[List[str]]): A list of strings representing the period identifiers for the fact. Examples include year (Y), quarters (Q1, Q2, Q3, Q4), cumulative quarters (3QCUM), and half years (H1, H2).
        period_fiscal_id (Optional[str]): The identifier of the fiscal period. Each period has an assigned hash that identifies the fiscal period. The hash can be used to search for identical periods.
        period_fiscal_period (Optional[List[str]]): A list of strings representing the fiscal periods.
        period_fiscal_year (Optional[List[int]]): A list of integers representing the fiscal years.
        period_id (Optional[str]): The ID of the period.
        period_year (Optional[List[int]]): A list of integers representing the years.
        report_accession (Optional[str]): The accession number of the report.
        report_creation_software (Optional[str]): The software used to create the report.
        report_document_type (Optional[List[str]]): A list of strings representing the document types of the report.
        report_document_index (Optional[List[int]]): A list of integers representing the document indexes of the report.
        report_entry_url (Optional[str]): The URL entry point of the report.
        report_id (Optional[List[int]]): A list of integers representing the internal identifiers used to identify the report.
        report_restated (Optional[bool]): A boolean indicating if the report has been restated.
        report_restated_index (Optional[List[int]]): A list of integers representing the indexes of restated reports.
        report_sec_url (Optional[str]): The URL of the report on the SEC website.
        report_sic_code (Optional[List[str]]): A list of strings representing the Standard Industrial Classification (SIC) codes of the report.
        report_source_id (Optional[int]): The source identifier of the report.
        report_source_name (Optional[str]): The source name of the report.
        unit (Optional[List[str]]): A list of strings representing the units.

    """

    def __init__(
        self,
        concept_id: Optional[int] = None,
        concept_is_base: Optional[bool] = None,
        concept_is_monetary: Optional[bool] = None,
        concept_local_name: Optional[List[str]] = None,
        concept_namespace: Optional[str] = None,
        dimension_is_base: Optional[bool] = None,
        dimension_local_name: Optional[List[str]] = None,
        dimension_namespace: Optional[str] = None,
        dimensions_count: Optional[List[int]] = None,
        dimensions_id: Optional[str] = None,
        dts_entry_point: Optional[str] = None,
        dts_id: Optional[List[int]] = None,
        dts_target_namespace: Optional[str] = None,
        entity_cik: Optional[List[str]] = None,
        entity_id: Optional[List[int]] = None,
        fact_has_dimensions: Optional[bool] = None,
        fact_hash: Optional[str] = None,
        fact_id: Optional[List[int]] = None,
        fact_is_extended: Optional[bool] = None,
        fact_text_search: Optional[str] = None,
        fact_ultimus: Optional[bool] = None,
        fact_ultimus_index: Optional[List[int]] = None,
        fact_value: Optional[str] = None,
        fact_value_link: Optional[str] = None,
        member_is_base: Optional[bool] = None,
        member_local_name: Optional[List[str]] = None,
        member_typed_value: Optional[List[str]] = None,
        member_member_value: Optional[List[str]] = None,
        member_namespace: Optional[str] = None,
        period_calendar_period: Optional[List[str]] = None,
        period_fiscal_id: Optional[str] = None,
        period_fiscal_period: Optional[List[str]] = None,
        period_fiscal_year: Optional[List[int]] = None,
        period_id: Optional[str] = None,
        period_year: Optional[List[int]] = None,
        report_accession: Optional[str] = None,
        report_creation_software: Optional[str] = None,
        report_document_type: Optional[List[str]] = None,
        report_document_index: Optional[List[int]] = None,
        report_entry_url: Optional[str] = None,
        report_id: Optional[List[int]] = None,
        report_restated: Optional[bool] = None,
        report_restated_index: Optional[List[int]] = None,
        report_sec_url: Optional[str] = None,
        report_sic_code: Optional[List[str]] = None,
        report_source_id: Optional[int] = None,
        report_source_name: Optional[str] = None,
        unit: Optional[List[str]] = None,
    ):
        self._concept_id = concept_id
        self._concept_is_base = concept_is_base
        self._concept_is_monetary = concept_is_monetary
        self._concept_local_name = concept_local_name
        self._concept_namespace = concept_namespace
        self._dimension_is_base = dimension_is_base
        self._dimension_local_name = dimension_local_name
        self._dimension_namespace = dimension_namespace
        self._dimensions_count = dimensions_count
        self._dimensions_id = dimensions_id
        self._dts_entry_point = dts_entry_point
        self._dts_id = dts_id
        self._dts_target_namespace = dts_target_namespace
        self._entity_cik = entity_cik
        self._entity_id = entity_id
        self._fact_has_dimensions = fact_has_dimensions
        self._fact_hash = fact_hash
        self._fact_id = fact_id
        self._fact_is_extended = fact_is_extended
        self._fact_text_search = fact_text_search
        self._fact_ultimus = fact_ultimus
        self._fact_ultimus_index = fact_ultimus_index
        self._fact_value = fact_value
        self._fact_value_link = fact_value_link
        self._member_is_base = member_is_base
        self._member_local_name = member_local_name
        self._member_typed_value = member_typed_value
        self._member_member_value = member_member_value
        self._member_namespace = member_namespace
        self._period_calendar_period = period_calendar_period
        self._period_fiscal_id = period_fiscal_id
        self._period_fiscal_period = period_fiscal_period
        self._period_fiscal_year = period_fiscal_year
        self._period_id = period_id
        self._period_year = period_year
        self._report_accession = report_accession
        self._report_creation_software = report_creation_software
        self._report_document_type = report_document_type
        self._report_document_index = report_document_index
        self._report_entry_url = report_entry_url
        self._report_id = report_id
        self._report_restated = report_restated
        self._report_restated_index = report_restated_index
        self._report_sec_url = report_sec_url
        self._report_sic_code = report_sic_code
        self._report_source_id = report_source_id
        self._report_source_name = report_source_name
        self._unit = unit

        # The attribute _attribute_dict was in the initial example, but I am not sure what it refers to.
        # It may need to be updated with the addition of the new attributes.
        self._attribute_dict = self._generate_attribute_dict()
        super().__init__()

    def _generate_attribute_dict(self):
        attribute_dict = {}
        attributes = [attr for attr in dir(self) if not attr.startswith("_")]
        attributes.remove("get_parameters_dict")
        for attribute in attributes:
            value = getattr(self, attribute)
            if value:
                attribute_dict[self._format_attribute_name(attribute)] = value
        return attribute_dict

    def __call__(self, *args, **kwargs):
        return self.get_parameters_dict()

    @staticmethod
    def _format_attribute_name(attribute_name):
        words = attribute_name.split("_", maxsplit=1)
        return ".".join([words[0], words[1].replace("_", "-", 1)])

    def get_parameters_dict(self):
        return self._attribute_dict

    @property
    def concept_id(self):
        return self._concept_id

    @concept_id.setter
    def concept_id(self, value):
        self._concept_id = value
        self._attribute_dict[self._format_attribute_name("concept_id")] = value

    @property
    def concept_is_base(self):
        return self._concept_is_base

    @concept_is_base.setter
    def concept_is_base(self, value):
        self._concept_is_base = value
        self._attribute_dict[self._format_attribute_name("concept_is_base")] = value

    @property
    def concept_is_monetary(self):
        return self._concept_is_monetary

    @concept_is_monetary.setter
    def concept_is_monetary(self, value):
        self._concept_is_monetary = value
        self._attribute_dict[self._format_attribute_name("concept_is_monetary")] = value

    @property
    def concept_local_name(self):
        return self._concept_local_name

    @concept_local_name.setter
    def concept_local_name(self, value):
        self._concept_local_name = value
        self._attribute_dict[self._format_attribute_name("concept_local_name")] = value

    @property
    def concept_namespace(self):
        return self._concept_namespace

    @concept_namespace.setter
    def concept_namespace(self, value):
        self._concept_namespace = value
        self._attribute_dict[self._format_attribute_name("concept_namespace")] = value

    @property
    def dimension_is_base(self):
        return self._dimension_is_base

    @dimension_is_base.setter
    def dimension_is_base(self, value):
        self._dimension_is_base = value
        self._attribute_dict[self._format_attribute_name("dimension_is_base")] = value

    @property
    def dimension_local_name(self):
        return self._dimension_local_name

    @dimension_local_name.setter
    def dimension_local_name(self, value):
        self._dimension_local_name = value
        self._attribute_dict[self._format_attribute_name("dimension_local_name")] = value

    @property
    def dimension_namespace(self):
        return self._dimension_namespace

    @dimension_namespace.setter
    def dimension_namespace(self, value):
        self._dimension_namespace = value
        self._attribute_dict[self._format_attribute_name("dimension_namespace")] = value

    @property
    def dimensions_count(self):
        return self._dimensions_count

    @dimensions_count.setter
    def dimensions_count(self, value):
        self._dimensions_count = value
        self._attribute_dict[self._format_attribute_name("dimensions_count")] = value

    @property
    def dimensions_id(self):
        return self._dimensions_id

    @dimensions_id.setter
    def dimensions_id(self, value):
        self._dimensions_id = value
        self._attribute_dict[self._format_attribute_name("dimensions_id")] = value

    @property
    def dts_entry_point(self):
        return self._dts_entry_point

    @dts_entry_point.setter
    def dts_entry_point(self, value):
        self._dts_entry_point = value
        self._attribute_dict[self._format_attribute_name("dts_entry_point")] = value

    @property
    def dts_id(self):
        return self._dts_id

    @dts_id.setter
    def dts_id(self, value):
        self._dts_id = value
        self._attribute_dict[self._format_attribute_name("dts_id")] = value

    @property
    def dts_target_namespace(self):
        return self._dts_target_namespace

    @dts_target_namespace.setter
    def dts_target_namespace(self, value):
        self._dts_target_namespace = value
        self._attribute_dict[self._format_attribute_name("dts_target_namespace")] = value

    @property
    def entity_cik(self):
        return self._entity_cik

    @entity_cik.setter
    def entity_cik(self, value):
        self._entity_cik = value
        self._attribute_dict[self._format_attribute_name("entity_cik")] = value

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value
        self._attribute_dict[self._format_attribute_name("entity_id")] = value

    @property
    def fact_has_dimensions(self):
        return self._fact_has_dimensions

    @fact_has_dimensions.setter
    def fact_has_dimensions(self, value):
        self._fact_has_dimensions = value
        self._attribute_dict[self._format_attribute_name("fact_has_dimensions")] = value

    @property
    def fact_hash(self):
        return self._fact_hash

    @fact_hash.setter
    def fact_hash(self, value):
        self._fact_hash = value
        self._attribute_dict[self._format_attribute_name("fact_hash")] = value

    @property
    def fact_id(self):
        return self._fact_id

    @fact_id.setter
    def fact_id(self, value):
        self._fact_id = value
        self._attribute_dict[self._format_attribute_name("fact_id")] = value

    @property
    def fact_is_extended(self):
        return self._fact_is_extended

    @fact_is_extended.setter
    def fact_is_extended(self, value):
        self._fact_is_extended = value
        self._attribute_dict[self._format_attribute_name("fact_is_extended")] = value

    @property
    def fact_text_search(self):
        return self._fact_text_search

    @fact_text_search.setter
    def fact_text_search(self, value):
        self._fact_text_search = value
        self._attribute_dict[self._format_attribute_name("fact_text_search")] = value

    @property
    def fact_ultimus(self):
        return self._fact_ultimus

    @fact_ultimus.setter
    def fact_ultimus(self, value):
        self._fact_ultimus = value
        self._attribute_dict[self._format_attribute_name("fact_ultimus")] = value

    @property
    def fact_ultimus_index(self):
        return self._fact_ultimus_index

    @fact_ultimus_index.setter
    def fact_ultimus_index(self, value):
        self._fact_ultimus_index = value
        self._attribute_dict[self._format_attribute_name("fact_ultimus_index")] = value

    @property
    def fact_value(self):
        return self._fact_value

    @fact_value.setter
    def fact_value(self, value):
        self._fact_value = value
        self._attribute_dict[self._format_attribute_name("fact_value")] = value

    @property
    def fact_value_link(self):
        return self._fact_value_link

    @fact_value_link.setter
    def fact_value_link(self, value):
        self._fact_value_link = value
        self._attribute_dict[self._format_attribute_name("fact_value_link")] = value

    @property
    def member_is_base(self):
        return self._member_is_base

    @member_is_base.setter
    def member_is_base(self, value):
        self._member_is_base = value
        self._attribute_dict[self._format_attribute_name("member_is_base")] = value

    @property
    def member_local_name(self):
        return self._member_local_name

    @member_local_name.setter
    def member_local_name(self, value):
        self._member_local_name = value
        self._attribute_dict[self._format_attribute_name("member_local_name")] = value

    @property
    def member_typed_value(self):
        return self._member_typed_value

    @member_typed_value.setter
    def member_typed_value(self, value):
        self._member_typed_value = value
        self._attribute_dict[self._format_attribute_name("member_typed_value")] = value

    @property
    def member_member_value(self):
        return self._member_member_value

    @member_member_value.setter
    def member_member_value(self, value):
        self._member_member_value = value
        self._attribute_dict[self._format_attribute_name("member_member_value")] = value

    @property
    def member_namespace(self):
        return self._member_namespace

    @member_namespace.setter
    def member_namespace(self, value):
        self._member_namespace = value
        self._attribute_dict[self._format_attribute_name("member_namespace")] = value

    @property
    def period_calendar_period(self):
        return self._period_calendar_period

    @period_calendar_period.setter
    def period_calendar_period(self, value):
        self._period_calendar_period = value
        self._attribute_dict[self._format_attribute_name("period_calendar_period")] = value

    @property
    def period_fiscal_id(self):
        return self._period_fiscal_id

    @period_fiscal_id.setter
    def period_fiscal_id(self, value):
        self._period_fiscal_id = value
        self._attribute_dict[self._format_attribute_name("period_fiscal_id")] = value

    @property
    def period_fiscal_period(self):
        return self._period_fiscal_period

    @period_fiscal_period.setter
    def period_fiscal_period(self, value):
        self._period_fiscal_period = value
        self._attribute_dict[self._format_attribute_name("period_fiscal_period")] = value

    @property
    def period_fiscal_year(self):
        return self._period_fiscal_year

    @period_fiscal_year.setter
    def period_fiscal_year(self, value):
        self._period_fiscal_year = value
        self._attribute_dict[self._format_attribute_name("period_fiscal_year")] = value

    @property
    def period_id(self):
        return self._period_id

    @period_id.setter
    def period_id(self, value):
        self._period_id = value
        self._attribute_dict[self._format_attribute_name("period_id")] = value

    @property
    def period_year(self):
        return self._period_year

    @period_year.setter
    def period_year(self, value):
        self._period_year = value
        self._attribute_dict[self._format_attribute_name("period_year")] = value

    @property
    def report_accession(self):
        return self._report_accession

    @report_accession.setter
    def report_accession(self, value):
        self._report_accession = value
        self._attribute_dict[self._format_attribute_name("report_accession")] = value

    @property
    def report_creation_software(self):
        return self._report_creation_software

    @report_creation_software.setter
    def report_creation_software(self, value):
        self._report_creation_software = value
        self._attribute_dict[self._format_attribute_name("report_creation_software")] = value

    @property
    def report_document_type(self):
        return self._report_document_type

    @report_document_type.setter
    def report_document_type(self, value):
        self._report_document_type = value
        self._attribute_dict[self._format_attribute_name("report_document_type")] = value

    @property
    def report_document_index(self):
        return self._report_document_index

    @report_document_index.setter
    def report_document_index(self, value):
        self._report_document_index = value
        self._attribute_dict[self._format_attribute_name("report_document_index")] = value

    @property
    def report_entry_url(self):
        return self._report_entry_url

    @report_entry_url.setter
    def report_entry_url(self, value):
        self._report_entry_url = value
        self._attribute_dict[self._format_attribute_name("report_entry_url")] = value

    @property
    def report_id(self):
        return self._report_id

    @report_id.setter
    def report_id(self, value):
        self._report_id = value
        self._attribute_dict[self._format_attribute_name("report_id")] = value

    @property
    def report_restated(self):
        return self._report_restated

    @report_restated.setter
    def report_restated(self, value):
        self._report_restated = value
        self._attribute_dict[self._format_attribute_name("report_restated")] = value

    @property
    def report_restated_index(self):
        return self._report_restated_index

    @report_restated_index.setter
    def report_restated_index(self, value):
        self._report_restated_index = value
        self._attribute_dict[self._format_attribute_name("report_restated_index")] = value

    @property
    def report_sec_url(self):
        return self._report_sec_url

    @report_sec_url.setter
    def report_sec_url(self, value):
        self._report_sec_url = value
        self._attribute_dict[self._format_attribute_name("report_sec_url")] = value

    @property
    def report_sic_code(self):
        return self._report_sic_code

    @report_sic_code.setter
    def report_sic_code(self, value):
        self._report_sic_code = value
        self._attribute_dict[self._format_attribute_name("report_sic_code")] = value

    @property
    def report_source_id(self):
        return self._report_source_id

    @report_source_id.setter
    def report_source_id(self, value):
        self._report_source_id = value
        self._attribute_dict[self._format_attribute_name("report_source_id")] = value

    @property
    def report_source_name(self):
        return self._report_source_name

    @report_source_name.setter
    def report_source_name(self, value):
        self._report_source_name = value
        self._attribute_dict[self._format_attribute_name("report_source_name")] = value

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value
        self._attribute_dict[self._format_attribute_name("unit")] = value
