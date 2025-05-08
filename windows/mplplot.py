import numpy as np
from matplotlib import use
use("Agg")

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QFileDialog, QDockWidget, QVBoxLayout, QMenuBar
from PySide6.QtCore import QStandardPaths, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt



class MplPlot(FigureCanvasQTAgg):
    def update_figure(self, A_sig=1, f_sig=5, phi_sig=0, SNR=0, f_ref=5, phi_ref=0):
        # === input parameters ===
        # signal
        #A_sig = 1  # signal amplitude (V)
        #f_sig = 5  # signal frequency (rad/s)
        #phi_sig = 0  # absolute phase of signal (rad)
        #SNR = 0.1  # SNR of the signal, noise is shot noise (white spectrum)

        # reference
        #f_ref = 5  # Modulation frequency (rad/s)
        #phi_ref = 0  # absolute phase of reference (rad)
        # === end input ===

        # =================

        # Create signal and noisy baseline
        x = np.arange(0, 2000 * 1 / f_sig, 0.1)  # time axis (s)
        noise = 1 / SNR * np.random.randn(len(x))  # noise
        baseline = noise + 40  # noise + baseline
        y = A_sig * (1 + np.sin(f_sig * x + phi_sig))  # pure signal
        ynoise = y + baseline  # noisy signal

        # Calculate SNR of original signal
        SignalToNoiseRatio = A_sig / np.std(baseline)

        # Generate reference
        reference = np.sin(f_ref * x + phi_ref)  # 50 percent duty-cycle sine wave modulation

        # Synchronous Detection (e.g. Lock-in amplifier)
        dy = ynoise * reference
        V_avg = np.mean(dy)

        # Plotting
        plt.clf()
        plt.subplot(3, 2, 3)
        plt.plot(x, reference, color="#77AC30")
        plt.xlim([0, 10])
        plt.xlabel('time (s)')
        plt.ylabel('$V_{ref}$ (V)')
        plt.title(f'reference f = {f_ref:0.2f} rad/s')

        plt.subplot(3, 2, 1)
        plt.plot(x, y, 'r')
        plt.xlim([0, 10])
        plt.xlabel('time (s)')
        plt.ylabel('$V_s$ (V)')
        plt.title(f'signal f = {f_sig:0.2f} rad/s')

        plt.subplot(3, 2, 2)
        plt.plot(x, ynoise, 'r')
        plt.xlim([0, 10])
        plt.ylim([0, 1.1 * np.max(ynoise)])
        plt.xlabel('time (s)')
        plt.ylabel('$V_s$ (V)')
        plt.title(f'signal + noise, SNR = {SNR:0.1f}')

        plt.subplot(3, 2, 4)
        plt.plot(x, dy, color="#EDB120")
        plt.xlim([0, 10])
        plt.xlabel('time (s)')
        plt.ylabel('$V_s$ (V)')
        plt.title('Mixed signal $V_p$')

        plt.subplot(3, 2, (5, 6))
        plt.barh([0], [V_avg])
        plt.xlabel('recovered $V_{avg}$ (V)')
        plt.xlim([0, 1])
        plt.yticks([])

        plt.tight_layout()
        plt.draw()

    def __init__(self, parent=None):
        fig = plt.figure(figsize=(6, 7))
        plt.tight_layout()
        super().__init__(fig)

    def save(self):
        loc = QStandardPaths.writableLocation(QStandardPaths.PicturesLocation)
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Figure", loc,"Image Files(*.png *.jpg)")
        if filepath:
            self.figure.savefig(filepath)