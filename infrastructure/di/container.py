import importlib
from typing import Any, Dict, Set

from infrastructure.config import Config

from .service_definition import ServiceDefinition
from .tagged_iterator import TaggedIterator


class Container:
    def __init__(self, definitions: Dict[str, ServiceDefinition]):
        self.definitions = definitions
        self.singletons: Dict[str, Any] = {}
        self.resolving: Set[str] = set()
        self.config = Config()

    def get(self, service_name: str) -> Any:
        # Check if it's already instantiated
        if service_name in self.singletons:
            return self.singletons[service_name]

        # Detect circular references
        if service_name in self.resolving:
            raise RuntimeError(f"Circular dependency detected: {service_name}")
        self.resolving.add(service_name)

        definition = self.definitions.get(service_name)
        if not definition:
            self.resolving.remove(service_name)
            raise KeyError(f"No definition for service: {service_name}")

        # Resolve positional arguments
        resolved_pos_args = [self._resolve_argument(arg) for arg in definition.pos_args]

        # Resolve keyword arguments
        resolved_kw_args = {
            key: self._resolve_argument(arg)
            for key, arg in definition.kw_args.items()
        }

        # Decide how to create the instance
        if definition.factory:
            # Factory-based instantiation
            instance = self._call_factory(definition.factory, resolved_pos_args, resolved_kw_args)
        else:
            # Direct class instantiation
            if not definition.cls:
                raise ValueError(
                    f"Service '{service_name}' has no 'cls' or 'factory' defined."
                )
            if definition.inject_class:
                instance = definition.cls
            else:
                instance = definition.cls(*resolved_pos_args, **resolved_kw_args)

        self.singletons[service_name] = instance
        self.resolving.remove(service_name)

        return instance

    def _call_factory(self, factory_info, pos_args, kw_args) -> Any:
        """
        factory_info is expected to be [ '@some_service', 'methodName' ]
        or [ 'some_service', 'methodName' ].
        """
        if not isinstance(factory_info, (list, tuple)) or len(factory_info) != 2:
            raise ValueError(f"Invalid factory format: {factory_info}")

        factory_ref, method_name = factory_info

        # If there's an '@', remove it and get that service
        if isinstance(factory_ref, str) and factory_ref.startswith('@'):
            factory_ref = factory_ref[1:]

        # Retrieve the factory service instance
        factory_service = self.get(factory_ref)

        # Call the specified method with the resolved arguments
        factory_method = getattr(factory_service, method_name)
        return factory_method(*pos_args, **kw_args)

    def _resolve_argument(self, arg: Any) -> Any:
        
        # New syntax: if arg is a string that starts with "~", load YAML from file.
        if isinstance(arg, str) and arg.startswith("~"):
            # Expected format: "~/path/to/file.yaml:sub.path.to.definition"
            arg_clean = arg[2:] if arg.startswith("~/") else arg[1:]
            if ":" in arg_clean:
                file_part, subpath_str = arg_clean.split(":", 1)
                import os
                project_root = os.getenv("K_PATH")
                if not project_root:
                    raise ValueError("K_PATH environment variable is not set.")
                file_path = os.path.join(project_root, file_part)
                subpath = subpath_str.split(".")
                from infrastructure.util.yaml_loader import YamlLoader
                loader = YamlLoader()
                return loader.load_yaml(file_path, subpath)
            else:
                raise ValueError("Invalid syntax for YAML loader: missing colon separator.")
        
        # Handle configuration variables
        if isinstance(arg, str) and arg.startswith('%') and arg.endswith('%'):
            env_var = arg[1:-1]
            return self.config.require(env_var)
        
        # Handle service references
        if isinstance(arg, str) and arg.startswith('@'):
            return self.get(arg[1:])

        # Handle tagged iterators
        if isinstance(arg, TaggedIterator):
            return self._build_tagged_collection(arg)

        # Otherwise, it's literal
        return arg

    def _build_tagged_collection(self, tagged_iter: TaggedIterator) -> Dict[str, Any]:
        result = {}
        for service_name, definition in self.definitions.items():
            for tag_obj in definition.tags:
                if tag_obj.get("name") == tagged_iter.tag:
                    key_for_dict = tag_obj.get(tagged_iter.index_by, service_name)
                    result[key_for_dict] = self.get(service_name)
        return result
