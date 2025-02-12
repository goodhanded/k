import importlib
from typing import Dict
from infrastructure.util import YamlLoader

from .service_definition import ServiceDefinition

# Make sure to import tagged_iterator so its constructor is registered!
import infrastructure.di.tagged_iterator  # noqa

def load_definitions_from_yaml(file_path: str) -> Dict[str, ServiceDefinition]:
    loader = YamlLoader()
    services_data = loader.load_yaml(file_path, "services") or {}
    definitions: Dict[str, ServiceDefinition] = {}

    for service_name, raw in services_data.items():
        # 'class' might be omitted if there's a factory-based definition
        cls = None
        if 'class' in raw:
            class_path = raw['class']
            mod_name, cls_name = class_path.rsplit('.', 1)
            module = importlib.import_module(mod_name)
            cls = getattr(module, cls_name)

        # 'factory' might look like [ '@some.factory.service', 'methodName' ]
        factory = raw.get('factory', None)

        # 'tags' is optional
        tags = raw.get('tags', [])

        # Determine if 'arguments' is a list (positional) or dict (keyword)
        arguments = raw.get('arguments', [])
        if isinstance(arguments, list):
            pos_args = arguments
            kw_args = {}
        elif isinstance(arguments, dict):
            pos_args = []
            kw_args = arguments
        else:
            raise TypeError(
                f"'arguments' for service '{service_name}' must be list or dict, got: {type(arguments)}"
            )

        definition = ServiceDefinition(
            cls=cls,
            pos_args=pos_args,
            kw_args=kw_args,
            tags=tags,
            factory=factory,
            inject_class=raw.get('inject_class', False)
        )
        definitions[service_name] = definition

    return definitions
