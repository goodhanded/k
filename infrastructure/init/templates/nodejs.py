from application.init.k_template import KTemplateProtocol

class NodeJSTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            "node_modules\n"
            "dist\n"
            "build\n"
            ".env\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.js\n"
            "*.ts\n"
            "*.json\n"
            "package.json\n"
            "package-lock.json\n"
            "yarn.lock\n"
        )

    def get_rules(self) -> str:
        return (
            "- Follow JavaScript best practices.\n"
            "- Use ESLint and Prettier for code quality.\n"
            "- Keep dependencies up to date.\n"
        )
