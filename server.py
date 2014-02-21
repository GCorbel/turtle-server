import RPIO.PWM as PWM
import RPIO
import socket
import json
import sys
import threading

servo = PWM.Servo()

watchdog = 10

def check ():
    global watchdog
    threading.Timer(1, check).start ()
    watchdog -= 1
    print (watchdog)
    if watchdog == 0:
        servo.set_servo(25, 1090)
        watchdog = 10


port = 8081

check()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
print ("waiting on port: ", port)
while 1:

    recv_data, addr = s.recvfrom(1024)

    received_text = recv_data.decode()

    for key, value in json.loads(received_text).items():
        if int(key) == 0 :
            watchdog = 10

        else:
            print("%d=%d" % (int(key),int(value)))
            servo.set_servo(int(key), int(value))

print("ready")
servo.set_servo(18, 1500)
servo.set_servo(23, 1500)
servo.set_servo(4, 1500)
servo.set_servo(25, 1090)
RPIO.wait_for_interrupts()
