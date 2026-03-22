import asyncio
import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from prompt_toolkit.formatted_text import HTML

from abot.cli import commands


@pytest.fixture
def mock_prompt_session():
    """Mock the global prompt session."""
    mock_session = MagicMock()
    mock_session.prompt_async = AsyncMock()
    with patch("abot.cli.commands._PROMPT_SESSION", mock_session), \
         patch("abot.cli.commands.patch_stdout"):
        yield mock_session


@pytest.mark.asyncio
async def test_read_interactive_input_async_returns_input(mock_prompt_session):
    """Test that _read_interactive_input_async returns the user input from prompt_session."""
    mock_prompt_session.prompt_async.return_value = "hello world"

    result = await commands._read_interactive_input_async()

    assert result == "hello world"
    mock_prompt_session.prompt_async.assert_called_once()
    args, _ = mock_prompt_session.prompt_async.call_args
    assert isinstance(args[0], HTML)  # Verify HTML prompt is used


@pytest.mark.asyncio
async def test_read_interactive_input_async_handles_eof(mock_prompt_session):
    """Test that EOFError converts to KeyboardInterrupt."""
    mock_prompt_session.prompt_async.side_effect = EOFError()

    with pytest.raises(KeyboardInterrupt):
        await commands._read_interactive_input_async()


def test_init_prompt_session_creates_session():
    """Test that _init_prompt_session initializes the global session."""
    # Ensure global is None before test
    commands._PROMPT_SESSION = None

    with patch("abot.cli.commands.PromptSession") as MockSession, \
         patch("abot.cli.commands.FileHistory") as MockHistory, \
         patch("pathlib.Path.home") as mock_home:

        mock_home.return_value = MagicMock()

        commands._init_prompt_session()

        assert commands._PROMPT_SESSION is not None
        MockSession.assert_called_once()
        _, kwargs = MockSession.call_args
        assert kwargs["multiline"] is False
        assert kwargs["enable_open_in_editor"] is False


def test_render_cli_media_renders_image_attachment(tmp_path):
    tiny_png = (
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO5tN8sAAAAASUVORK5CYII="
    )
    image_path = tmp_path / "qr.png"
    image_path.write_bytes(base64.b64decode(tiny_png))

    with patch("abot.cli.commands._render_image_ascii", return_value=True) as mock_render, \
         patch.object(commands.console, "print") as mock_print:
        commands._render_cli_media([str(image_path)])

    mock_render.assert_called_once()
    assert mock_print.called


def test_render_image_ascii_respects_terminal_width(tmp_path):
    from PIL import Image

    image_path = tmp_path / "wide.png"
    img = Image.new("1", (120, 120), 1)
    px = img.load()
    for y in range(120):
        for x in range(120):
            if (x + y) % 3 == 0:
                px[x, y] = 0
    img.save(image_path)

    with patch.object(commands.console, "print") as mock_print:
        ok = commands._render_image_ascii(image_path, max_width=64, terminal_width=40)

    assert ok is True
    rendered_lines: list[str] = []
    for call in mock_print.call_args_list:
        if not call.args:
            continue
        value = call.args[0]
        if isinstance(value, str):
            rendered_lines.extend(value.splitlines())
        else:
            rendered_lines.append(getattr(value, "plain", str(value)))
    assert rendered_lines
    longest = max(len(line) for line in rendered_lines)
    assert longest <= 40
