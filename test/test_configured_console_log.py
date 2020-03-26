import logging
import sys

import structlog

from structlog_to_seq import MessageTemplateRenderer


def console_log():
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper("%H:%M:%S.%f", utc=False),
            MessageTemplateRenderer(),
            structlog.dev.ConsoleRenderer(colors=True),
        ],
    )

    logger = structlog.get_logger()

    logger.debug(
        "Configured structlog logger with {processor} with a longer message"
        " {processor} {processor}",
        processor="CELF processor",
    )

    logger = logger.bind(some_foo=123.123)

    try:
        raise NotImplementedError("Is this even working?")
    except NotImplementedError as ni:
        logger.error("Whoops {what_wrong}", what_wrong="i don't know", exc_info=ni)

    logger.warning(
        "Now what {longer_dict}",
        longer_dict={
            "a": 123,
            "b": "asdfasdf",
            "c": {"im": "nested", 2: "with_numbers"},
        },
    )

    raise EOFError("Im doing this, dont worry")
