from typing import Any, Dict, List, Optional, Tuple, Type

class ServiceDefinition:
    def __init__(
        self,
        cls: Optional[Type[Any]] = None,
        pos_args: Optional[List[Any]] = None,
        kw_args: Optional[Dict[str, Any]] = None,
        tags: Optional[List[Dict[str, str]]] = None,
        factory: Optional[Tuple[str, str]] = None
    ):
        """
        :param cls: The class for direct instantiation (optional if using a factory).
        :param pos_args: Positional arguments to pass to either the constructor or factory method.
        :param kw_args: Keyword arguments to pass to either the constructor or factory method.
        :param tags: List of tags for this service.
        :param factory: A 2-tuple/list of [factory_service_ref, factory_method_name].
        """
        self.cls = cls
        self.pos_args = pos_args or []
        self.kw_args = kw_args or {}
        self.tags = tags or []
        self.factory = factory