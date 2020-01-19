from abc import ABCMeta, abstractmethod
from typing import Any


class AbsProcessor(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, logger, name, event_dict) -> Any:
        pass


class CelfProcessor(AbsProcessor):

    """
    Celf format specification
    ----------------------------


    The seq log server consumes events in the CLEF (Complact Log Event Format).
     This format contains newline separated JSON objects.

    The official documentation can be found here:
    https://docs.datalust.co/docs/posting-raw-events#section-reified-properties

    A format for one JSON object is:

    | Propertry | Name             | Description | Required? |
    | :--------:| :--------------- | ----------- | --------- |
    | @t        | Timestamp        | An ISO 8601 timestamp | no, but highly recommended, if not provided, the server will add it |
    | @m        | Message          | A fully-rendered message describing the event | no, if not provided, the server will render the message |
    | @mt       | Message Template | Alternative to Message; specifies a message template over the event's properties that provides for rendering into a textual description of the event. | |
    | @l        | Level            | An implementation-specific level identifier (string or number) | if not provided, or recognized, message is treated like INFO |
    | @x        | Exception        | A language-dependent error representation potentially including backtrace | |
    | @i        | Event id         | An implementation specific event id (string or number) | The Seq server does a good job at handling this, doing it inside client applications would be tedious. |
    | @r        | Renderings       | If @mt includes tokens with programming-language-specific formatting, an array of pre-rendered values for each such token | May be omitted; if present, the count of renderings must match the count of formatted tokens exactly |


    """

    __event_keyword = "event"

    __structlog_to_celf_mapper = {
        "timestamp": "@t",
        __event_keyword: "@mt",
        "level": "@l",
        "exception": "@x",
        "renderings": "@r"
    }

    def _replace_reserved_keys(self, input_dict: dict) -> dict:

        for reserved_key in self.__structlog_to_celf_mapper.values():
            value_with_reserved_key = input_dict.pop(reserved_key, None)
            if value_with_reserved_key:

                new_key = f"_{reserved_key}"

                input_dict.update({
                    new_key: value_with_reserved_key
                })

                event: str = input_dict[self.__event_keyword]
                event.replace(reserved_key, new_key)

        return input_dict

    def _translate_keys(self, input_dict: dict) -> dict:
        translated_dict = {self.__structlog_to_celf_mapper.get(k, k): v for k, v in input_dict.items()}
        return translated_dict

    def __call__(self, _, __, event_dict) -> dict:
        return self._translate_keys(event_dict)
