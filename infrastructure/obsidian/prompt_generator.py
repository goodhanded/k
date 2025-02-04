from application.agency import PromptGeneratorProtocol
from application.notes import NoteVaultProtocol

class ObsidianPromptGenerator(PromptGeneratorProtocol):

    def __init__(self, vault: NoteVaultProtocol, prompt_template_path: str):
        self.vault = vault
        self.prompt_template_path = prompt_template_path

    def generate(self, template_name: str, **template_vars) -> str:
        """
        :param template_name: Name of the Obsidian note or template file to load.
        :param template_vars: Arbitrary key-value pairs for the template substitution.
        """
        # Load the template from your vault.
        full_path = f"{self.prompt_template_path}/{template_name}"
        prompt_template = self.vault.get(full_path)
        parent_template_content = prompt_template.content  # e.g. "Hello {name}, your item is {item}."

        # Interpolate using Python's str.format(**kwargs).
        #    If missing keys are possible, consider using a safer templating approach,
        #    like Jinja2 or a default dict. For now, we do basic .format(...) logic.
        try:
            rendered_content = parent_template_content.format(**template_vars)
        except KeyError as e:
            # If your template has {foo} but user didn't pass --foo=... 
            # you can either raise an error or fallback to something else.
            raise ValueError(f"Missing template var: {e.args[0]}") from e

        return rendered_content