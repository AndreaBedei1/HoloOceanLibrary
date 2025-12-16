import time
import threading
from queue import Queue, Empty
import numpy as np
import matplotlib.pyplot as plt

try:
    import torch
    _TORCH_OK = True
except Exception:
    _TORCH_OK = False


class PolarSonarVisualizerAsync:
    """
    Main thread: renders matplotlib.
    Worker thread: preprocesses sonar -> uint8 (CPU or CUDA).
    """

    def __init__(self, azimuth_deg, range_min, range_max, plot_hz=3.0, cmap="gray",
                 use_cuda=True, ema_alpha=0.1):
        self.azimuth_deg = azimuth_deg
        self.range_min = range_min
        self.range_max = range_max
        self.plot_hz = plot_hz
        self.cmap = cmap

        self.use_cuda = bool(use_cuda and _TORCH_OK and torch.cuda.is_available())
        self.ema_alpha = float(ema_alpha)

        self.last_plot_time = 0.0
        self.initialized = False
        self.mesh = None

        # robust scaling state (EMA of lo/hi)
        self._lo = None
        self._hi = None

        # latest-only queues
        self.in_q = Queue(maxsize=1)
        self.out_q = Queue(maxsize=1)
        self._running = True
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

        plt.ion()
        self.fig, self.ax = plt.subplots(subplot_kw=dict(polar=True))
        self.ax.set_theta_zero_location("N")
        self.ax.set_thetamin(-self.azimuth_deg / 2)
        self.ax.set_thetamax(+self.azimuth_deg / 2)
        self.ax.set_ylim(self.range_min, self.range_max)
        self.ax.grid(False)

    def close(self):
        self._running = False

    def _init_mesh(self, sonar_shape):
        R, A = sonar_shape
        theta = np.linspace(-self.azimuth_deg/2, +self.azimuth_deg/2, A) * np.pi/180
        r = np.linspace(self.range_min, self.range_max, R)
        Theta, Rg = np.meshgrid(theta, r)

        self.mesh = self.ax.pcolormesh(
            Theta, Rg,
            np.zeros((R, A), dtype=np.uint8),
            cmap=self.cmap, shading="auto", vmin=0, vmax=255
        )
        self.fig.canvas.draw()
        self.initialized = True

    def submit(self, sonar: np.ndarray):
        """Call from main loop: push latest sonar to worker (non-blocking)."""
        if sonar is None:
            return
        if sonar.ndim == 3:
            sonar = sonar[..., 0]

        # latest-only semantics
        try:
            while True:
                self.in_q.get_nowait()
        except Empty:
            pass

        try:
            self.in_q.put_nowait(sonar)
        except Exception:
            pass

    def update_plot(self):
        """Call from main loop: render if new processed frame is ready."""
        now = time.time()
        if now - self.last_plot_time < 1.0 / self.plot_hz:
            return

        try:
            u8 = self.out_q.get_nowait()
        except Empty:
            return

        if not self.initialized:
            self._init_mesh(u8.shape)

        self.mesh.set_array(u8.ravel())
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        self.last_plot_time = now

    # ---------- worker ----------
    def _worker_loop(self):
        device = "cuda" if self.use_cuda else "cpu"

        while self._running:
            try:
                sonar = self.in_q.get(timeout=0.1)
            except Empty:
                continue

            u8 = self._normalize_to_u8(sonar, device=device)

            # latest-only output
            try:
                while True:
                    self.out_q.get_nowait()
            except Empty:
                pass

            try:
                self.out_q.put_nowait(u8)
            except Exception:
                pass

    def _normalize_to_u8(self, img: np.ndarray, device="cpu") -> np.ndarray:
        """
        Fast robust normalization.
        Instead of per-frame percentiles (slow), use EMA on lo/hi computed from min/max,
        or approximate quantiles via torch.quantile (still heavier).
        """
        if _TORCH_OK:
            t = torch.as_tensor(img, dtype=torch.float32, device=device)

            # cheap stats (min/max) + EMA: good enough for viz, much faster than percentiles
            lo = float(t.amin().item())
            hi = float(t.amax().item())

            if self._lo is None:
                self._lo, self._hi = lo, hi
            else:
                a = self.ema_alpha
                self._lo = (1 - a) * self._lo + a * lo
                self._hi = (1 - a) * self._hi + a * hi

            lo, hi = self._lo, self._hi
            if hi - lo < 1e-6:
                hi = lo + 1e-6

            t = (t - lo) / (hi - lo)
            t = t.clamp(0.0, 1.0)
            u8 = (t * 255.0).to(torch.uint8).cpu().numpy()
            return u8

        # CPU fallback
        a = img.astype(np.float32)
        lo = float(a.min())
        hi = float(a.max())
        if self._lo is None:
            self._lo, self._hi = lo, hi
        else:
            alpha = self.ema_alpha
            self._lo = (1 - alpha) * self._lo + alpha * lo
            self._hi = (1 - alpha) * self._hi + alpha * hi
        lo, hi = self._lo, self._hi

        if hi - lo < 1e-6:
            hi = lo + 1e-6
        a = np.clip((a - lo) / (hi - lo), 0.0, 1.0)
        return (a * 255).astype(np.uint8)
