import yaml
from typing import Any, Optional
from application.util.yaml_loader_protocol import YamlLoaderProtocol

class YamlLoader(YamlLoaderProtocol):
    def load_yaml(self, file_path: str, subpath: Optional[Any] = None) -> Any:
        if not file_path.endswith('.yml') and not file_path.endswith('.yaml'):
            raise ValueError(f"File must be a YAML file. Got: {file_path}")
        
        if subpath and not isinstance(subpath, (str, list)):
            raise ValueError('Subpath must be a string or a list of strings')
        
        if isinstance(subpath, str):
            subpath = [subpath]

        with open(file_path, 'r') as file:
            all_content = yaml.safe_load(file)
            if subpath:
                content = all_content
                for key in subpath:
                    content = content.get(key)
                    if content is None:
                        return None
                return content
            else:
                return all_content
