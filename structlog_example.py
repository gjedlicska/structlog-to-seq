import logging
import sys

import structlog

from structlog_to_seq import CelfProcessor


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    structlog.configure(
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            # Prevent exception formatting if logging is not configured
            # Add file, line, function information of where log occurred
            # Add a timestamp to log message
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            CelfProcessor(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
    )

    log = structlog.get_logger()

    log.info(
        "Great news, you can use {log_solution} with SEQ server",
        log_solution="structlog",
    )
    log.debug(
        "This is debug message created using {log_solution} "
        "and processed by {processor}",
        log_solution="structlog",
        log_version=structlog.__version__,
        processor="structlog_2_seq",
    )

    key_im_looking_for = "foo"
    try:
        v = {"bar": 123}
        val = v[key_im_looking_for]

    except KeyError as ke:
        log.error(
            "Did not find the key I'm looking for",
            key_im_looking_for=key_im_looking_for,
            exc_info=ke,
        )

    log.info("Move along...")
