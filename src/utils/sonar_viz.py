import time
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt


class PolarSonarVisualizer:
    """
    Single-thread visualizer:
    - submit(sonar) salva l'ultimo frame
    - update_plot() normalizza e disegna (rate-limited)
    """

    def __init__(self, azimuth_deg, range_min, range_max, plot_hz=3.0, cmap="gray", ema_alpha=0.1):
        self.azimuth_deg = float(azimuth_deg)
        self.range_min = float(range_min)
        self.range_max = float(range_max)
        self.plot_hz = float(plot_hz)
        self.cmap = cmap
        self.ema_alpha = float(ema_alpha)

        self.last_plot_time = 0.0
        self.initialized = False
        self.mesh = None

        # scaling state (EMA of min/max)
        self._lo = None
        self._hi = None

        self._latest = None
        self._closed = False

        plt.ion()
        self.fig, self.ax = plt.subplots(subplot_kw=dict(polar=True))
        self.ax.set_theta_zero_location("N")
        self.ax.set_thetamin(-self.azimuth_deg / 2)
        self.ax.set_thetamax(+self.azimuth_deg / 2)
        self.ax.set_ylim(self.range_min, self.range_max)
        self.ax.grid(False)

        self.fig.canvas.mpl_connect("close_event", lambda evt: self.close())

    def close(self):
        if self._closed:
            return
        self._closed = True
        try:
            plt.close(self.fig)
        except Exception:
            pass

    def _init_mesh(self, sonar_shape):
        R, A = sonar_shape
        theta = np.linspace(-self.azimuth_deg / 2, +self.azimuth_deg / 2, A) * np.pi / 180.0
        r = np.linspace(self.range_min, self.range_max, R)
        Theta, Rg = np.meshgrid(theta, r)

        self.mesh = self.ax.pcolormesh(
            Theta, Rg,
            np.zeros((R, A), dtype=np.uint8),
            cmap=self.cmap,
            shading="auto",
            vmin=0, vmax=255
        )
        self.fig.canvas.draw()
        self.initialized = True

    def submit(self, sonar: np.ndarray):
        if self._closed or sonar is None:
            return
        if sonar.ndim == 3:
            sonar = sonar[..., 0]
        self._latest = sonar

    def update_plot(self):
        if self._closed:
            return
        if self.fig is None or not plt.fignum_exists(self.fig.number):
            self.close()
            return

        now = time.time()
        if now - self.last_plot_time < 1.0 / self.plot_hz:
            plt.pause(0.001)
            return

        sonar = self._latest
        if sonar is None:
            plt.pause(0.001)
            return

        # normalize -> u8 (EMA min/max)
        a = sonar.astype(np.float32)
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
        u8 = (a * 255.0).astype(np.uint8)

        if not self.initialized:
            self._init_mesh(u8.shape)

        # draw
        try:
            self.mesh.set_array(u8.ravel())
            self.fig.canvas.draw_idle()
            plt.pause(0.001) 
        except Exception:
            return

        self.last_plot_time = now
