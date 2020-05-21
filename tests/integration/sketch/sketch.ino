#include <ArduinoRpc.h>

boolean testRunning = false;
boolean sendingTestActive = false;
int sendIndex = 0;

ArduinoRpc rpc("Full Tutorial Sketch (www.mauxilium.it)");

void setup() {
  Serial.begin(9600);

  rpc.registerArduinoAction("Start", testStart);
  rpc.registerArduinoAction("Switch", testSwitch);
  rpc.registerArduinoAction("Stop", testStop);

  rpc.registerArduinoAction("FloatCallPcToArduino", floatCall);
  rpc.registerArduinoAction("StringCallPcToArduino", stringCall);
  rpc.registerArduinoAction("IntCallPcToArduino", intCall);
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
      rpc.executeRemoteAction("string_call_pc_to_arduino", String(13*sendIndex));
      rpc.executeRemoteAction("float_call_pc_to_arduino", 18.11*sendIndex);
      rpc.executeRemoteAction("int_call_pc_to_arduino", sendIndex, 27*sendIndex);
    } else {
      rpc.executeRemoteAction("arduino_ends");
      sendingTestActive = false;
    }
  }
}
