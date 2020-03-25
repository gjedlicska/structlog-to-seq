import logging
import sys

import pytest
import structlog
import structlog_to_seq


@pytest.fixture(name="log_output")
def fixture_log_output():
    return structlog.testing.LogCapture()


def test_configure_logger(log_output):
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            structlog_to_seq.CelfProcessor(),
            log_output,
        ],
    )

    structlog.get_logger().info(
        "Configured structlog logger with {processor}", processor="CELF processor"
    )

    assert log_output.entries == [
        {
            "@l": "info",
            "@mt": "Configured structlog logger with {processor}",
            "processor": "CELF processor",
            "log_level": "info",
        }
    ]
