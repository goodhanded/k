from application.templating import TemplateProtocol

class PullRequestPrompt(TemplateProtocol):

    def format(self, **kwargs):
        return f"""
You are a highly skilled software engineering agent assisting with generating pull requests for a project. Respond using the structured response to indicate which files should be added, removed, or modified in order to accomplish the stated goal. Include the FULL CONTENT of every file to be created or modified. DO NOT RETURN PARTIAL FILE CONTENT. This content will be used to fully replace existing content, overwriting it entirely. Favor completeness over simplicity in your responses. The changes are expected to work out of the box without further modification. 

Occasionally source code may be unintentionally omitted. If asked to make changes to a file that is not present in the source code, return no additions, modifications, or removals and ask for the required file(s) to be added.

If the prompt neglects to mention something that is necessary for the changes to work, take the liberty to change what needs to be changed in order to accomplish the goal IF THE CHANGE IS FEASIBLE. Otherwise, ask for what you need. The changes will be inspected before committing to the project, so don't be overly risk-averse. Don't be lazy. Be thorough. Be creative. Be the best software engineering agent you can be. Here we go!  

=====================================================================================================================

GOAL: 

{kwargs.get('goal')}

=====================================================================================================================

PROJECT GUIDELINES:

{kwargs.get('rules')}

---------------------------------------------------------------------------------------------------------------------

EXISTING DIRECTORY TREE:

{kwargs.get('tree')}

---------------------------------------------------------------------------------------------------------------------

SOURCE CODE:

{kwargs.get('source_code')}

---------------------------------------------------------------------------------------------------------------------

{self._get_history(kwargs)}

"""
    
    def _get_history(self, kwargs):

        if kwargs.get('history'):
            return f"""

=====================================================================================================================
            
PREVIOUS REQUESTS:

Following is a list of previous requests related to this one and the summary of changes made in response to them. Pay close attention to avoid regressing on previous changes:

{self._parse_history(kwargs.get('history'))}

"""
        return ''
    
    def _parse_history(self, history):
        return '\n'.join([f"Goal:\n{item['goal']}:\n\nSummary:\n{item['summary']}" for item in history])