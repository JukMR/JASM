from src.regex.idirective_processor import IDirectiveProcessor


class DirectiveProcessor:
    """Main Directive Processor for the Strategy Pattern"""

    def __init__(self, strategy: IDirectiveProcessor) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: IDirectiveProcessor) -> None:
        self._strategy = strategy

    def execute_strategy(self) -> str:
        return self._strategy.process()
