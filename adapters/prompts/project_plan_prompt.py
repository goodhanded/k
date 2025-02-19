from application.templating import TemplateProtocol


class ProjectPlanPrompt(TemplateProtocol):
    def format(self, **kwargs) -> str:
        return f"""
You are a highly skilled software engineering agent tasked with creating a detailed project plan based on the provided goal which will inform
another agent how to implement the changes. The plan should consist of a list of user stories. Each user story must represent a tiny unit of work which can be assigned to an agent and, when completed together, accomplish the overall goal. The user stories also include acceptance criteria, technical considerations, steps to implement, and a detailed description. DO NOT write user stories for functionality that has already been implemented. Use the context below to think through the steps that must be completed to implement each story, using the source code and directory tree as a starting point.

============================================

GOAL: {kwargs.get('goal')}

============================================

CONTEXT:

--------------------------------------------

Directory Tree:

{kwargs.get('tree')}

--------------------------------------------

Source Code (if applicable):
{kwargs.get('source_code')}

"""
