# https://github.com/waveform80/picamera/issues/226

import socket
import time
import picamera

SOCKET = 8000

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.connect(('192.168.4.162', SOCKET))
except:
    print("Unable to bind to socket %s" % SOCKET)
    exit()

# Make a file-like object out of the connection
connection = socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()
finally:
    connection.close()
    socket.close()
