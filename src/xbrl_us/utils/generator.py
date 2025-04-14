"""Model and type hint generators for XBRL API"""
import logging
from typing import Any
from typing import Dict

logger = logging.getLogger(__name__)

TYPE_MAPPINGS = {
    "text": "str",
    "varchar": "str",
    "bigint": "int",
    "int": "int",
    "boolean": 'Literal["true", "false"]',
    "numeric": "float",
    "jsonb": "Dict[str, Any]",
}


def generate_field_map() -> str:
    """Generate a universal field mapping class for all endpoints"""
    return '''from typing import TypedDict, Dict, Any, Literal, Set, List
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
        parts = snake_name.split('_')
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
'''


def generated_parameters(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a Parameters class for an endpoint response data"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    fields = metadata.get("fields", {})
    # only keep fields where searchable is true
    fields = {k: v for k, v in fields.items() if v.get("searchable", "false") == "true"}

    # Generate field definitions and docstrings
    field_defs = []
    field_docs = []

    for field_name, field_info in fields.items():
        if "type" in field_info.keys():
            python_type = TYPE_MAPPINGS.get(field_info.get("type", "str"), "str")
        else:
            continue

        # Create snake_case version of the field name
        snake_name = field_name.replace(".", "_").replace("-", "_")

        # Add snake_case version to TypedDict
        field_defs.append(f"    {snake_name}: NotRequired[{python_type}]")

        # Add docstring with original field name
        definition = field_info.get("definition", "No definition provided")
        field_docs.append(f'    """{definition}"""')

    # Generate the Parameters class
    content = f'''class {class_name}Parameters(TypedDict, total=False):
    """Parameters for {endpoint_name} endpoint response data

    Example:
        >>> data: {class_name}Parameters = {{
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }}

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """
'''
    # append each field definition and its docstring
    for field_def, field_doc in zip(field_defs, field_docs):
        content += f"{field_def}\n{field_doc}\n"
    return content


def generated_sort_fields(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a Sort class for an endpoint response data"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    fields = metadata.get("fields", {})

    # Generate field definitions and docstrings
    field_defs = []
    field_docs = []

    for field_name, field_info in fields.items():
        if "type" not in field_info.keys():
            continue

        # Create snake_case version of the field name
        snake_name = field_name.replace(".", "_").replace("-", "_")

        # Add snake_case version to TypedDict
        field_defs.append(f"    {snake_name}: NotRequired[Literal['asc', 'desc']]")

        # Add docstring with original field name
        definition = field_info.get("definition", "No definition provided")
        field_docs.append(f'    """{definition}"""')

    # Generate the Parameters class
    content = f'''class {class_name}Sorts(TypedDict, total=False):
    """Sort Fields for {endpoint_name} endpoint response data

    Example:
        >>> data: {class_name}Sorts = {{
        ...     "fact_value": "asc",  # API field: fact.value
        ...     "concept_balance_type": "desc",  # API field: concept.balance-type
        ... }}

    The API will automatically convert between snake_case and original API format.
    For example, the field "fact_value" will be converted to "fact.value" in the API request.

    """
'''
    # append each field definition and its docstring
    for field_def, field_doc in zip(field_defs, field_docs):
        content += f"{field_def}\n{field_doc}\n"
    return content


def generate_fields_literal(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a Literal type containing all fields with a type attribute"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    # Get all fields with a type attribute
    typed_fields = []
    for field_name, field_info in metadata.get("fields", {}).items():
        if "type" in field_info.keys():
            typed_fields.append(field_name)

    # Generate the field literals
    field_literals = ", ".join(f'"{field}"' for field in sorted(typed_fields))

    content = f'''{class_name}Fields = List[Literal[{field_literals}]]
"""All fields with type information for the {endpoint_name} endpoint."""
'''
    return content


def generate_endpoint_literal(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a Literal type containing valid endpoint keys and paths"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    endpoints = metadata.get("endpoints", {})

    # Create literals for both keys and paths
    endpoint_literals = []

    for _key, path in endpoints.items():
        # Add both key and path to literals
        endpoint_literals.extend([f'"{path}"'])

    # Generate the types and mapping
    content = f'''{class_name}Endpoint = Literal[{", ".join(sorted(endpoint_literals))}]
"""Valid endpoint identifiers for the {endpoint_name} endpoint.
Can be either the endpoint key or the full path."""
'''
    return content


def generate_init_content(metadata: Dict[str, Dict[str, Any]]) -> str:
    """Generate content for __init__.py to expose all generated types"""
    imports = []
    exports = []

    # First add the UniversalFieldMap
    imports.append("from .endpoint_types import UniversalFieldMap")
    exports.append("UniversalFieldMap")

    # Add all TypedDicts, Fields, Parameters and Endpoints
    for endpoint_name in metadata.keys():
        name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
        class_name = "".join(word.capitalize() for word in name.split("_"))

        # Add imports for each type
        imports.append(f"from .endpoint_types import {class_name}Parameters")
        imports.append(f"from .endpoint_types import {class_name}Fields")
        imports.append(f"from .endpoint_types import {class_name}Endpoint")
        imports.append(f"from .endpoint_types import {class_name}Sorts")

        # Add to exports
        exports.extend(
            [
                f"{class_name}Parameters",
                f"{class_name}Fields",
                f"{class_name}Endpoint",
                f"{class_name}Sorts",
            ]
        )

    # Generate the content
    content = [
        '"""This module was automatically generated. Do not edit manually."""',
        "",
        *imports,
        "",
        "__all__ = [",
        *[f"    {export!r}," for export in sorted(exports)],
        "]",
        "",
    ]

    return "\n".join(content)


def generate_all_types(metadata: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
    """Generate all type definitions and __init__ for the API

    Returns:
        Dict[str, str]: Dictionary with generated file contents:
            - 'endpoint_types.py': All type definitions
            - '__init__.py': Init file exposing all types
    """
    # First generate the universal field map
    content = [generate_field_map()]

    # Then generate TypedDicts and other types for each endpoint
    for endpoint_name, endpoint_meta in metadata.items():
        content.extend(
            [
                generated_parameters(endpoint_name, endpoint_meta),
                generate_fields_literal(endpoint_name, endpoint_meta),
                generate_endpoint_literal(endpoint_name, endpoint_meta),
                generated_sort_fields(endpoint_name, endpoint_meta),
            ]
        )

    # Generate the init file content
    init_content = generate_init_content(metadata)

    return {"endpoint_types.py": "\n\n".join(content), "__init__.py": init_content}


# Expose all generation methods
__all__ = ["generated_parameters", "generate_fields_literal", "generate_endpoint_literal", "generated_sort_fields", "generate_all_types"]
