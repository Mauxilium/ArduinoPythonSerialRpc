# ArduinoPythonSerialRpc

ArduinoPythonSerialRpc is the Python side of a serial communication library with Arduino Card.

The Arduino part of this communication is implemented into ArduinoSerialRpc repository.

The communication model is implemented in form of:
* Remote Method Invocation. Where Arduino calls a method declared into a Python class.
* Remote Procedure Call. Where a Python process call a function defined into the Arduino sketch.

The communication is a point to point model, performed through the serial (USB) port.
 
## Architecture

Tbdf

## Features

* Bidirectional communication
* Low Arduino resources required
* Easy to learn interface
* Flexible naming convention

# Getting Started

## Arduino Side Installation
It is required to:
 * download the Arduino library from: https://github.com/Mauxilium/ArduinoSerialRpc
 * expand it into your "library" path of Arduino Ide,
  or follows the manual installation section of https://www.arduino.cc/en/guide/libraries
  
## Python Side Installation
pip install arduinopythonserialrpc

## Arduino Sketch basic example
```c++
#include <ArduinoSerialRpc.h>

ArduinoSerialRpc rpc("Arduino www.mauxilium.it");

void setup() {
  Serial.begin(9600);
  rpc.registerArduinoFunction("go", startTest);
  rpc.registerArduinoFunction("halt", stopTest);
}


// ##########################################################################
// BE AWARE!!!
// DO NOT FORGET TO ADD THE FOLLOWING serialEvent() FUNCTION INTO YOUR SKETCH
void serialEvent() {
  rpc.serialEventHandler();
}
// ##########################################################################


bool execFlag = false;
int counter = 0;

void startTest() {
  execFlag = true;
}

void stopTest() {
  counter = 0;
  execFlag = false;
}

void loop() {
  delay(200);
  if (execFlag) {
    rpc.executeRemoteMethod("ping_from_arduino", counter, counter++);
  }
}

```

## Python Class basic example
A simplified version of Python test program could be:
```code
from threading import Event
from arduinopythonserialrpc.arduino_python_serial_rpc import ArduinoPythonSerialRpc


class ArduinoRpc(ArduinoPythonSerialRpc):
    def __init__(self):
        super(ArduinoRpc, self).__init__("COM5", 9600, self)

    def ping_from_arduino(self, arg1: int, arg2: int) -> int:
        print("Ping: "+str(arg2))
        if arg1 == 15:
            test_arduino_to_pc_completed.set()
        return arg2


test_arduino_to_pc_completed = Event()

if __name__ == "__main__":
    rpc = ArduinoRpc()
    rpc.connect()
    card_name = rpc.get_card_name()
    print("Connected to: " + card_name)

    print("First cicle of 15 pings")
    rpc.execute_remote_function("go")
    test_arduino_to_pc_completed.wait()
    rpc.execute_remote_function("halt")

    print("Second cicle of 15 pings")
    test_arduino_to_pc_completed.clear()
    rpc.execute_remote_function("go")
    test_arduino_to_pc_completed.wait()
    rpc.execute_remote_function("halt")

    print("Test ends")
    rpc.disconnect()
```
You can find another real complete use case in the source path:
* ArduinoPythonSerialRpc\tests\integration\sketch
* ArduinoPythonSerialRpc\tests\integration\java

### Build and run 
Python and Arduino communication is performed by the way of pyserial external library:

In order to execute the integration example test, please follows this steps:
* Open the sketch ArduinoPythonSerialRpc\tests\integration\sketch\sketch.ino
* Download it into your Arduino Card
* Open a terminal and go to ArduinoPythonSerialRpc\tests\integration\python
* Execute the following command
```bash
python integration_test.py
```

### Next steps
* ArduinoPythonSerialRpc tutorial - A tutorial to discover a more complex use of library (On Working)
* www.mauxilium.it - The reference site for my other projects (On Working)
