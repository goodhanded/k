from application.init import KTemplateProtocol


class NextJSTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            "node_modules\n"
            ".next\n"
            "out\n"
            ".env\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.js\n"
            "*.jsx\n"
            "*.ts\n"
            "*.tsx\n"
            "next.config.js\n"
            "package.json\n"
        )

    def get_rules(self) -> str:
        return (
            "- Follow Next.js conventions.\n"
            "- Optimize for performance and SEO.\n"
            "- Use built-in routing and API features.\n"
        )
