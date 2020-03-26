from enum import Enum
from typing import Any, Callable, Dict

import colorful as cf

from structlog_to_seq.abs_processor import AbsProcessor
from structlog_to_seq.celf_processor import CelfKeywords


class StructlogKeywords(Enum):
    Timestamp = "timestamp"
    Message = "event"
    Level = "level"
    Exception = "exception"


class MessageTemplateRenderer(AbsProcessor):
    def __init__(self) -> None:
        cf.use_style("solarized")
        cf.use_true_colors()

        self._token_formatting_mapping: Dict[
            StructlogKeywords, Callable[[str], cf.Colorful]
        ] = {
            StructlogKeywords.Exception: cf.bold_red,
            StructlogKeywords.Timestamp: cf.bold_yellow
            # StructlogKeywords.Message: f"{token}",
            # don't mess with level formatting, it breaks structlog console renderer
            # StructlogKeywords.Level: cf.bold,
        }

    """
    Celf renderer provides renderings for tokens in the message template.
    The fully rendered message field is created for the event.
    """

    def __call__(self, _, __, event_dict) -> dict:
        rendered_event = self._render_tokens(event_dict)
        message = self._render_message_template(rendered_event)

        rendered_event[StructlogKeywords.Message.value] = message

        return rendered_event

    def _render_message_template(self, event_dict: dict) -> str:
        """
        """
        message = event_dict.get(StructlogKeywords.Message.value)

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

    def _render_tokens(self, event_dict: dict) -> Dict[str, str]:
        rendered_event_dict = {
            key: self._render_token(key, value) for key, value in event_dict.items()
        }
        return rendered_event_dict

    def _render_token(self, key: Any, token: Any) -> str:
        """
        Convert any token to a string representation.
        """

        try:
            enum_key = StructlogKeywords(key)
            formatter_func = self._token_formatting_mapping[enum_key]
            token = formatter_func(token)

        # cannot cast to StructlogKeyword, it must be a log event keyword
        except ValueError:
            token = cf.underlined(token)

        except KeyError:
            pass

        # return as a string formatted token
        finally:
            str_token = f"{token}"
            return str_token
