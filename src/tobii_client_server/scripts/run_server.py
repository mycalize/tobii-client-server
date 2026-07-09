import socket
import time

from tobii_client_server.gaze.gaze_server import GazeServer
from tobii_client_server.tobii.tobii_eye_tracker import TobiiEyeTracker

SCREEN_RES = (1920, 1080)


def main():
    with GazeServer(ip_address=socket.gethostbyname(socket.gethostname())) as gaze_server:
        with TobiiEyeTracker(SCREEN_RES, gaze_server.send_data):
            try:
                # Using a polling mechanism instead of a `threading.Event` object because keyboard
                # interrupt cannot break `threading.Event().wait()`
                while True:
                    time.sleep(1000000)
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
