import logging
import socket
import struct

# "!ii" means: network byte order (big-endian), and two standard integers (4 bytes each)
DATA_FORMAT = "!ii"


class GazeServer:
    def __init__(self, ip_address="localhost", port=7700, log_level="INFO"):
        self._address = (ip_address, port)
        self.sock = None
        self.client_conn = None

        # Set-up logging
        formatter = logging.Formatter("[Gaze Server][{levelname}]: {message}", style="{")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(handler)

    def __enter__(self):
        self.sock = socket.create_server(self._address, backlog=1)

        # Make the server listening socket non-blocking so `send_data()` doesn't block waiting for a
        # new client connection
        self.sock.setblocking(False)

        self._logger.info(f"Gaze server started at {self._address[0]}:{self._address[1]}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.sock is not None:
            self.sock.close()

        if self.client_conn is not None:
            self.client_conn.close()

    def send_data(self, gaze_x_y_px):
        if self.client_conn is None:
            try:
                self.client_conn, _ = self.sock.accept()
            except BlockingIOError:
                return

        # Pack the data into bytes
        packed_data = struct.pack(DATA_FORMAT, *gaze_x_y_px)

        try:
            self.client_conn.sendall(packed_data)
        except Exception:
            self._logger.warning(
                "Connection with client failed. Waiting for client to reconnect..."
            )
            self.client_conn.close()
            self.client_conn = None
