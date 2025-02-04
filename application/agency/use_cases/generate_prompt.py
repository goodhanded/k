from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.notes import NoteVaultProtocol
    from application.filesystem import ClipboardProtocol
    from ..protocols.prompt_generator import PromptGeneratorProtocol

class GeneratePromptUseCase:
    def __init__(self, clipboard: 'ClipboardProtocol', prompt_generator: 'PromptGeneratorProtocol'):
        self.clipboard = clipboard
        self.generator = prompt_generator

    def execute(self, template_name: str, **template_vars):
        """
        :param template_name: Name of the Obsidian note or template file to load.
        :param template_vars: Arbitrary key-value pairs for the template substitution.
        """
        rendered_content = self.generator.generate(template_name, **template_vars)

        # Put the rendered text into the clipboard (or any final location).
        self.clipboard.set(rendered_content)

        print(f"\nTemplate '{template_name}' copied to clipboard with substitutions: {template_vars}\n")