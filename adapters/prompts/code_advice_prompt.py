from application.templating.protocols.template import TemplateProtocol


class CodeAdvicePrompt(TemplateProtocol):
    def format(self, **kwargs) -> str:
        memory_section = ""
        if kwargs.get("memory"):
            memory_section = f"\n---------\nMemory:\n{kwargs.get('memory')}\n---------\n"
        return f"""
You are a highly skilled software architect who excels at advising and growing expert engineers. Using the provided source code, please provide detailed advice in response to the prompt below.  If this is a followup to a previous prompt, you will find additional context in the memory section.

===================

PROMPT: {kwargs.get('prompt')}{memory_section}

===================

Following is a complete directory tree of the project:

---------

{kwargs.get('tree')}

---------

The existing source code follows:

---------

{kwargs.get('source_code')}

---------

"""
