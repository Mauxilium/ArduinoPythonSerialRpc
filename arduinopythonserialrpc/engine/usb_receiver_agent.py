from threading import Thread, Lock
from arduinopythonserialrpc.engine.protocol_constants import CMD_PREAMBLE, RESULT_PREAMBLE, ERROR_PREAMBLE, MESSAGE_PREAMBLE, \
    VOID_ARG_PREAMBLE, INT_ARG_PREAMBLE, FLOAT_ARG_PREAMBLE, STRING_ARG_PREAMBLE
from arduinopythonserialrpc.engine.protocol_from_arduino import ProtocolFromArduino
from arduinopythonserialrpc.exception.remote_exception import RemoteException


class UsbReceiverAgent(Thread):
    def __init__(self, input_stream, ctrl, usb_handler):
        super(UsbReceiverAgent, self).__init__(target=self.serial_listener, args=(1,))
        self.input = input_stream
        self.controller = ctrl
        self.usb_handler = usb_handler
        self.is_in_life = True
        self.calling_result = None

    def disconnect(self):
        self.is_in_life = False

    def serial_listener(self, fake):
        self.input.reset_input_buffer()
        while self.is_in_life:
            received = ProtocolFromArduino.get_token(self.input)
            if len(received) > 0:
                self.handle_receiving_data(received)
                self.usb_handler.set_incoming_result(self.calling_result)

    def handle_receiving_data(self, received: str):
        if received.startswith(CMD_PREAMBLE, 0, len(CMD_PREAMBLE)):
            ProtocolFromArduino.receive_command(self.input, self.controller)
        elif received.startswith(RESULT_PREAMBLE, 0, len(RESULT_PREAMBLE)):
            self.parsing_result()
        elif received.startswith(ERROR_PREAMBLE, 0, len(ERROR_PREAMBLE)):
            raise RemoteException(ProtocolFromArduino.get_token(self.input))
        elif received.startswith(MESSAGE_PREAMBLE, 0, len(MESSAGE_PREAMBLE)):
            print("Arduino message: " + ProtocolFromArduino.get_token(self.input))

    def parsing_result(self):
        arg_type = ProtocolFromArduino.get_token(self.input)
        preamble = arg_type[0]
        if preamble == VOID_ARG_PREAMBLE:
            self.calling_result = None
        elif preamble == INT_ARG_PREAMBLE:
            self.calling_result = int(ProtocolFromArduino.get_token(self.input))
        elif preamble == FLOAT_ARG_PREAMBLE:
            self.calling_result = float(ProtocolFromArduino.get_token(self.input))
        elif preamble == STRING_ARG_PREAMBLE:
            self.calling_result = ProtocolFromArduino.get_token(self.input)
        else:
            raise RemoteException("Not supported received data type: " + arg_type)
