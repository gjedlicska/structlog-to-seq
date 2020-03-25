import pytest

from structlog_to_seq import CelfProcessor


@pytest.fixture(scope="module")
def celf_processor() -> CelfProcessor:
    return CelfProcessor()
