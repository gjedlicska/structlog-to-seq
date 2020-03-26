from typing import Any

import pytest

from structlog_to_seq.abs_processor import AbsProcessor


class DummyProcessor(AbsProcessor):
    def __call__(self, logger, name, event_dict) -> Any:
        return super().__call__(logger, name, event_dict)


def test_abs_processor():
    with pytest.raises(TypeError):
        AbsProcessor()


def test_call_not_implemented():
    dummy_processor = DummyProcessor()

    with pytest.raises(NotImplementedError):
        dummy_processor(None, None, None)
