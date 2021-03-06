import pytest

from structlog_to_seq import CelfProcessor


def dummy_value() -> str:
    return "value"


input_dictionaries = [
    {"@t": dummy_value()},
    {"@mt": dummy_value()},
    {"@l": dummy_value()},
    {"@x": dummy_value()},
    {"@r": dummy_value()},
    {
        "@t": dummy_value(),
        "@mt": dummy_value(),
        "event": "sample {@t} message {@mt} with reserved key {@t}",
    },
]


result_dictionaries = [
    {"_@t": dummy_value()},
    {"_@mt": dummy_value()},
    {"_@l": dummy_value()},
    {"_@x": dummy_value()},
    {"_@r": dummy_value()},
    {
        "_@t": dummy_value(),
        "_@mt": dummy_value(),
        "event": "sample {_@t} message {_@mt} with reserved key {_@t}",
    },
]


@pytest.mark.parametrize(
    "input_dict, result_dict", zip(input_dictionaries, result_dictionaries)
)
def test_reserved_key_replace_in_dict(
    input_dict: dict, result_dict: dict, celf_processor: CelfProcessor
):

    replace_result = celf_processor._replace_reserved_keys(input_dict)
    assert result_dict == replace_result
