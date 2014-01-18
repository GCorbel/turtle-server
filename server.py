import RPi.GPIO as GPIO
import socket
import json
import sys
from optparse import OptionParser

def main():
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", help="The port of destination")
    (options, args) = parser.parse_args()

    if options.port is None:
        print("You must to a port")
    else:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', int(options.port)))
        s.listen(1)
        conn, addr = s.accept()

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7, GPIO.OUT)

        try:
            while True:
                received_text = conn.recv(1024).decode()
                for key, value in json.loads(received_text).items():
                    GPIO.output(int(key), int(value))
                conn.sendall(bytes(1))
        finally:
            conn.close()
            GPIO.cleanup()

if __name__ == "__main__":
    main()
