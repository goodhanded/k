from application.templating import TemplateProtocol

class PullRequestPrompt(TemplateProtocol):

    def format(self, **kwargs):
        return f"""
I need help generating a pull request for my current project. Please respond using the structured response to indicate which files should be added, removed, or modified in order to accomplish the goal:

===================

{kwargs.get('goal')}

===================

Additional guidelines:

{kwargs.get('rules')}

---------

Following is a complete directory tree of the project:

---------

{kwargs.get('tree')}

---------

The existing content follows:

---------

{kwargs.get('content')}

---------

"""