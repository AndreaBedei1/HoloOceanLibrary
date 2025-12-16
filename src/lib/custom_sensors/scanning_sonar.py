import numpy as np
import torch


class ScanningImagingSonar:
    """
    Imaging-sonar-like reconstruction from SinglebeamSonar data.
    - We therefore reconstruct an image over time by stacking profiles.
    """

    def __init__(
        self,
        # azimuth_deg: float = 80.0,
        azimuth_bins: int = 256,
        range_bins: int = 512,
        range_max: float = 50.0,
        device: str = "cuda",
    ):
        self.azimuth_bins = azimuth_bins
        self.range_bins = range_bins
        self.range_max = range_max
        self.device = device

        # Column pointer
        self.col = 0

        # Sonar image buffer (range x azimuth)
        self.buffer = torch.zeros(
            (range_bins, azimuth_bins),
            device=device,
            dtype=torch.float32
        )

        # Range vector (for TVG)
        self.ranges = torch.linspace(
            1.0, range_max, range_bins, device=device
        )

    # --------------------------------------------------

    def step(self, profile):
        """
        profile: 1D numpy array (range_bins,)
        """

        self.buffer[:, self.col] = torch.as_tensor(
            profile, device=self.device
        )

        self.col += 1

        if self.col < self.azimuth_bins:
            return None

        self.col = 0
        return self._build_image()


    # --------------------------------------------------

    def _build_image(self):
        """
        Build the imaging-sonar-like image.
        """

        with torch.no_grad():
            # Time-Varying Gain (TVG)
            tvg = (self.ranges ** 2).unsqueeze(1)
            img = self.buffer * tvg

            # Log compression
            img = torch.log1p(img)

            # Normalize
            img = img / (img.max() + 1e-6)

            # Convert to uint8
            img = (img * 255).to(torch.uint8)

            # (azimuth x range) for visualization
            return img.T.contiguous().cpu().numpy()
