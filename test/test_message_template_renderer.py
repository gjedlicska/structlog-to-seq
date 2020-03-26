import pytest

from structlog_to_seq import MessageTemplateRenderer


@pytest.fixture
def message_template_renderer() -> MessageTemplateRenderer:
    return MessageTemplateRenderer()


def test_message_template_renderer_no_message_template_error(message_template_renderer):
    with pytest.raises(ValueError):
        message_template_renderer(None, None, {"message": "without_template"})


def test_not_string_token_raises_value_erro(message_template_renderer):
    with pytest.raises(ValueError):
        message_template_renderer._render_message_template({"event": 123})


def test_key_replace(message_template_renderer):
    input = {"event": "Some message {template}.", "template": "rendered"}

    expected_result = {
        "event": "Some message \x1b[4mrendered\x1b[24m\x1b[26m.",
        "template": "\x1b[4mrendered\x1b[24m\x1b[26m",
    }

    result = message_template_renderer(None, None, input)

    assert result == expected_result


render_data = [
    (
        {"event": "Some message {template}.", "template": "rendered"},
        "Some message rendered.",
    ),
    (
        {"event": "{foo} message {template}.", "template": "rendered"},
        "{foo} message rendered.",
    ),
    (
        {"event": "{foo} message {template}.", "template": "rendered", "foo": "123"},
        "123 message rendered.",
    ),
]


@pytest.mark.parametrize("event_dict, expected_message", render_data)
def test_render_message_template(
    message_template_renderer, event_dict, expected_message
):

    assert expected_message == message_template_renderer._render_message_template(
        event_dict
    )


def tests_render_tokens(message_template_renderer: MessageTemplateRenderer) -> None:
    class MockClass:
        def __str__(self):
            return "{class: mocked}"

    event_dict = {
        "event": "{foo} message {template}.",
        "template": MockClass(),
        "foo": 123,
        "exception": "Something wrong",
    }

    rendered_dict = message_template_renderer._render_tokens(event_dict)

    assert rendered_dict == {
        "event": "{foo} message {template}.",
        "template": "\x1b[4m{class: mocked}\x1b[24m\x1b[26m",
        "foo": "\x1b[4m123\x1b[24m\x1b[26m",
        "exception": (
            "\x1b[1m\x1b[38;2;220;50;47mSomething wrong\x1b[22m\x1b[39m\x1b[26m"
        ),
    }
