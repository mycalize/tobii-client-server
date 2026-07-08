import pygame

from src.gaze.gaze_point import GazePoint


class GazeVisualizer:
    def __init__(
        self,
        screen_res,
        fps_limit=20,
    ):
        self.screen_res = screen_res
        self.fps_limit = fps_limit

    def __enter__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        flags = pygame.FULLSCREEN
        self.screen = pygame.display.set_mode(self.screen_res, flags)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pygame.quit()

    def display_gaze_pt(self, gaze_pt_px):
        # Poll for events.
        # `pygame.QUIT`` event means the user clicked X to close the window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        # Exit if "q" is pressed.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            return False

        self.screen.fill("black")

        if gaze_pt_px is None:
            return True

        gaze_pt = GazePoint(
            pos=gaze_pt_px,
            inner_radius=5.0,
            outer_radius=5.0,
            color="red",
        )
        gaze_pt.draw(self.screen)

        pygame.display.flip()

        return True
