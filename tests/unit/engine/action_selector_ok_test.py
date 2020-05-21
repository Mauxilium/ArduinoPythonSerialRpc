from unittest.mock import Mock

import pytest

from arduinopythonserialrpc.engine.action_selector import ActionSelector
from arduinopythonserialrpc.engine import UsbHandler


@pytest.fixture
def usb_handle_mock():
    return Mock(spec=UsbHandler)


def test_execute_void_ok(usb_handle_mock):
    usb_handle_mock.execute_remote_action.return_value = None
    result = ActionSelector.select_and_execute(usb_handle_mock, "fake_void_function")

    usb_handle_mock.execute_remote_action.assert_called_with("fake_void_function")
    assert result is None


def test_execute_string_ok(usb_handle_mock):
    usb_handle_mock.execute_remote_action_str.return_value = "result_value"

    result = ActionSelector.select_and_execute(usb_handle_mock, "fake_string_function", "test_value")

    usb_handle_mock.execute_remote_action_str.assert_called_with("fake_string_function", "test_value")
    assert result == "result_value"


def test_execute_float_ok(usb_handle_mock):
    usb_handle_mock.execute_remote_action_float.return_value = 18.11

    result = ActionSelector.select_and_execute(usb_handle_mock, "fake_float_function", 11.18)

    usb_handle_mock.execute_remote_action_float.assert_called_with("fake_float_function", 11.18)
    assert result == 18.11


def test_execute_int_int_ok(usb_handle_mock):
    usb_handle_mock.execute_remote_action_int_int.return_value = 20

    result = ActionSelector.select_and_execute(usb_handle_mock, "fake_int_int_function", 13, 67)

    usb_handle_mock.execute_remote_action_int_int.assert_called_with("fake_int_int_function", 13, 67)
    assert result == 20
