from application.init.k_template import KTemplateProtocol

class TerraformTemplate(KTemplateProtocol):
    def get_excludes(self) -> str:
        return (
            ".vs\n"
            ".terraform\n"
            ".git\n"
        )

    def get_includes(self) -> str:
        return (
            "*.tf\n"
            "*.tfvars\n"
            "*.json\n"
            "*.yaml\n"
        )

    def get_rules(self) -> str:
        return (
            "- Create a new module for each resource in modules/resources with reasonable default values.\n"
            "- Create component modules in modules/components for components requiring multiple resources.\n"
            "- Reference only resource modules from the component modules. Do not create resources directly in components.\n"
            "- Pay attention to established conventions.\n"
        )
