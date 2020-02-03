# pylint: disable=no-member
from unittest import mock

import click
import pytest

from cooar.utilities import echo


class TestEcho:
    def reset(self, click):
        click.echo.reset_mock()
        click.style.reset_mock()

    @mock.patch("click.style", mock.MagicMock())
    @mock.patch("click.echo", mock.MagicMock())
    def test_message(self):
        self.reset(click)
        echo.message("TEST", color="green", bold=False)
        click.style.assert_called_once_with("TEST", fg="green", bold=False)
        assert click.echo.called

    @mock.patch("click.style", mock.MagicMock())
    @mock.patch("click.echo", mock.MagicMock())
    @pytest.mark.parametrize("is_err", [True, False])
    def test__prefixed_message(self, is_err):
        self.reset(click)
        echo._prefixed_message("LULULUL", "message", "green", is_err)
        click.style.assert_has_calls(
            [
                mock.call("LULULUL: ", fg="green", bold=True),
                mock.call("message", fg="green", bold=False),
            ]
        )
        if is_err is True:
            click.echo.assert_called_once_with(mock.ANY, err="message")

        else:
            click.echo.assert_called_once_with(mock.ANY)

    @mock.patch("click.style", mock.MagicMock())
    @mock.patch("click.echo", mock.MagicMock())
    def test_key_value_message(self):
        self.reset(click)
        echo.key_value_message("key", "value", "green", "green")
        click.style.assert_has_calls(
            [mock.call("key: ", fg="green"), mock.call("value", fg="green"),]
        )
        click.echo.assert_called_once_with(mock.ANY)

    @mock.patch("click.style", mock.MagicMock())
    @pytest.mark.parametrize("value", [True, False])
    def test_bool_style(self, value):
        click.style.reset_mock()
        echo.bool_style(value)
        if value is True:
            click.style.assert_called_once_with("True", fg="green")
        else:
            click.style.assert_called_once_with("False", fg="red")

    @mock.patch("click.get_current_context", mock.MagicMock())
    @mock.patch("cooar.utilities.echo._prefixed_message", mock.MagicMock())
    @pytest.mark.parametrize("debug", [True, False])
    def test_debug_msg(self,debug):
        echo._prefixed_message.reset_mock()
        class FakeContext():
                obj = {}
                if debug is True:
                    obj['DEBUG'] = True
        click.get_current_context.return_value = FakeContext()

        echo.debug_msg('Test')
        if debug is True:
            echo._prefixed_message.assert_called_once_with("DEBUG", 'Test', "bright_black")
        else:
            assert not echo._prefixed_message.called

    @mock.patch("cooar.utilities.echo._prefixed_message", mock.MagicMock())
    def test_warning_msg(self):
        echo.warning_msg('Test')
        echo._prefixed_message.assert_called_once_with("WARNING", 'Test', "bright_yellow")

    @mock.patch("cooar.utilities.echo._prefixed_message", mock.MagicMock())
    def test_error_msg(self):
        echo.error_msg('Test')
        echo._prefixed_message.assert_called_once_with("ERROR", 'Test', "bright_red")
