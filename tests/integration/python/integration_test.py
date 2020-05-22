from threading import Event

from arduinopythonserialrpc.arduino_python_serial_rpc import ArduinoPythonSerialRpc

# String assigned to ArduinoRpc instance inside the sketch
EXPECTED_SKETCH = "Full Tutorial Sketch (www.mauxilium.it)"

# Values registered as placeholder during sketch setup (registerArduinoAction)
FLOAT_CALL_FROM_PC_TO_ARDUINO = "FloatCallPcToArduino"
STRING_CALL_FROM_PC_TO_ARDUINO = "StringCallPcToArduino"
INTEGER_CALL_FROM_PC_TO_ARDUINO = "IntCallPcToArduino"


class ArduinoRpc(ArduinoPythonSerialRpc):
    def __init__(self, port_name: str, baud_rate: int):
        super(ArduinoRpc, self).__init__(port_name, baud_rate, self)
        self.receiving_counter = 0
        self.string_call_counter = 0
        self.float_call_counter = 0
        self.int_call_counter = 0
        self.receiving_report = ""

    def get_report(self) -> str:
        if self.receiving_counter != 9:
            self.receiving_report += "FAILED:  Received "+str(self.receiving_counter)+" calls when expected is 9: "
            self.receiving_report += "stringCallJavaSide called "+str(self.string_call_counter)+" times instead 3"
            self.receiving_report += "floatCallJavaSide called " +str(self.float_call_counter)+" times instead 3"
            self.receiving_report += "intCallJavaSide called "+str(self.int_call_counter)+" times instead 3"
        return self.receiving_report

    def string_call_arduino_to_pc(self, value: str) -> str:
        '''
        Method called from Arduino
        :param value: a tests value sent from Arduino card
        :return: a constant ignored inside the sketch
        '''
        self.receiving_counter += 1
        self.string_call_counter += 1

        expected_str = str(13*self.string_call_counter)
        if expected_str != value:
            self.receiving_report += "stringCallArduinoToPc called from Arduino fails. Expected " + expected_str +\
                                     "; Found "+value+".\n"
        else:
            print("\tstringCallArduinoToPc called with value: "+value+"; expected: "+expected_str)
        return "ok"

    def float_call_arduino_to_pc(self, value: float) -> float:
        '''
        Method called from Arduino
        :param value: a tests value sent from Arduino card
        :return: a constant ignored inside the sketch
        '''
        self.receiving_counter += 1
        self.float_call_counter += 1

        expected_float = float(18.11*self.float_call_counter)
        if expected_float != value:
            self.receiving_report += "floatCallArduinoToPc called from Arduino fails. Expected " + str(expected_float) +\
                                     "; Found " + str(value) + ".\n"
        else:
            print("\tfloatCallArduinoToPc called with value: "+str(value)+"; expected: "+str(expected_float))
        return float(1.0)

    def int_call_arduino_to_pc(self, value1: int, value2: int) -> int:
        '''
        Method called from Arduino
        :param value1: a tests value sent from Arduino card
        :param value2: a tests value sent from Arduino card
        :return: a constant ignored inside the sketch
        '''
        self.receiving_counter += 1
        self.int_call_counter += 1

        if self.int_call_counter != value1:
            self.receiving_report += "intCallArduinoToPc called from Arduino fails. Expected first value " +\
                                     str(self.int_call_counter) + "; Found " + str(value1) + ".\n"

        expected_int = int(27 * value1)
        if expected_int != value2:
            self.receiving_report += "intCallArduinoToPc called from Arduino fails. Expected second value " +\
                                     str(expected_int) + "; Found " + str(value2) + ".\n"
        else:
            print("\tintCallArduinoToPc called with value1: "+str(value1)+"; expected: "+str(self.int_call_counter)+
                  "; value2: "+str(value2)+"; expected: "+str(expected_int))
        return 1

    def arduino_ends(self):
        '''
        Method called from Arduino when the Arduino to Pc calls are done
        When this method is called, the wait_receiving_test_completed method can be unlocked
        '''
        test_arduino_to_pc_completed.set()


def perform_python_to_arduino_test(arduino: ArduinoRpc):
    report = ""
    for cicle in range(1, 4):
        report += send_execution(cicle, arduino)

    if len(report) > 0:
        print("Pc to Arduino tests, FAILS:")
        print("\t"+report)
    else:
        print("Pc to Arduino tests, successfully done")
    print("")


def send_execution(cicle: int, arduino: ArduinoRpc) -> str:
    print("\tExec " + STRING_CALL_FROM_PC_TO_ARDUINO + " with index: " + str(cicle))
    string_expected = str(cicle) + str(cicle) + str(cicle)
    string_resp = arduino.execute_remote_function(STRING_CALL_FROM_PC_TO_ARDUINO, str(cicle))
    print("\t\tResult: "+string_resp+"; Expected: "+string_expected)

    print("\tExec " + INTEGER_CALL_FROM_PC_TO_ARDUINO + " with index: " + str(cicle))
    int_expected = (cicle + 18) * cicle
    int_resp = arduino.execute_remote_function(INTEGER_CALL_FROM_PC_TO_ARDUINO, cicle, cicle + 18)
    print("\t\tResult: " + str(int_resp)+"; Expected: "+str(int_expected))

    print("\tExec " + FLOAT_CALL_FROM_PC_TO_ARDUINO + " with index: " + str(cicle))
    float_expected = float(3.1 * cicle)
    float_resp = arduino.execute_remote_function(FLOAT_CALL_FROM_PC_TO_ARDUINO, float(1.0 * cicle))
    print("\t\tResult: " + str(float_resp)+"; Expected: "+str(float_expected))
    print("")

    report = ""
    if float_expected != float_resp:
        report += "Pc to Arduino Float method call fails. Expected " + str(float_expected) + "; Found " + str(float_resp) + ".\n"

    if string_expected != string_resp:
        report += "Pc to Arduino String method call fails. Expected " + string_expected + "; Found " + string_resp + ".\n"

    if int_expected != int_resp:
        report += "Pc to Arduino Integer method call fails. Expected " + str(int_expected) + "; Found " + str(int_resp) + ".\n"

    return report


def wait_receiving_test_completed(arduino):
    print("Waiting Arduino to Pc calls...")
    test_arduino_to_pc_completed.wait(10000)
    print("Arduino to Pc ends")


def evaluate_test_result(arduino):
    if len(arduino.get_report()) > 0:
        print("")
        print("Arduino to Pc tests, FAILS: ")
        print(arduino.get_report())
    else:
        print("Arduino to Pc tests, successfully done")


test_arduino_to_pc_completed = Event()


def do_it():
    arduino = ArduinoRpc("COM5", 9600)
    arduino.connect()

    card_name = arduino.get_card_name()
    if EXPECTED_SKETCH != card_name:
        print("Invalid card. Found \""+card_name+"\" instead of expected \""+EXPECTED_SKETCH+"\"")
        exit(-1)
    else:
        print("Connected to: "+card_name)

    arduino.execute_remote_function("Start")
    perform_python_to_arduino_test(arduino)
    arduino.execute_remote_function("Switch")
    wait_receiving_test_completed(arduino)
    arduino.execute_remote_function("Stop")
    evaluate_test_result(arduino)
    arduino.disconnect()


if __name__ == "__main__":
    do_it()
