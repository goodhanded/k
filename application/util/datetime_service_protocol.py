from typing import Protocol, Tuple

class DatetimeServiceProtocol(Protocol):
    def ym(self) -> Tuple[str, str]:
        ...

    def ymd(self) -> Tuple[str, str, str]:
        ...

    def datetime_string(self) -> str:
        ...

    def datetime_string_for_filename(self) -> str:
        ...

    def date_string(self) -> str:
        ...
