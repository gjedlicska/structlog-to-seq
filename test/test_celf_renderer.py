import pytest

from structlog_to_seq import CelfRenderer


@pytest.fixture
def celf_renderer() -> CelfRenderer:
    return CelfRenderer()


def test_celf_renderer_no_message_template_error(celf_renderer):
    with pytest.raises(ValueError):
        celf_renderer(None, None, {"message": "without_template"})


def test_key_replace(celf_renderer):
    input = {"@mt": "Some message {template}.", "template": "rendered"}

    expected_result = {
        "@m": "Some message rendered.",
        "@mt": "Some message {template}.",
        "template": "rendered",
    }

    result = celf_renderer(None, None, input)

    assert result == expected_result


render_data = [
    (
        {"@mt": "Some message {template}.", "template": "rendered"},
        "Some message rendered.",
    ),
    (
        {"@mt": "{foo} message {template}.", "template": "rendered"},
        "{foo} message rendered.",
    ),
    (
        {"@mt": "{foo} message {template}.", "template": "rendered", "foo": "123"},
        "123 message rendered.",
    ),
]


@pytest.mark.parametrize("event_dict, expected_message", render_data)
def test_render_message_template(celf_renderer, event_dict, expected_message):

    assert expected_message == celf_renderer._render_message_template(event_dict)
