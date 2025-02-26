from application.init.k_template import KTemplateProtocol

class PythonTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            "venv\n"
            "__pycache__\n"
            "*.pyc\n"
            ".env\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.py\n"
            "*.md\n"
            "requirements.txt\n"
            "setup.py\n"
        )

    def get_rules(self) -> str:
        return (
            "- Follow PEP8 guidelines.\n"
            "- Use virtual environments for dependency isolation.\n"
            "- Write unit tests for new features.\n"
        )
