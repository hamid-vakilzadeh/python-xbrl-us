from typing import Optional


class ConceptDetails:
    # Docstring here...

    def __init__(self):
        self._balance_type: Optional[int] = None
        self._datatype: Optional[str] = None
        self._id: Optional[int] = None
        self._is_abstract: Optional[bool] = None
        self._is_base: Optional[bool] = None
        self._is_monetary: Optional[bool] = None
        self._is_nillable: Optional[bool] = None
        self._is_numeric: Optional[bool] = None
        self._local_name: Optional[str] = None
        self._namespace: Optional[str] = None
        self._period_type: Optional[int] = None
        self._substitution: Optional[str] = None

    @staticmethod
    def convert_key_format(key: str) -> str:
        return key.replace("-", "_") if "-" in key else key.replace("_", "-")

    @property
    def balance_type(self) -> Optional[int]:
        return self._balance_type

    @balance_type.setter
    def balance_type(self, value: Optional[int]):
        if value is not None and not isinstance(value, int):
            raise TypeError(f"balance_type must be of type int or None, not {type(value)}")
        self._balance_type = value

    @property
    def datatype(self) -> Optional[str]:
        return self._datatype

    @datatype.setter
    def datatype(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"datatype must be of type str or None, not {type(value)}")
        self._datatype = value

    @property
    def id(self) -> Optional[int]:
        return self._id

    @id.setter
    def id(self, value: Optional[int]):
        if value is not None and not isinstance(value, int):
            raise TypeError(f"id must be of type int or None, not {type(value)}")
        self._id = value

    @property
    def is_abstract(self) -> Optional[bool]:
        return self._is_abstract

    @is_abstract.setter
    def is_abstract(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_abstract must be of type bool or None, not {type(value)}")
        self._is_abstract = value

    @property
    def is_base(self) -> Optional[bool]:
        return self._is_base

    @is_base.setter
    def is_base(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_base must be of type bool or None, not {type(value)}")
        self._is_base = value

    @property
    def is_monetary(self) -> Optional[bool]:
        return self._is_monetary

    @is_monetary.setter
    def is_monetary(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_monetary must be of type bool or None, not {type(value)}")
        self._is_monetary = value

    @property
    def is_nillable(self) -> Optional[bool]:
        return self._is_nillable

    @is_nillable.setter
    def is_nillable(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_nillable must be of type bool or None, not {type(value)}")
        self._is_nillable = value

    @property
    def is_numeric(self) -> Optional[bool]:
        return self._is_numeric

    @is_numeric.setter
    def is_numeric(self, value: Optional[bool]):
        if value is not None and not isinstance(value, bool):
            raise TypeError(f"is_numeric must be of type bool or None, not {type(value)}")
        self._is_numeric = value

    @property
    def local_name(self) -> Optional[str]:
        return self._local_name

    @local_name.setter
    def local_name(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"local_name must be of type str or None, not {type(value)}")
        self._local_name = value

    @property
    def namespace(self) -> Optional[str]:
        return self._namespace

    @namespace.setter
    def namespace(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"namespace must be of type str or None, not {type(value)}")
        self._namespace = value

    @property
    def period_type(self) -> Optional[int]:
        return self._period_type

    @period_type.setter
    def period_type(self, value: Optional[int]):
        if value is not None and not isinstance(value, int):
            raise TypeError(f"period_type must be of type int or None, not {type(value)}")
        self._period_type = value

    @property
    def substitution(self) -> Optional[str]:
        return self._substitution

    @substitution.setter
    def substitution(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"substitution must be of type str or None, not {type(value)}")
        self._substitution = value

    def to_dict(self):
        attribute_dict = {}
        for attr in dir(self):
            if attr.startswith("_") and not attr.startswith("__"):
                api_key = f"concept.{self.convert_key_format(attr[1:])}"
                attribute_dict[api_key] = getattr(self, attr)
        return attribute_dict
