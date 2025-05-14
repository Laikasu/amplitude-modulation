from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QDoubleSpinBox, QSpinBox, QGroupBox, QTabWidget, QVBoxLayout, QGridLayout, QDockWidget
from PySide6.QtCore import Signal

class ParameterWindow(QDockWidget):
    """Window where you set the parameters."""
    params_changed = Signal(tuple)
        
    # def clip_phase_x(self, value):
    #     if np.abs(value>=180):
    #         self.phase_x.blockSignals(True)
    #         self.phase_x.setValue(((value + 180) % 360) - 180)
    #         self.phase_x.blockSignals(False)
    
    # def clip_phase_y(self, value):
    #     if np.abs(value>=180):
    #         self.phase_y.blockSignals(True)
    #         self.phase_y.setValue(((value + 180) % 360) - 180)
    #         self.phase_y.blockSignals(False)
    
    def emit_params(self):
        self.params_changed.emit((self.A.value(), self.f.value(), self.phase.value(), self.SNR.value(), self.ref_f.value(), self.ref_phase.value()))

    def __init__(self, name, parent=None):
        super().__init__(name, parent)

        # All parameters
        self.A = QDoubleSpinBox(minimum=0.1, maximum=10, value=1, singleStep=0.1, suffix="V")
        self.f = QDoubleSpinBox(minimum=0.1, maximum=100, value=5, singleStep=0.1, suffix="rad/s")
        self.phase = QDoubleSpinBox(minimum=0, maximum=10, value=1, singleStep=0.1, suffix="rad")
        self.SNR = QDoubleSpinBox(minimum=0.01, maximum=100, value=0.1, singleStep=0.1)

        self.integr = QSpinBox(minimum=1, maximum=1000, value=100, singleStep=10, suffix=' periods')

        self.ref_f = QDoubleSpinBox(minimum=0, maximum=10000, value=0, singleStep=0.1, decimals=3, suffix="rad/s")
        self.ref_phase = QDoubleSpinBox(minimum=0, maximum=100, value=0, singleStep=0.1, suffix="rad")

        for param in [self.A, self.f, self.phase, self.SNR, self.ref_f, self.ref_phase, self.integr]:
            param.valueChanged.connect(self.emit_params)

        
        

        self.signal_group = QGroupBox("Signal Parameters")
        signal_layout = QFormLayout()
        signal_layout.addRow('Amplitude', self.A)
        signal_layout.addRow('frequency', self.f)
        signal_layout.addRow('phase', self.phase)
        signal_layout.addRow('SNR', self.SNR)
        self.signal_group.setLayout(signal_layout)

        self.reference_group = QGroupBox("Reference Parameters")
        reference_layout = QFormLayout()
        reference_layout.addRow('frequency', self.ref_f)
        reference_layout.addRow('phase', self.ref_phase)
        reference_layout.addRow('integration time', self.integr)
        self.reference_group.setLayout(reference_layout)

        self.widget = QWidget(self)
        layout = QVBoxLayout()
        layout.addWidget(self.signal_group)
        layout.addWidget(self.reference_group)
        layout.addStretch(1)
        
        self.widget.setLayout(layout)
        self.setWidget(self.widget)