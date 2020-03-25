import pytest

from structlog_to_seq import CelfProcessor

from .mock_timestamper import MockTimestamper


@pytest.fixture(scope="module")
def celf_processor() -> CelfProcessor:
    return CelfProcessor()


@pytest.fixture()
def mock_timestamper() -> MockTimestamper:
    return MockTimestamper()
