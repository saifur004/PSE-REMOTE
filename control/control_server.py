import socket
import RPi.GPIO as GPIO

MOTOR_FORWARD = 17
MOTOR_BACKWARD = 18
MOTOR_LEFT = 22
MOTOR_RIGHT = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)
GPIO.setup(MOTOR_LEFT, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT, GPIO.OUT)

def move_forward():
    GPIO.output(MOTOR_FORWARD, GPIO.HIGH)
    GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
    print("Moving Forward")

def move_backward():
    GPIO.output(MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_BACKWARD, GPIO.HIGH)
    print("Moving Backward")

def turn_left():
    GPIO.output(MOTOR_LEFT, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT, GPIO.LOW)
    print("Turning Left")

def turn_right():
    GPIO.output(MOTOR_LEFT, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT, GPIO.HIGH)
    print("Turning Right")

def stop():
    GPIO.output(MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
    GPIO.output(MOTOR_LEFT, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT, GPIO.LOW)
    print("Stopping")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 6000))  # Listening on port 6000
server.listen(5)

print("Waiting for commands...")

try:
    while True:
        client_socket, addr = server.accept()
        command = client_socket.recv(1024).decode()
        print(f"Received command: {command}")

        if command == "forward":
            move_forward()
        elif command == "backward":
            move_backward()
        elif command == "left":
            turn_left()
        elif command == "right":
            turn_right()
        elif command == "stop":
            stop()

        client_socket.close()
except KeyboardInterrupt:
    print("Stopping server...")
    GPIO.cleanup()
    server.close()