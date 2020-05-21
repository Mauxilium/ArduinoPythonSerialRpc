from serial.rfc2217 import Serial

from arduinopythonserialrpc.engine.protocol_constants import CMD_PREAMBLE, RESULT_PREAMBLE, ERROR_PREAMBLE, MESSAGE_PREAMBLE, \
    VOID_ARG_PREAMBLE, INT_INT_ARG_PREAMBLE, STRING_ARG_PREAMBLE, FLOAT_ARG_PREAMBLE, INT_ARG_PREAMBLE


class ProtocolFromArduino:

    @staticmethod
    def get_token(serial: Serial):
        return serial.readline().decode().replace("\r\n", "")

    @staticmethod
    def handle_receiving_data(serial: Serial, controller):
        received_preamble = ProtocolFromArduino.get_token(serial)
        if received_preamble == CMD_PREAMBLE:
            ProtocolFromArduino.receive_command(serial, controller)
        elif received_preamble == RESULT_PREAMBLE:
            return ProtocolFromArduino.parsing_result(serial)
        elif received_preamble == ERROR_PREAMBLE:
            return "ERROR"
        elif received_preamble == MESSAGE_PREAMBLE:
            print("Arduino message: " + str(serial.readline()))

    @staticmethod
    def receive_command(serial: Serial, ctrl):
        cmd_name = ProtocolFromArduino.get_token(serial)
        arg_type = ProtocolFromArduino.get_token(serial)
        if arg_type == VOID_ARG_PREAMBLE:
            ctrl.execute_local_action(cmd_name)
        elif arg_type == INT_INT_ARG_PREAMBLE:
            arg1 = int(ProtocolFromArduino.get_token(serial))
            arg2 = int(ProtocolFromArduino.get_token(serial))
            ctrl.execute_local_action(cmd_name, arg1, arg2)
        elif arg_type == STRING_ARG_PREAMBLE:
            arg = ProtocolFromArduino.get_token(serial)
            ctrl.execute_local_action(cmd_name, arg)
        elif arg_type == FLOAT_ARG_PREAMBLE:
            arg = float(ProtocolFromArduino.get_token(serial))
            ctrl.execute_local_action(cmd_name, arg)
        else:
            raise Exception("Not supported received argument model: " + str(arg_type[0]))

    @staticmethod
    def parsing_result(serial: Serial):
        arg_type = ProtocolFromArduino.get_token(serial)
        if arg_type[0] == VOID_ARG_PREAMBLE:
            return None
        elif arg_type[0] == INT_ARG_PREAMBLE:
            return int(ProtocolFromArduino.get_token(serial))
        elif arg_type[0] == FLOAT_ARG_PREAMBLE:
            return float(ProtocolFromArduino.get_token(serial))
        elif arg_type[0] == STRING_ARG_PREAMBLE:
            return ProtocolFromArduino.get_token(serial)
        else:
            raise Exception("Not supported received data type: " + str(arg_type[0]))
