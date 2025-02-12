
class Registry:
    def __init__(self, services):
        self.services = services

    def register(self, item):
        self.services[item.id] = item

    def get(self, item_id):
        return self.services.get(item_id)
    
    def exists(self, item_id):
        return item_id in self.services

    def __iter__(self):
        return iter(self.services.values())

    def __len__(self):
        return len(self.services)