from structlog_to_seq.abs_processor import AbsProcessor
from structlog_to_seq.celf_processor import CelfKeywords


class CelfRenderer(AbsProcessor):

    """
    Celf renderer provides renderings for tokens in the message template.
    The fully rendered message field is created for the event.
    """

    def __call__(self, _, __, event_dict) -> dict:

        message_template = event_dict.get(CelfKeywords.MessageTemplate.value)

        if not message_template:
            raise ValueError(
                f"The event dict doesn't contain a message template key "
                f"({CelfKeywords.MessageTemplate.value}), cannot format message. "
                f"{event_dict}"
            )

        message = self._render_message_template(event_dict)

        event_dict[CelfKeywords.Message.value] = message

        return event_dict

    @classmethod
    def _render_message_template(cls, event_dict: dict) -> str:
        """
        """
        message = event_dict[CelfKeywords.MessageTemplate.value]

        for key, value in event_dict.items():
            if not isinstance(value, str):
                raise ValueError("All tokens have to be rendered to string.")

            message = message.replace(f"{{{key}}}", value)

        return message
