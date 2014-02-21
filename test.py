import RPIO.PWM as PWM
import RPIO
import socket
import json
import sys

servo = PWM.Servo()

def socket_callback(socket, val):
    print(val)
    received_text = val.decode()
    print(received_text)
    for key, value in json.loads(received_text).items():
        print("%d=%d" % (int(key), int(value)))
        servo.set_servo(int(key), int(value))
    socket.send(b"ok")

RPIO.add_tcp_callback(8081, socket_callback)

print("ready")
servo.set_servo(18, 1500)
servo.set_servo(23, 1500)
servo.set_servo(4, 1500)
servo.set_servo(25, 1090)
RPIO.wait_for_interrupts()
