import datetime

from structlog_to_seq.abs_processor import AbsProcessor


class MockTimestamper(AbsProcessor):
    def __init__(self) -> None:
        self._timestamp = datetime.datetime.now().isoformat()

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    def __call__(self, _, __, event_dict) -> dict:
        timestamp = self.timestamp
        event_dict["timestamp"] = timestamp
        return event_dict
