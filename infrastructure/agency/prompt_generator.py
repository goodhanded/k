from application.agency import PromptGeneratorProtocol
from application.templating import TemplateProtocol
from domain.registry import Registry

class PromptGenerator(PromptGeneratorProtocol):

    def __init__(self, prompt_registry: Registry):
        self.registry = prompt_registry

    def generate(self, template_name: str, **template_vars) -> str:
        template = self.registry.get(template_name)
        if not hasattr(template, 'format'):
            raise TypeError("Expected an object with a 'format' method")

        try:
            rendered_content = template.format(**template_vars)
        except KeyError as e:
            raise ValueError(f"Missing template var: {e.args[0]}") from e
        return rendered_content