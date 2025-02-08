"""Model and type hint generators for XBRL API"""
import logging
import re
from datetime import datetime
from datetime import timezone
from pathlib import Path
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


def generate_model_file(endpoint_name: str, metadata: Dict[str, Any], output_dir: Path) -> None:
    """Generate a Pydantic model file for an endpoint"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")

    model_name = "".join(word.capitalize() for word in name.split("_"))

    fields = metadata.get("fields", {})
    parameters = {k: v for k, v in metadata.get("fields", {}).items() if v.get("searchable") == "true"}

    field_lines = []
    for field_name, field_info in fields.items():
        python_type = TYPE_MAPPINGS.get(field_info.get("type", "str"), "str")
        snake_name = snake_case(field_name)

        # Add field with validation
        field_def = f"    {snake_name}: Optional[{python_type}] = Field("
        field_def += f"None, alias='{field_name}'"

        if field_info.get("definition"):
            field_def += f", definition='''{field_info['definition']}'''"

        if "format" in field_info:
            if field_info["format"] == "boolean":
                field_def += ", strict=True"
            elif field_info["format"] == "integer":
                field_def += ", strict=True"

        field_def += ")"
        field_lines.append(field_def)

    param_lines = []
    for param_name, param_info in parameters.items():
        python_type = TYPE_MAPPINGS.get(param_info.get("type", "str"), "str")
        snake_name = snake_case(param_name)

        param_def = f"    {snake_name}: Optional[{python_type}] = Field("
        param_def += f"None, alias='{param_name}'"

        if isinstance(param_info, dict) and param_info.get("description"):
            param_def += f", description='''{param_info['description']}'''"

        param_def += ")"
        param_lines.append(param_def)

    # Generate the model file content
    content = f'''"""
This module was automatically generated from XBRL.us API metadata on {datetime.now(tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
Do not edit manually.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class {model_name}Fields(BaseModel):
    """Fields model for {endpoint_name} endpoint"""

{chr(10).join(field_lines)}

class {model_name}Parameters(BaseModel):
    """Parameters model for {endpoint_name} endpoint"""

{chr(10).join(param_lines)}
'''

    # Write the file
    output_file = output_dir / f"{snake_case(name)}.py"
    output_file.write_text(content)
    logger.info(f"Generated model file: {output_file}")


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


class DynamicField:
    """Descriptor for dynamic field access"""

    def __init__(self, field_name: str, field_info: Dict[str, Any]):
        self.field_name = field_name
        self.field_info = field_info
        self.__doc__ = field_info.get("definition", "")

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.field_name


class DynamicEndpoint:
    """Dynamic attribute access for endpoint fields"""

    def __init__(self, metadata: Dict[str, Any]):
        self._metadata = metadata
        self._fields = metadata.get("fields", {})

        # Create descriptors for each field
        for field_name, field_info in self._fields.items():
            snake_name = snake_case(field_name)
            setattr(self.__class__, snake_name, DynamicField(field_name, field_info))

    def __getattr__(self, name):
        # Convert snake_case to original field name
        field_name = name.replace("_", "-")
        if field_name in self._fields:
            return field_name
        raise AttributeError(f"No field named {name}")

    @property
    def fields(self) -> Dict[str, Any]:
        """Get all available fields"""
        return self._fields


def create_dynamic_endpoint(endpoint_name: str, metadata: Dict[str, Any]) -> DynamicEndpoint:
    """Create a dynamic endpoint accessor instance"""
    return DynamicEndpoint(metadata)


def generate_json_schema(endpoint_name: str, metadata: Dict[str, Any], output_dir: Path) -> None:
    """Generate a JSON schema file for IDE autocompletion"""
    name = endpoint_name.replace("https://api.xbrl.us/api/v1/meta/", "").replace("/", "_")

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": f"{name} Fields",
        "description": f"Fields for {endpoint_name} endpoint",
        "type": "object",
        "properties": {},
    }

    for field_name, field_info in metadata.get("fields", {}).items():
        schema["properties"][field_name] = {
            "type": "string" if field_info.get("type") not in TYPE_MAPPINGS else TYPE_MAPPINGS[field_info["type"]],
            "description": field_info.get("definition", ""),
            "searchable": field_info.get("searchable") == "true",
        }

    import json

    output_file = output_dir / f"{snake_case(name)}_schema.json"
    with output_file.open("w") as f:
        json.dump(schema, f, indent=2)
    logger.info(f"Generated JSON schema: {output_file}")


# Expose all generation methods
__all__ = ["generate_model_file", "generate_typed_dict", "create_dynamic_endpoint", "generate_json_schema"]
