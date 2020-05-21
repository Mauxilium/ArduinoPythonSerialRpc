from arduinopythonserialrpc.engine.action_selector import ActionSelector
from arduinopythonserialrpc.engine.usb_handler import UsbHandler
from arduinopythonserialrpc.engine.usb_receiver_agent import UsbReceiverAgent


class ArduinoPythonSerialRpc:
    def __init__(self, port_name: str, baud_rate: int, ctrl):
        self.usb_handler = UsbHandler(port_name, baud_rate, ctrl)
        self.usb_agent = None
        self.ctrl = ctrl

    def connect(self):
        serial = self.usb_handler.initialize()
        self.usb_agent = UsbReceiverAgent(serial, self.ctrl, self.usb_handler)
        self.usb_agent.start()

    def disconnect(self):
        self.usb_agent.disconnect()
        self.usb_handler.disconnect()

    def port_scanner(self) -> []:
        return self.usb_handler.port_scanner()

    def get_port_name(self) -> str:
        return self.usb_handler.get_port_name()

    def get_baud_rate(self) -> int:
        return self.usb_handler.get_baud_rate()

    def get_cart_name(self) -> str:
        return self.usb_handler.get_card_name()

    def execute_remote_action(self, action_name: str, arg1=None, arg2=None):
        return ActionSelector.select_and_execute(self.usb_handler, action_name, arg1, arg2)

    def execute_local_action(self, action_name: str, arg1=None, arg2=None):
        if arg2 is not None:
            return getattr(self.ctrl, action_name)(arg1, arg2)
        elif arg1 is not None:
            return getattr(self.ctrl, action_name)(arg1)
        else:
            return getattr(self.ctrl, action_name)()
