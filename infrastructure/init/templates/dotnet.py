from application.init.k_template import KTemplateProtocol

class DotNetTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            "bin\n"
            "obj\n"
            ".vs\n"
            "packages\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.cs\n"
            "*.csproj\n"
            "*.sln\n"
            "appsettings.json\n"
        )

    def get_rules(self) -> str:
        return (
            "- Follow C# coding conventions.\n"
            "- Maintain proper project structure.\n"
            "- Use dependency injection and SOLID principles.\n"
        )
