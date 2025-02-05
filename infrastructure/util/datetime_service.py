from datetime import datetime
from application.util.datetime_service_protocol import DatetimeServiceProtocol

class DatetimeService(DatetimeServiceProtocol):
    def ym(self) -> tuple[str, str]:
        return datetime.now().strftime("%Y"), datetime.now().strftime("%m")

    def ymd(self) -> tuple[str, str, str]:
        return datetime.now().strftime("%Y"), datetime.now().strftime("%m"), datetime.now().strftime("%d")

    def datetime_string(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def datetime_string_for_filename(self) -> str:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def date_string(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")
