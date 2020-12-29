import socket
import subprocess

SOCKET = 8000

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket.bind(('0.0.0.0', SOCKET))

# Accept a single connection and make a file-like object out of it
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    cmdline = ['vlc', '--demux', 'h264', '-']
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read up to 128k of data from the connection and write it
        # to the media player's stdin; we deliberately use a large size here to
        # avoid truncating UDP messages
        data = socket.recv(131072)
        if not data:
            break
        player.stdin.write(data)
finally:
    socket.close()
    player.terminate()