from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.notes import NoteVaultProtocol
    from application.filesystem import ClipboardProtocol

class GeneratePromptUseCase:
    def __init__(self, clipboard: 'ClipboardProtocol', note_vault: 'NoteVaultProtocol', prompt_template_path: str):
        self.clipboard = clipboard
        self.note_vault = note_vault
        self.prompt_template_path = prompt_template_path

    def execute(self, template_name: str, **template_vars):
        """
        :param template_name: Name of the Obsidian note or template file to load.
        :param template_vars: Arbitrary key-value pairs for the template substitution.
        """
        # 1. Load the template from your vault.
        full_path = f"{self.prompt_template_path}/{template_name}"
        prompt_template = self.note_vault.get(full_path)
        original_content = prompt_template.content  # e.g. "Hello {name}, your item is {item}."

        # 2. Interpolate using Python's str.format(**kwargs).
        #    If missing keys are possible, consider using a safer templating approach,
        #    like Jinja2 or a default dict. For now, we do basic .format(...) logic.
        try:
            rendered_content = original_content.format(**template_vars)
        except KeyError as e:
            # If your template has {foo} but user didn't pass --foo=... 
            # you can either raise an error or fallback to something else.
            raise ValueError(f"Missing template var: {e.args[0]}") from e

        # 3. Put the rendered text into the clipboard (or any final location).
        self.clipboard.set(rendered_content)

        print(f"\nTemplate '{template_name}' copied to clipboard with substitutions: {template_vars}\n")