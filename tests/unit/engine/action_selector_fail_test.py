from unittest.mock import Mock

import pytest
from arduinopythonserialrpc.exception.local_exception import LocalException

from arduinopythonserialrpc.engine.usb_handler import UsbHandler

from arduinopythonserialrpc.engine.action_selector import ActionSelector

EMPTY_ACTION_NAME_EXCEPTION = "Error: invalid empty action name"


@pytest.fixture
def usb_handle_mock():
    return Mock(spec=UsbHandler)


def test_execute_void_without_name_fails(usb_handle_mock):
    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, None)

    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, "")


def test_execute_string_without_name_fails(usb_handle_mock):
    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, None, "fake_Arg")

    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, "", "fake_Arg")


def test_execute_float_without_name_fails(usb_handle_mock):
    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, None, 93.5)

    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, "", 45.2)


def test_execute_int_int_without_name_fails(usb_handle_mock):
    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, None, 38, 43)

    with pytest.raises(LocalException, match=EMPTY_ACTION_NAME_EXCEPTION):
        ActionSelector.select_and_execute(usb_handle_mock, "", 6, 82)


def test_execute_float_with_int_fails(usb_handle_mock):
    with pytest.raises(LocalException,
                       match="Error calling fake_method: invalid argument type. Found int instead of str or float"):
        ActionSelector.select_and_execute(usb_handle_mock, "fake_method", 13)


def test_execute_int_int_with_none_fails(usb_handle_mock):
    with pytest.raises(LocalException,
                       match="Error calling fake_method: invalid empty first argument with the second argument: 5"):
        ActionSelector.select_and_execute(usb_handle_mock, "fake_method", None, 5)


def test_execute_int_int_with_arg1_none_fails(usb_handle_mock):
    with pytest.raises(LocalException,
                       match="Error calling fake_method: invalid empty first argument with the second argument: 6.19"):
        ActionSelector.select_and_execute(usb_handle_mock, "fake_method", None, 6.19)


def test_execute_int_int_with_float_int_fails(usb_handle_mock):
    with pytest.raises(LocalException,
                       match="Error calling fake_method: invalid first argument type. Found float instead of int"):
        ActionSelector.select_and_execute(usb_handle_mock, "fake_method", 74.12, 2)


def test_execute_int_int_with_int_float_fails(usb_handle_mock):
    with pytest.raises(LocalException,
                       match="Error calling fake_method: invalid second argument type. Found float instead of int"):
        ActionSelector.select_and_execute(usb_handle_mock, "fake_method", 8, 33.2)
