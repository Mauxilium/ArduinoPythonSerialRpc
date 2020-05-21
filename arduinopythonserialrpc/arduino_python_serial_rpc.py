from arduinopythonserialrpc.engine.action_selector import ActionSelector
from arduinopythonserialrpc.engine.usb_handler import UsbHandler
from arduinopythonserialrpc.engine.usb_receiver_agent import UsbReceiverAgent

MAC_OS_DEFAULT_PORT = "/dev/tty.usbserial-A9007UX1"
'''Default port to use when the Operative System is Mac OS.'''

RASPBERRY_PI_DEFAULT_PORT = "/dev/ttyACM0"
'''Default port to use when the Platform is Raspberry PI.'''

LINUX_DEFAULT_PORT = "/dev/ttyUSB0"
'''Default port to use when the Operative System is Linux'''

INDOWS_DEFAULT_PORT = "COM5"
'''Default port to use when the Operative System is Windows.'''

WINDOWS_USB_1 = "COM1"
'''Port COM1, when the Operative System is Windows.'''

WINDOWS_USB_2 = "COM2"
WINDOWS_USB_3 = "COM3"
WINDOWS_USB_4 = "COM4"
WINDOWS_USB_5 = "COM5"
WINDOWS_USB_6 = "COM6"

DATA_RATE_300 = 300
DATA_RATE_600 = 600
DATA_RATE_1200 = 1200
DATA_RATE_2400 = 2400
DATA_RATE_4800 = 4800
DATA_RATE_9600 = 9600
DATA_RATE_14400 = 14400
DATA_RATE_19200 = 19200
DATA_RATE_28800 = 28800
DATA_RATE_38400 = 38400
DATA_RATE_57600 = 57600
DATA_RATE_115200 = 115200


class ArduinoPythonSerialRpc:
    '''
    This class implements a bidirectional communication with Arduino card in form
    of RPC (Remote Procedure Call) and RMI (Remote Method Invocation) through the serial port.
    Due to resource limitations of Arduino card, only a few fixed signatures are available.

    Java to Arduino (RPC)
        A Java program that includes ArduinoJavaSerialRpc can call a function inside an Arduino sketch if:
            - The sketch includes the ArduinoSerialRpc library: "#include <ArduinoSerialRpc.h>"
            - The sketch function is registered using the "registerArduinoAction" method.
            - The registered function have one of the following signatures:
                - void <i>methodName</i>();
                - int <i>methodName</i>(int arg1, int arg2);
                - float <i>methodName</i>(float arg);
                - String <i>methodName</i>(String arg);

        For example, a legal call could be:
            libraryInstance.executeAction("writeAction", 1811, 1118);

    Arduino to Java (RMI)
        An Arduino sketch can call a Java method without any registration, if:
            - The sketch includes: "#include <ArduinoSerialRpc.h>".
            - The required method is part of a class which extends ArduinoJavaSerialRpc.
            - The method signature is one of the following:
                - void <i>methodName</i>();
                - Integer <i>methodName</i>(Integer arg1, Integer arg2);
                - Float <i>methodName</i>(Float arg);
                - String <i>methodName</i>(String arg);

    '''

    def __init__(self, port_name: str, baud_rate: int, ctrl):
        '''
        Creates a connector to Arduino card.
        The constructor requires two parameter:
        The port name, which syntax depends from the operating system in use.
        The baud rate, which depends from the sketch setup().
        Frequently used values are declared in the PORTs constants (like LINUX_DEFAULT_PORT) and DATA_RATE constants.

        NOTE:
        This constructor instantiates the resource only, to establish a physical connection with the card a
        "connect()" invocation is required.
        :param port_name: The name of connection port; i.e. "COM1"
        :param baud_rate: The value for Serial port speed
        :param ctrl: The instance where the methods accessible from Arduino sketch are declared
        '''
        print("Powered by ArduinoPythonSerialRpc from www.mauxilium.it")
        self.usb_handler = UsbHandler(port_name, baud_rate, ctrl)
        self.usb_agent = None
        self.ctrl = ctrl

    def connect(self):
        '''
        Creates a connection with the Arduino card.
        After this calls the USB port is locked and no other programs can use it.
        In order to release the USB port a "disconnect()" call is required.
        '''
        serial = self.usb_handler.initialize()
        self.usb_agent = UsbReceiverAgent(serial, self.ctrl, self.usb_handler)
        self.usb_agent.start()

    def disconnect(self):
        '''
        Release the serial port connected to the Arduino card.
        To establish a new connection a "connect()" call is required.
        '''
        self.usb_agent.disconnect()
        self.usb_handler.disconnect()

    def port_scanner(self) -> []:
        '''
        Discover the available serial ports in system.
        :return: A list of available serial ports (free and used too).
        '''
        return self.usb_handler.port_scanner()

    def get_port_name(self) -> str:
        '''
        Returns the used USB port name
        :return: one of the legal values like "/dev/ttyUSB0" or "COM4"
        '''
        return self.usb_handler.get_port_name()

    def get_baud_rate(self) -> int:
        '''
        Returns the used baud rate
        :return: one of the legal values like DATA_RATE_300 or DATA_RATE_9600
        '''
        return self.usb_handler.get_baud_rate()

    def get_card_name(self) -> str:
        '''
        Returns the card identification declared into the sketch
        It is the string used as argument of ArduinoSerialRpc constructor into the sketch.
        :return: the registered card identification name
        '''
        return self.usb_handler.get_card_name()

    def execute_remote_action(self, action_name: str, arg1=None, arg2=None):
        '''
        Executes a function (of Arduino sketch) with signature selected by the not none arguments combination
        :param action_name: he name of Arduino's function to call.
        :param arg1: the optional first argument
        :param arg2: the optional second argument (must be None if arg1 is None)
        :return: the Arduino response if arg1 is not none; None otherwise
        '''
        return ActionSelector.select_and_execute(self.usb_handler, action_name, arg1, arg2)

    def execute_local_action(self, action_name: str, arg1=None, arg2=None):
        '''
        Executes a function of local controller with signature selected by the not none arguments combination
        :param action_name: the controller function to call
        :param arg1: the optional first argument
        :param arg2: the optional second argument (must be None if arg1 is None)
        :return: the function result
        '''
        if arg2 is not None:
            return getattr(self.ctrl, action_name)(arg1, arg2)
        elif arg1 is not None:
            return getattr(self.ctrl, action_name)(arg1)
        else:
            return getattr(self.ctrl, action_name)()
