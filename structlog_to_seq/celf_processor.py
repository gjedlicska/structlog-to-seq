from structlog_to_seq.abs_processor import AbsProcessor


class CelfProcessor(AbsProcessor):

    """
    Celf format specification
    ----------------------------


    The seq log server consumes events in the CLEF (Compact Log Event Format).
     This format contains newline separated JSON objects.

    The official documentation can be found here:
    https://docs.datalust.co/docs/posting-raw-events#section-reified-properties

    A format for one JSON object is:

    | Property | Name              | Required? |
    | :--------:| :--------------- | --------- |
    | @t        | Timestamp        | no, but highly recommended |
    | @m        | Message          | if not provided, server will render the template |
    | @mt       | Message Template | without message or template, server shows a blank |
    | @l        | Level            | if not provided, or recognized, level = INFO |
    | @x        | Exception        | |
    | @i        | Event id         | not recommended |
    | @r        | Renderings       | |


    Details:
    * **Timestamp**: An ISO 8601 timestamp. If not provided, the server will add it at
        the time of arrival, not at the time of message creation.
    * **Message**: A fully-rendered message describing the event.
    * **Message Template**: Alternative to Message; specifies a message template over
        the event's properties that provides for rendering into a textual
        description of the event.
    * **Level**: An implementation-specific level identifier (string or number)
    * **Exception**: A language-dependent error representation potentially
        including backtrace
    * **Event id**: An implementation specific event id (string or number).
        Ie.: messages with the same template belong to the same event id,
        so are searchable in the server gui / api.
        The Seq server does a good job at handling this, doing it inside client
        applications would be tedious.
    * **Renderings**: If @mt includes tokens with programming-language-specific
        formatting, an array of pre-rendered values for each such token.
        May be omitted; if present, the count of renderings must match
        the count of formatted tokens exactly.

    """

    __event_keyword = "event"

    __structlog_to_celf_mapper = {
        "timestamp": "@t",
        __event_keyword: "@mt",
        "level": "@l",
        "exception": "@x",
        "renderings": "@r",
    }

    def _replace_reserved_keys(self, input_dict: dict) -> dict:

        for reserved_key in self.__structlog_to_celf_mapper.values():
            value_with_reserved_key = input_dict.pop(reserved_key, None)
            if value_with_reserved_key:

                new_key = f"_{reserved_key}"

                input_dict.update({new_key: value_with_reserved_key})

                event: str = input_dict.get(self.__event_keyword, None)
                if event:
                    input_dict[self.__event_keyword] = event.replace(
                        reserved_key, new_key
                    )

        return input_dict

    def _translate_keys(self, input_dict: dict) -> dict:
        translated_dict = {
            self.__structlog_to_celf_mapper.get(k, k): v for k, v in input_dict.items()
        }
        return translated_dict

    def __call__(self, _, __, event_dict) -> dict:
        return self._translate_keys(event_dict)
