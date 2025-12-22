import cv2
import numpy as np


def show_camera(state, sensor_key, window_name=None):
    """
    Safely display a camera image from HoloOcean state.

    Parameters
    ----------
    state : dict
        Environment state returned by env.step()
    sensor_key : str
        Key of the camera sensor in the state dict
    window_name : str, optional
        OpenCV window name (defaults to sensor_key)
    """
    if sensor_key not in state:
        return

    img = state[sensor_key]

    if img is None:
        return

    img = np.asarray(img)

    # Handle RGBA -> RGB
    if img.ndim == 3 and img.shape[2] >= 3:
        img = img[:, :, :3]

    # Convert float images to uint8 if needed
    if img.dtype != np.uint8:
        img = np.clip(img * 255.0, 0, 255).astype(np.uint8)

    cv2.imshow(window_name or sensor_key, img)
