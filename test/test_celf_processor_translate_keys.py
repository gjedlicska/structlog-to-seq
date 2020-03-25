import pytest

from structlog_to_seq import CelfProcessor


def dummy_value() -> str:
    return "value"


input_dictionaries = [
    {"timestamp": dummy_value()},
    {"event": dummy_value()},
    {"level": dummy_value()},
    {"renderings": dummy_value()},
]

result_dictionaries = [
    {"@t": dummy_value()},
    {"@mt": dummy_value()},
    {"@l": dummy_value()},
    {"@r": dummy_value()},
]


@pytest.mark.parametrize(
    "input_dict, result_dict", zip(input_dictionaries, result_dictionaries)
)
def test_translate_keys(
    input_dict: dict, result_dict: dict, celf_processor: CelfProcessor
):
    translate_result = celf_processor._translate_keys(input_dict)

    assert translate_result == result_dict


@pytest.mark.parametrize(
    "input_dict, result_dict", zip(input_dictionaries, result_dictionaries)
)
def test_call(input_dict: dict, result_dict: dict, celf_processor: CelfProcessor):
    translate_result = celf_processor(None, None, input_dict)
    assert translate_result == result_dict
