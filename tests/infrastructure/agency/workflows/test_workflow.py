'''Test module for the Workflow functionality in infrastructure/agency/workflows/workflow.py.'''

from infrastructure.agency.workflows.workflow import Workflow


class DummyWorkflow(Workflow):
    def run(self) -> str:
        return "workflow executed"


def test_dummy_workflow_execution() -> None:
    """Test that a DummyWorkflow instance returns the expected output from run()."""
    dummy = DummyWorkflow()
    result = dummy.run()
    assert result == "workflow executed", "The DummyWorkflow run did not return the expected value."


def test_instance_of_workflow() -> None:
    """Test that DummyWorkflow is a subclass instance of Workflow."""
    dummy = DummyWorkflow()
    assert isinstance(dummy, Workflow), "DummyWorkflow should be an instance of Workflow."
