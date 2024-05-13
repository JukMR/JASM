from jasm.global_definitions import MatchingSearchMode, ConsumerType
from jasm.match.abstracts.i_matched_observer import IMatchedObserver
from jasm.match.implementations.complete_consumer import CompleteConsumer
from jasm.match.implementations.instruction_observer_consumer import InstructionObserverConsumer


class ConsumerBuilder:
    """Builder for the consumer."""

    @staticmethod
    def build(
        regex_rule: str,
        iMatchedObserver: IMatchedObserver,
        consumer_type: ConsumerType,
        matching_mode: MatchingSearchMode,
        return_only_address: bool,
    ) -> InstructionObserverConsumer:
        """Decide which consumer to create"""

        match consumer_type:
            case ConsumerType.complete:
                return CompleteConsumer(
                    regex_rule=regex_rule,
                    matched_observer=iMatchedObserver,
                    matching_mode=matching_mode,
                    return_only_address=return_only_address,
                )
            # TODO: implement this consumer
            # case ConsumerType.stream:
            #     return StreamConsumer(regex_rule=regex_rule, matched_observer=iMatchedObserver)

            case _:
                raise ValueError("Invalid consumer type")
