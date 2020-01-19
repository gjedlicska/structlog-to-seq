import structlog
from structlog_to_seq import CelfProcessor
import logging
import sys

if __name__ == '__main__':
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG
    )

    structlog.configure(
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,

        processors=[
            # Prevent exception formatting if logging is not configured
            # Add file, line, function information of where log occurred
            # Add a timestamp to log message
            structlog.processors.TimeStamper(fmt='iso', utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            CelfProcessor(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ]
    )

    log = structlog.get_logger()

    # log.debug("this is debug")
    # log.info("this is info")
    # log.warn("this is warning")

    try:
        v = {}
        val = v["foo"]

    except KeyError as ke:
        log.fatal("error", exc_info=ke)
