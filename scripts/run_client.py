from src.gaze.gaze_client import GazeClient
from src.gaze.gaze_visualizer import GazeVisualizer

SCREEN_RES = (1920, 1080)


def main():
    with (
        GazeVisualizer(SCREEN_RES) as gaze_visualizer,
        GazeClient(server_ip_address="192.168.0.102") as gaze_client,
    ):
        while True:
            if not gaze_visualizer.display_gaze_pt(gaze_client.gaze_px_x_y):
                return


if __name__ == "__main__":
    main()
