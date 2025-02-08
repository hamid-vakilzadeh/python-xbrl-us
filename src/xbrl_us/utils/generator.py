"""Model and type hint generators for XBRL API"""
import logging
import re
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


def snake_case(text: str) -> str:
    """Convert kebab-case or dot notation to snake_case"""
    text = text.replace("-", "_").replace(".", "_")
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def generate_typed_dict(endpoint_name: str, metadata: Dict[str, Any]) -> str:
    """Generate a TypedDict class for an endpoint"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")
    class_name = "".join(word.capitalize() for word in name.split("_"))

    fields = metadata.get("fields", {})

    field_lines = []
    for field_name, field_info in fields.items():
        python_type = TYPE_MAPPINGS.get(field_info.get("type", "str"), "str")
        snake_name = snake_case(field_name)

        # Add field with docstring
        if field_info.get("definition"):
            field_lines.append(f'    """{field_info["definition"]}"""')
        field_lines.append(f"    {snake_name}: NotRequired[{python_type}]")

    # Generate the TypedDict class
    content = f'''class {class_name}TypedDict(TypedDict, total=False):
    """TypedDict for {endpoint_name} endpoint fields"""
{chr(10).join(field_lines)}
'''
    return content


# Expose all generation methods
__all__ = ["generate_typed_dict"]
