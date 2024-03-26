from typing import Optional

from jasm.global_definitions import TimeType


class TimeTypeBuilder:
    @staticmethod
    def get_min_max_regex(times: TimeType) -> Optional[str]:

        if times.min_times == 1 and times.max_times == 1:
            return None
        if times.min_times == times.max_times:
            return f"{{{times.min_times}}}"
        return f"{{{times.min_times},{times.max_times}}}"
