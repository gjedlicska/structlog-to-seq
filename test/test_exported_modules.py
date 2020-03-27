from structlog_to_seq import __all__


try:
    from importlib.metadata import version  # type: ignore
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore


def test_all():
    assert __all__ == ["CelfProcessor", "MessageTemplateRenderer"]


def test_version():
    assert version("structlog_to_seq") == "0.2.1"
