from typing import Optional

from jasm.global_definitions import TimesType


class TimesTypeBuilder:
    @staticmethod
    def get_min_max_regex(times: TimesType) -> Optional[str]:

        if times.min_times == 1 and times.max_times == 1:
            return None
        if times.min_times == times.max_times:
            return f"{{{times.min_times}}}"
        return f"{{{times.min_times},{times.max_times}}}"
