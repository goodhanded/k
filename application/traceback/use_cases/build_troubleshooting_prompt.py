from ..protocols.prompt_builder import PromptBuilderProtocol

class BuildTroubleshootingPromptUseCase:
    def __init__(self, builder: PromptBuilderProtocol):
        self.builder = builder

    def execute(self) -> str:
        self.builder.build()