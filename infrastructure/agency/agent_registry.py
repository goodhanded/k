from domain.registry import Registry

class AgentRegistryFactory:

    def getRegistry(self, services=None):
        """
        The method that returns an 'AgentRegistry' instance.
        In real usage, you might do more advanced logic here.
        """
        # Return your custom object
        # For example, a domain.agency.AgentRegistry
        return Registry(registry=services)