import yaml

def load_yaml(file_path: str, subpath=None):
    """
    Load a YAML file and return the content as a dictionary. Optional parameter
    specifies a subpath to return. Subpath is a single string or a list of keys 
    to traverse the dictionary. If the subpath is not found, return None.
    """
    if not file_path.endswith('.yml') and not file_path.endswith('.yaml'):
        raise ValueError('File must be a YAML file')
    
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