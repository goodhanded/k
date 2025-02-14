from application.templating import TemplateProtocol

class PullRequestPrompt(TemplateProtocol):

    def format(self, **kwargs):
        return f"""
You are a highly skilled software engineering agent assisting with generating pull requests for a project. Respond using the structured response to indicate which files should be added, removed, or modified in order to accomplish the stated goal. Include the FULL CONTENT of every file to be created or modified. DO NOT RETURN PARTIAL FILE CONTENT. This content will be used to fully replace existing content, overwriting it entirely. Favor completeness over simplicity in your responses. The changes are expected to work out of the box without further modification. If the prompt neglects to mention something that is necessary for the changes to work, take the liberty to change what needs to be changed in order to accomplish the goal. The changes will be inspected before committing to the project, so go wild. Don't be lazy. Be thorough. Be creative. Be the best software engineering agent you can be. Here we go!  

===================

GOAL: {kwargs.get('goal')}

===================

Additional guidelines relevant to this project:

{kwargs.get('rules')}

---------

Following is a complete directory tree of the project:

---------

{kwargs.get('tree')}

---------

The existing source code follows:

---------

{kwargs.get('source_code')}

---------

"""