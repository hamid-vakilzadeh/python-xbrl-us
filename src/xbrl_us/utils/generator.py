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
    "boolean": "bool",
    "numeric": "float",
    "jsonb": "Dict[str, Any]",
}


def generate_field_map() -> str:
    """Generate a universal field mapping class for all endpoints"""
    return '''class UniversalFieldMap:
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

        # Group by prefix (e.g. 'fact', 'concept', etc)
        current_group = []
        result_parts = []

        for part in parts:
            if part in {"fact", "concept", "entity", "report", "dts", "network",
                       "dimension", "period", "unit", "label", "footnote", "member",
                       "relationship", "assertion", "cube"}:
                if current_group:
                    result_parts.append(".".join(current_group))
                current_group = [part]
            else:
                current_group.append(part)

        if current_group:
            result_parts.append(".".join(current_group))

        return "-".join(result_parts)

    @classmethod
    def to_snake(cls, original_name: str) -> str:
        """Convert an original API field name to snake_case"""
        return original_name.replace(".", "_").replace("-", "_")
'''


def generate_typed_dict(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a TypedDict class for an endpoint response data"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    fields = metadata.get("fields", {})

    # Generate field definitions and docstrings
    field_defs = []
    field_docs = []

    for field_name, field_info in fields.items():
        python_type = TYPE_MAPPINGS.get(field_info.get("type", "str"), "str")

        # Create snake_case version of the field name
        snake_name = field_name.replace(".", "_").replace("-", "_")

        # Add snake_case version to TypedDict
        field_defs.append(f"    {snake_name}: NotRequired[{python_type}]")

        # Add docstring with original field name
        if field_info.get("definition"):
            definition = field_info["definition"].replace("\n", " ").strip()
            definition = " ".join(definition.split())
            field_docs.append(f"    # {field_name}: {definition}")

    # Generate the TypedDict class
    content = f'''from typing import TypedDict, Dict, Any, Literal, Set
from typing_extensions import NotRequired

class {class_name}TypedDict(TypedDict, total=False):
    """TypedDict for {endpoint_name} endpoint response data

    Field names use snake_case format. Use UniversalFieldMap to convert between
    snake_case and original API format (with dots/hyphens).

    Example:
        >>> data: {class_name}TypedDict = {{
        ...     "fact_value": "1000000",  # API field: fact.value
        ...     "concept_balance_type": "debit",  # API field: concept.balance-type
        ... }}
        >>> api_field = UniversalFieldMap.to_original("fact_value")  # Returns "fact.value"
        >>> snake_field = UniversalFieldMap.to_snake("concept.balance-type")  # Returns "concept_balance_type"
    """
{chr(10).join(field_docs) if field_docs else ""}
{chr(10).join(field_defs)}
'''
    return content


def generate_parameters(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate parameter types for query fields"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    # Get all searchable fields and their prefixes
    searchable_fields = []
    field_prefixes = set()

    for field_name, field_info in metadata.get("fields", {}).items():
        if field_info.get("searchable") == "true":
            searchable_fields.append(field_name)
            prefix = field_name.split(".")[0] if "." in field_name else field_name
            field_prefixes.add(prefix)

    # Generate the field literals
    field_literals = ", ".join(f'"{field}"' for field in sorted(searchable_fields))
    prefix_literals = ", ".join(f'"{prefix}.*"' for prefix in sorted(field_prefixes))

    # Combine individual fields and wildcards
    all_literals = f"{field_literals}, {prefix_literals}" if prefix_literals else field_literals

    content = f'''from typing import Literal, Set, Union

{class_name}Parameter = Literal[{all_literals}]
"""{class_name} parameter fields that can be used in queries.
Includes both individual fields and wildcard patterns (e.g. fact.*)"""

{class_name}Parameters = Set[{class_name}Parameter]
"""Set of {class_name} parameters for use in queries"""
'''
    return content


def generate_endpoint_literal(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a Literal type containing valid endpoint keys and paths"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    endpoints = metadata.get("endpoints", {})

    # Create literals for both keys and paths
    endpoint_literals = []
    endpoint_mapping = []

    for key, path in endpoints.items():
        # Add both key and path to literals
        endpoint_literals.extend([f'"{key}"', f'"{path}"'])
        # Create mapping entry
        endpoint_mapping.append(f'    "{key}": "{path}",')

    # Generate the types and mapping
    content = f'''from typing import Literal, Dict

{class_name}Endpoint = Literal[{", ".join(sorted(endpoint_literals))}]
"""Valid endpoint identifiers for the {endpoint_name} endpoint.
Can be either the endpoint key or the full path."""

{class_name}EndpointMap: Dict[str, str] = {{
{chr(10).join(endpoint_mapping)}
}}
"""Mapping of endpoint keys to their paths"""
'''
    return content


def generate_init_content(metadata: Dict[str, Dict[str, Any]]) -> str:
    """Generate content for __init__.py to expose all generated types"""
    imports = []
    exports = []

    # First add the UniversalFieldMap
    imports.append("from .endpoint_types import UniversalFieldMap")
    exports.append("UniversalFieldMap")

    # Add all TypedDicts, Parameters and Endpoints
    for endpoint_name in metadata.keys():
        name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
        class_name = "".join(word.capitalize() for word in name.split("_"))

        # Add imports for each type
        imports.append(f"from .endpoint_types import {class_name}TypedDict")
        imports.append(f"from .endpoint_types import {class_name}Parameter")
        imports.append(f"from .endpoint_types import {class_name}Parameters")
        imports.append(f"from .endpoint_types import {class_name}Endpoint")
        imports.append(f"from .endpoint_types import {class_name}EndpointMap")

        # Add to exports
        exports.extend(
            [
                f"{class_name}TypedDict",
                f"{class_name}Parameter",
                f"{class_name}Parameters",
                f"{class_name}Endpoint",
                f"{class_name}EndpointMap",
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
                generate_typed_dict(endpoint_name, endpoint_meta),
                generate_parameters(endpoint_name, endpoint_meta),
                generate_endpoint_literal(endpoint_name, endpoint_meta),
            ]
        )

    # Generate the init file content
    init_content = generate_init_content(metadata)

    return {"endpoint_types.py": "\n\n".join(content), "__init__.py": init_content}


# Expose all generation methods
__all__ = ["generate_typed_dict", "generate_parameters", "generate_endpoint_literal", "generate_all_types"]
