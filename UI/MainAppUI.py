from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtCore import QThread, Signal, Slot, QSize, QRect
import SupportResistance

class Worker(QThread):
    update = Signal(dict)

    def __init__(self, support_input, resistance_input, dataLabel):
        super().__init__()
        self.support_input = support_input
        self.resistance_input = resistance_input
        self.dataLabel = dataLabel

    def run(self):
        support_value = self.support_input.text()
        resistance_value = self.resistance_input.text()
        SupportResistance.supportAndResistance(float(support_value), float(resistance_value), self)


class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Support and Resistance")

        self.layout = QVBoxLayout()

        self.support_label = QLabel("Support:")
        self.layout.addWidget(self.support_label)
        self.setFixedSize(QSize(1000, 700))

        self.support_input = QLineEdit(self)
        self.layout.addWidget(self.support_input)

        self.resistance_label = QLabel("Resistance:")
        self.layout.addWidget(self.resistance_label)

        self.resistance_input = QLineEdit(self)
        self.layout.addWidget(self.resistance_input)
        self.resistance_input.setFixedSize(10,150)


        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.on_start)
        self.layout.addWidget(self.start_button)

        self.data_label = QTextEdit(self)
        self.data_label.setReadOnly(True)
        self.layout.addWidget(self.data_label)
        self.data_label.setVisible(False)
        self.data_label.setFixedHeight(40)

        self.message_label = QTextEdit(self)
        self.message_label.setReadOnly(True)
        self.layout.addWidget(self.message_label)

        self.setLayout(self.layout)


        self.worker = None

    def on_start(self):
        self.resistance_label.setVisible(False)
        self.resistance_input.setVisible(False)
        self.support_input.setVisible(False)
        self.support_label.setVisible(False)
        self.start_button.setVisible(False)
        self.data_label.setVisible(True)
        if self.worker is None or not self.worker.isRunning():
            self.data_label.setText(f"Support = {self.support_input.text()} Resistance = {self.resistance_input.text()}")
            self.worker = Worker(self.support_input, self.resistance_input,  self.data_label)
            self.worker.update.connect(self.display_message)
            self.worker.start()


    @Slot(str)
    def display_message(self,message):
        self.data_label.setText(message["log"])
        self.message_label.append(message["message"])
        self.message_label.verticalScrollBar().setValue(self.message_label.verticalScrollBar().maximum())