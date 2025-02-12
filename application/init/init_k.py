import os
from typing import Any


class DefaultTemplateRegistry:
    def get(self, template: str):
        return None


class InitKUseCase:
    """
    Use case to initialize a .k directory with configuration templates.
    """

    def __init__(self, template_registry: Any = None):
        if template_registry is None:
            template_registry = DefaultTemplateRegistry()
        self.template_registry = template_registry

    def execute(self, template: str = None) -> None:
        """
        Initializes the .k directory in the current working directory.
        If a template alias is provided, use the corresponding template's content.
        Otherwise, use default content.
        """
        current_dir = os.getcwd()
        k_dir = os.path.join(current_dir, ".k")

        if os.path.exists(k_dir):
            print(f"The .k directory already exists at {k_dir}. Initialization skipped.")
            return

        os.makedirs(k_dir, exist_ok=True)

        if template:
            tmpl = self.template_registry.get(template)
            if tmpl:
                excludes_content = tmpl.get_excludes()
                includes_content = tmpl.get_includes()
                rules_content = tmpl.get_rules()
            else:
                print(f"Template '{template}' not found. Falling back to default templates.")
                excludes_content = (
                    ".git\n"
                    "venv\n"
                    "__pycache__\n"
                    "dist\n"
                    "build\n"
                    ".env\n"
                    "node_modules\n"
                    ".turbo\n"
                    "pnpm-lock.yaml\n"
                    "package-lock.json\n"
                    ".pytest_cache\n"
                    "effective_agents\n"
                )
                includes_content = (
                    "*.py\n"
                    "*.ts\n"
                    "*.js\n"
                    "*.json\n"
                    "*.yml\n"
                    "*.yaml\n"
                    "*.md\n"
                    "*.tsx\n"
                    "*.jsx\n"
                    "*.css\n"
                    "*.scss\n"
                    "*.svg\n"
                    "*.sequelizerc\n"
                    "*.cjs\n"
                    "*.txt\n"
                    ".env.example\n"
                )
                rules_content = (
                    "- Adhere to Clean Architecture principles, as written by Robert Martin.\n"
                    "- Use type hints.\n"
                    "- Keep imports sorted at the top of the file.\n"
                    "- Limit classes to one per file.\n"
                    "- Update the README when appropriate.\n"
                    "- Add or update unit tests.\n"
                    "- Remove unaccessed imports.\n"
                    "- Leave existing comments in place when rewriting code. Add additional comments and comment blocks to improve code clarity.\n"
                )
        else:
            excludes_content = (
                ".git\n"
                "venv\n"
                "__pycache__\n"
                "dist\n"
                "build\n"
                ".env\n"
                "node_modules\n"
                ".turbo\n"
                "pnpm-lock.yaml\n"
                "package-lock.json\n"
                ".pytest_cache\n"
                "effective_agents\n"
            )
            includes_content = (
                "*.py\n"
                "*.ts\n"
                "*.js\n"
                "*.json\n"
                "*.yml\n"
                "*.yaml\n"
                "*.md\n"
                "*.tsx\n"
                "*.jsx\n"
                "*.css\n"
                "*.scss\n"
                "*.svg\n"
                "*.sequelizerc\n"
                "*.cjs\n"
                "*.txt\n"
                ".env.example\n"
            )
            rules_content = (
                "- Adhere to Clean Architecture principles, as written by Robert Martin.\n"
                "- Use type hints.\n"
                "- Keep imports sorted at the top of the file.\n"
                "- Limit classes to one per file.\n"
                "- Update the README when appropriate.\n"
                "- Add or update unit tests.\n"
                "- Remove unaccessed imports.\n"
                "- Leave existing comments in place when rewriting code. Add additional comments and comment blocks to improve code clarity.\n"
            )

        with open(os.path.join(k_dir, "excludes.txt"), "w", encoding="utf-8") as f:
            f.write(excludes_content)
        with open(os.path.join(k_dir, "includes.txt"), "w", encoding="utf-8") as f:
            f.write(includes_content)
        with open(os.path.join(k_dir, "rules.txt"), "w", encoding="utf-8") as f:
            f.write(rules_content)

        print(f".k directory has been initialized at {k_dir}.")
