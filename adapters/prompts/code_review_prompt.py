from application.templating import TemplateProtocol

class CodeReviewPrompt(TemplateProtocol):
    def format(self, **kwargs) -> str:
        return f"""
You are an assistant specialized in code reviews. Please carefully review the following codebase.

Current Directory Tree:
-------------------
{kwargs.get('tree')}

Extracted File Content:
-------------------
{kwargs.get('source_code')}

Provide a concise and constructive code review highlighting potential improvements, code smells, and best practices.
"""
