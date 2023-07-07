from typing import Optional


class DimensionDetails:
    def __init__(self):
        self._id = None
        self._is_base = None
        self._local_name = None
        self._count = None
        self._is_domain = None
        self._is_explicit = None

    # Method to convert between API keys (with dashes)
    # and Python attribute names (with underscores)
    @staticmethod
    def convert_key_format(key: str) -> str:
        return key.replace("-", "_") if "-" in key else key.replace("_", "-")

    # Using property decorator for is_base attribute (API acceptable key: is-base)
    @property
    def is_base(self) -> Optional[bool]:
        return getattr(self, self.convert_key_format("is-base"), None)

    # Using setter for is_base attribute (API acceptable key: is-base)
    @is_base.setter
    def is_base(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_base must be of type bool or None, not {type(value)}")
        setattr(self, self.convert_key_format("is-base"), value)

    # Similar property and setter for other attributes
    # ...

    # Method to return the attributes as a dictionary
    def to_dict(self):
        attribute_dict = {}
        for attr in dir(self):
            if attr.startswith("_") and not attr.startswith("__"):
                api_key = f"concept.{self.convert_key_format(attr[1:])}"
                attribute_dict[api_key] = getattr(self, attr)
        return attribute_dict
