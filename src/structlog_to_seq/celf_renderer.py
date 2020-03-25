from typing import Any, Dict

from structlog_to_seq.abs_processor import AbsProcessor
from structlog_to_seq.celf_processor import CelfKeywords

import colorful as cf


class CelfRenderer(AbsProcessor):

    """
    Celf renderer provides renderings for tokens in the message template.
    The fully rendered message field is created for the event.
    """

    def __call__(self, _, __, event_dict) -> dict:

        rendered_event = self._render_tokens(event_dict)

        message_template = event_dict["event"]
        message = self._render_message_template(rendered_event)

        # event_dict[CelfKeywords.Message.value] = message
        rendered_event["event"] = message
        rendered_event["message_template"] = message_template

        return rendered_event

    @classmethod
    def _render_message_template(cls, event_dict: dict) -> str:
        """
        """
        # message = event_dict.get(CelfKeywords.MessageTemplate.value)
        message = event_dict.get("event")

        if not message:
            raise ValueError(
                f"The event dict doesn't contain a message template key "
                f"({CelfKeywords.MessageTemplate.value}), cannot format message. "
                f"{event_dict}"
            )

        for key, value in event_dict.items():
            if not isinstance(value, str):
                raise ValueError("All tokens have to be rendered to string.")

            message = message.replace(f"{{{key}}}", value)

        return message

    @classmethod
    def _render_tokens(cls, event_dict: dict) -> Dict[str, str]:
        rendered_event_dict = {
            key: cls._render_token(key, value) for key, value in event_dict.items()
        }
        return rendered_event_dict

    @classmethod
    def _render_token(cls, key: Any, token: Any) -> str:
        """
        Convert any token to a string representation.
        """

        if key == "exception":
            str_token = f"{cf.bold_red}{token}"
        elif key not in ["event", "level"]:
            str_token = f"{cf.underlined}{token}"
        else:
            str_token = f"{token}"
        return str_token


if __name__ == "__main__":
    # bwt = cf.black_on_white("Hello Colorful")
    # bwt_str = str(bwt)

    # print(bwt_str)

    import sys
    import logging
    import structlog
    from structlog_to_seq import CelfProcessor

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    structlog.configure(
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        processors=[
            structlog.processors.TimeStamper("iso", utc=False),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.add_log_level,
            # CelfProcessor(),
            CelfRenderer(),
            structlog.dev.ConsoleRenderer(),
        ],
    )

    logger = structlog.get_logger()

    logger.debug(
        "Configured structlog logger with {processor}", processor="CELF processor"
    )

    logger = logger.bind(some_foo=123.123)

    try:
        raise NotImplementedError("Is this even working?")
    except NotImplementedError as ni:
        logger.error("Whoops {what_wrong}", what_wrong="i don't know", exc_info=ni)

    logger.warning(
        "Now what {longer_dict}", longer_dict={
            "a": 123,
            "b": "asdfasdf",
            "c": {
                "im": "nested",
                2: "with_numbers"
            }
        }
    )

    raise EOFError("Im doing this, dont worry")
