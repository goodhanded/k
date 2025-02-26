from application.templating.protocols.template import TemplateProtocol

class CodeAdvicePrompt(TemplateProtocol):

    def format(self, **kwargs):
        return f"""
You are a highly skilled software architect who excels at advising and growing expert engineers. Using the provided source code, please provide detailed advice in response to the prompt below.  

===================

PROMPT: {kwargs.get('prompt')}

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