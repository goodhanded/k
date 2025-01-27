import importlib

def resolve_module(target_str: str, container: object = None):
    """
    Given a string like "infrastructure.apps.test.TestApp.run",
    instantiate the module, class, and function.
    """
    # If target_str begins with @ symbol and container is not None, resolve the target from the container
    if target_str.startswith("@") and container is not None:
        return _import_service(target_str, container)

    # Otherwise, import the target directly
    return _import_target(target_str)

def _import_service(target_str: str, container: object):
    """
    Import the service and function specified in the target string.
    """
    # Extract the service name and function name
    service_name = target_str[1:].rsplit(".", 1)[0]
    func_name = target_str.split(".")[-1]

    # Get the service and function
    service = container.get(service_name)
    func = getattr(service, func_name)

    return func

def _import_target(target_str: str):
    """
    Import the module, class, and function specified in the target string.
    """
    module_path, class_name, func_name = target_str.rsplit(".", 2)
    
    # Import the module
    module = importlib.import_module(module_path)

    # Instantiate the class
    cls = getattr(module, class_name)
    instance = cls()

    # Get the method/function
    func = getattr(instance, func_name)

    return func