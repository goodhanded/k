from dataclasses import dataclass, field, fields
from typing import (
    TypeVar, Type, Union, Optional, List, Dict, Any,
    get_origin, get_args
)

T = TypeVar("T", bound="DataTransferObject")

@dataclass
class DataTransferObject:
    """
    Base class for data transfer objects with a generic from_dict method.
    """

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create an instance of cls from a dictionary of data.
        We iterate over each dataclass field in cls:
          1) If the field is not in the data, we just skip it (the dataclass default applies).
          2) Otherwise, parse the value according to the field's annotated type.
        """
        if not isinstance(data, dict):
            raise TypeError(f"Expected a dict to parse {cls.__name__}, got {type(data)}")

        init_args = {}
        for f in fields(cls):
            if f.name not in data:
                # If it's missing in the dict, the field's default (if any) is used.
                continue

            raw_value = data[f.name]
            parsed_value = cls._parse_value(f.type, raw_value)
            init_args[f.name] = parsed_value

        return cls(**init_args)

    @classmethod
    def _parse_value(cls, annotation: Any, raw_value: Any) -> Any:
        """
        Dispatch method for parsing a raw_value according to the given annotation.
        """

        # 1. Check if annotation is a Union (including Optional)
        if cls._is_union(annotation):
            return cls._parse_union(annotation, raw_value)

        # 2. Check if annotation is a generic container
        origin = get_origin(annotation)
        if origin is list:
            return cls._parse_list(annotation, raw_value)
        if origin is dict:
            return cls._parse_dict(annotation, raw_value)

        # 3. If annotation is a DataTransferObject subclass, parse recursively
        if cls._is_dto_subclass(annotation):
            return cls._parse_dto_subclass(annotation, raw_value)

        # 4. Otherwise, treat it as a "primitive" or pass it through
        return raw_value

    # -------------------------------------------------------------------------
    # Helpers for each kind of type annotation
    # -------------------------------------------------------------------------

    @staticmethod
    def _is_union(annotation: Any) -> bool:
        """
        Return True if annotation is a Union (including Optional).
        """
        return get_origin(annotation) is Union

    @classmethod
    def _parse_union(cls, annotation: Any, raw_value: Any) -> Any:
        """
        Handle Union[...] (including Optional[...]).

        If it's a simple Optional[T], then raw_value is either None or T.
        If it's a larger union of multiple types, you'd need more logic to pick which type to use.
        """
        args = get_args(annotation)
        # If value is None and None is in the Union, just return None
        if raw_value is None and type(None) in args:
            return None

        # Simple case: Optional[T]
        non_none_args = [t for t in args if t is not type(None)]
        if len(non_none_args) == 1:
            # e.g. Optional[Foo]
            return cls._parse_value(non_none_args[0], raw_value)

        # More complex Unions (Union[Foo, Bar, None, ...]):
        # You'd need logic to decide which type is correct. For demonstration, 
        # we just try each type until one succeeds (or return raw_value if all fail).
        for possible_type in non_none_args:
            try:
                return cls._parse_value(possible_type, raw_value)
            except Exception:
                pass
        
        # Fallback if we cannot parse
        return raw_value

    @classmethod
    def _parse_list(cls, annotation: Any, raw_value: Any) -> List[Any]:
        """
        Handle list[...] types (e.g. List[SomeDTO]).
        """
        if not isinstance(raw_value, list):
            raise TypeError(f"Expected list for {annotation}, got {type(raw_value)}")

        (inner_type,) = get_args(annotation)  # list has a single generic argument
        return [cls._parse_value(inner_type, item) for item in raw_value]

    @classmethod
    def _parse_dict(cls, annotation: Any, raw_value: Any) -> Dict[Any, Any]:
        """
        Handle dict[...] types (e.g. Dict[str, SomeDTO]).
        """
        if not isinstance(raw_value, dict):
            raise TypeError(f"Expected dict for {annotation}, got {type(raw_value)}")

        key_type, val_type = get_args(annotation)
        parsed = {}
        for k, v in raw_value.items():
            parsed_key = cls._parse_value(key_type, k)
            parsed_val = cls._parse_value(val_type, v)
            parsed[parsed_key] = parsed_val
        return parsed

    @staticmethod
    def _is_dto_subclass(annotation: Any) -> bool:
        """
        Return True if annotation is a subclass of DataTransferObject.
        """
        return isinstance(annotation, type) and issubclass(annotation, DataTransferObject)

    @classmethod
    def _parse_dto_subclass(cls, annotation: Type[T], raw_value: Any) -> Any:
        """
        Handle nested DataTransferObject subclasses.
        """
        if not isinstance(raw_value, dict):
            raise TypeError(f"Expected dict to parse {annotation.__name__}, got {type(raw_value)}")

        return annotation.from_dict(raw_value)