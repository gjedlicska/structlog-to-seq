import structlog
import structlog_to_seq
import sys
import logging


def test_configure_logger(capsys):
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            structlog_to_seq.CelfProcessor(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
            structlog.PrintLogger(),
        ],
    )

    log = structlog.get_logger()

    log.debug(
        "Configured structlog logger with {processor}", processor="CELF processor"
    )

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)

    log.warning(
        "Configured structlog logger with {processor}", processor="CELF processor"
    )

    out, err = capsys.readouterr()
    sys.stdout.write(out)
    sys.stderr.write(err)


if __name__ == "__main__":
    test_configure_logger()
