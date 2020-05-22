#include <ArduinoSerialRpc.h>

boolean testRunning = false;
boolean sendingTestActive = false;
int sendIndex = 0;

ArduinoSerialRpc rpc("Full Tutorial Sketch (www.mauxilium.it)");

void setup() {
  Serial.begin(9600);

  rpc.registerArduinoFunction("Start", testStart);
  rpc.registerArduinoFunction("Switch", testSwitch);
  rpc.registerArduinoFunction("Stop", testStop);

  rpc.registerArduinoFunction("FloatCallPcToArduino", floatCall);
  rpc.registerArduinoFunction("StringCallPcToArduino", stringCall);
  rpc.registerArduinoFunction("IntCallPcToArduino", intCall);
}

void serialEvent() {
  rpc.serialEventHandler();
}


void testStart() {
  testRunning = true;
}

void testSwitch() {
  sendingTestActive = true;
}

void testStop() {
  testRunning = false;
  sendingTestActive = false;
  sendIndex = 0;
}


float floatCall(float arg) {
  return 3.1*arg;
}

String stringCall(String arg) {
  return arg + arg + arg;
}

int intCall(int arg1, int arg2) {
  return arg1*arg2;
}


void loop() {
  delay(10);
  if (sendingTestActive) {
    if (++sendIndex < 4) {
      rpc.executeRemoteMethod("string_call_arduino_to_pc", String(13*sendIndex));
      rpc.executeRemoteMethod("float_call_arduino_to_pc", 18.11*sendIndex);
      rpc.executeRemoteMethod("int_call_arduino_to_pc", sendIndex, 27*sendIndex);
    } else {
      rpc.executeRemoteMethod("arduino_ends");
      sendingTestActive = false;
    }
  }
}
