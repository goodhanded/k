from pydantic import BaseModel, Field
from application.agency import WorkflowProtocol


class ContinuousDevelopmentWorkflow(WorkflowProtocol):

    def run(self):
        
        # Load user stories
        # Load style guide
        # Load test procedures
        # Load directory tree
        # Load codebase

        pass