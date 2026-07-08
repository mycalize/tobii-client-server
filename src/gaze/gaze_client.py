import logging
import socket
import struct
import threading

from src.gaze.gaze_server import DATA_FORMAT


class GazeClient:
    def __init__(self, server_ip_address="localhost", server_port=7700, log_level="INFO"):
        self._server_addr = (server_ip_address, server_port)
        self.conn = None
        self.gaze_px_x_y = None

        self._running = False
        self._buffer = b""
        self._sample_len_bytes = struct.calcsize(DATA_FORMAT)

        # Set-up logging
        formatter = logging.Formatter("[Gaze Client][{levelname}]: {message}", style="{")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        self._logger.addHandler(handler)

    def __enter__(self):
        self._running = True

        # Start a daemon thread that is automatically killed whenever this program exits
        thread = threading.Thread(target=self._recv_loop, daemon=True)
        thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._running = False

        if self.conn is not None:
            self.conn.close()

    def _recv_data(self):
        # Read up to 4096 from the network receive buffer to try to drain buffer
        chunk = self.conn.recv(4096)

        if chunk == b"":
            raise ConnectionError("Connection with server broken")

        self._buffer += chunk

        num_samples = len(self._buffer) // self._sample_len_bytes
        if num_samples > 0:
            latest_sample_idx = (num_samples - 1) * self._sample_len_bytes
            latest_sample = self._buffer[
                latest_sample_idx : (latest_sample_idx + self._sample_len_bytes)
            ]

            # In the current implementation, a lock is unnecessary because the following assignment
            # is atomic
            self.gaze_px_x_y = struct.unpack(DATA_FORMAT, latest_sample)

            # Discard complete samples from `self._buffer`
            self._buffer = self._buffer[num_samples * self._sample_len_bytes :]

    def _recv_loop(self):
        while True:
            if self.conn is None:
                self.conn = socket.create_connection(self._server_addr)

            try:
                self._recv_data()
            except (ConnectionError, OSError) as e:
                if not self._running:
                    return

                self._logger.warning(f"Connection failed: {e}. Trying to reconnect...")

                self.conn.close()
                self.conn = None
                self._buffer = b""
