import numpy as np
import tobii_research as tr


class TobiiEyeTracker:
    def __init__(self, screen_res, send_data_callback=None):
        self.screen_res = screen_res
        self.send_data_callback = send_data_callback

        eye_trackers = tr.find_all_eyetrackers()
        if len(eye_trackers) < 1:
            raise RuntimeError("No Tobii eye trackers detected")

        # Assumes that only one Tobii eye tracker is connected
        self.eye_tracker = tr.find_all_eyetrackers()[0]

        self.gaze_px = None

    def __enter__(self):
        self.eye_tracker.subscribe_to(
            tr.EYETRACKER_GAZE_DATA, self._update_gaze, as_dictionary=True
        )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self._update_gaze)

    def _update_gaze(self, gaze_data):
        # Gaze point given in Active Display Coordinate System, where (0, 0) denotes the upper left
        # corner and (1, 1) the lower right corner
        gaze_frac_left = gaze_data["left_gaze_point_on_display_area"]
        gaze_frac_right = gaze_data["right_gaze_point_on_display_area"]

        # Stack left and right gaze
        gaze_frac = np.vstack((gaze_frac_left, gaze_frac_right))

        if np.isnan(gaze_frac).all(axis=0).any():
            self.gaze_px = None
            return

        # Find mean gaze point of left and right eyes (clipping so the gaze point stays within the
        # display area)
        gaze_frac_mean = np.nanmean(gaze_frac, axis=0)
        gaze_frac_mean = np.clip(gaze_frac_mean, 0, 1)
        gaze_px_mean = gaze_frac_mean * self.screen_res

        # Update gaze point
        self.gaze_px = gaze_px_mean.round().astype(int)

        # Send gaze point
        if self.send_data_callback is not None:
            self.send_data_callback(self.gaze_px)
