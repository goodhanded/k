
class Registry:
    def __init__(self, registry):
        self.registry = registry

    def register(self, item):
        self.registry[item.id] = item

    def get(self, item_id):
        return self.registry.get(item_id)

    def __iter__(self):
        return iter(self.registry.values())

    def __len__(self):
        return len(self.registry)