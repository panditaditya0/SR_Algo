import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import QSize, QThread, Signal, Slot
import SupportResistance
from datetime import datetime


class Worker(QThread):
    update = Signal(dict)

    def __init__(self, support_input, resistance_input):
        super().__init__()
        self.support_input = support_input
        self.resistance_input = resistance_input

    def run(self):
        support_value = self.support_input.text()
        resistance_value = self.resistance_input.text()
        SupportResistance.supportAndResistance(float(support_value), float(resistance_value), self)


def get_new_value(new_value, old_value):
    try:
        return float(new_value)
    except:
        float(old_value)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setFixedSize(QSize(1000, 700))

        self.resistance_label = QLabel("Resistance:")
        main_layout.addWidget(self.resistance_label)

        self.resistance_input = QLineEdit(self)
        main_layout.addWidget(self.resistance_input)

        self.support_label = QLabel("Support:")
        main_layout.addWidget(self.support_label)
        self.setFixedSize(QSize(1000, 700))

        self.support_input = QLineEdit(self)
        main_layout.addWidget(self.support_input)

        # support and resistance
        config_layout = QHBoxLayout()
        self.Sup_label = QLabel("Sup")
        self.Res_label2 = QLabel("Res")
        config_layout.addWidget(self.Sup_label)
        config_layout.addWidget(self.Res_label2)
        self.Sup_label.setVisible(False)
        self.Res_label2.setVisible(False)
        main_layout.addLayout(config_layout)

        display_config_layout = QHBoxLayout()
        self.sup_input = QLineEdit()
        self.res_input = QLineEdit()
        self.sup_input.setReadOnly(True)
        self.res_input.setReadOnly(True)
        self.sup_input.setVisible(False)
        self.res_input.setVisible(False)
        display_config_layout.addWidget(self.sup_input)
        display_config_layout.addWidget(self.res_input)
        main_layout.addLayout(display_config_layout)

        # Labels
        label_layout = QHBoxLayout()
        self.clock_label = QLabel("Clock")
        self.ltp_label2 = QLabel("LTP 1")
        self.ltp_label3 = QLabel("LTP 2")
        self.ltp_label4 = QLabel("LTP 3")
        label_layout.addWidget(self.clock_label)
        label_layout.addWidget(self.ltp_label2)
        label_layout.addWidget(self.ltp_label3)
        label_layout.addWidget(self.ltp_label4)
        main_layout.addLayout(label_layout)

        # Display Txt
        display_layout = QHBoxLayout()
        self.clock_input = QLineEdit()
        self.ltp_input2 = QLineEdit()
        self.ltp_input3 = QLineEdit()
        self.ltp_input4 = QLineEdit()
        display_layout.addWidget(self.clock_input)
        display_layout.addWidget(self.ltp_input2)
        display_layout.addWidget(self.ltp_input3)
        display_layout.addWidget(self.ltp_input4)
        self.clock_input.setReadOnly(True)
        self.clock_input.setText(datetime.now().strftime("%H:%M:%S"))
        self.ltp_input2.setText("0")
        self.ltp_input3.setText("0")
        self.ltp_input4.setText("0")
        self.ltp_input2.setReadOnly(True)
        self.ltp_input3.setReadOnly(True)
        self.ltp_input4.setReadOnly(True)
        main_layout.addLayout(display_layout)

        #pnl layout
        pnl_layout = QHBoxLayout()
        self.pnl_label = QLabel("P&L")
        self.pnl_input = QLineEdit()
        pnl_layout.addWidget(self.pnl_label)
        pnl_layout.addWidget(self.pnl_input)
        self.pnl_input.setReadOnly(True)
        self.pnl_input.setText("0")
        main_layout.addLayout(pnl_layout)

        self.message_label = QTextEdit(self)
        self.message_label.setReadOnly(True)
        main_layout.addWidget(self.message_label)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.on_start)
        main_layout.addWidget(self.start_button)

        self.setLayout(main_layout)

        # Set window title and size
        self.setWindowTitle("PySide6 Layout Example")
        self.resize(400, 100)
        self.worker = None

    def on_start(self):
        self.Sup_label.setVisible(True)
        self.Res_label2.setVisible(True)
        self.sup_input.setVisible(True)
        self.res_input.setVisible(True)
        self.resistance_label.setVisible(False)
        self.resistance_input.setVisible(False)
        self.support_input.setVisible(False)
        self.support_label.setVisible(False)
        self.start_button.setVisible(False)
        self.sup_input.setText(self.support_input.text())
        self.res_input.setText(self.resistance_input.text())
        self.worker = Worker(self.support_input, self.resistance_input)
        self.worker.update.connect(self.display_message)
        self.worker.start()

    @Slot(str)
    def display_message(self, message):
        old_input1 = self.ltp_input2.text()
        old_input2 = self.ltp_input3.text()
        old_input3 = self.ltp_input4.text()
        self.ltp_label2.setText(message['symbol1'])
        self.ltp_label3.setText(message['symbol2'])
        self.ltp_label4.setText(message['symbol3'])
        self.Sup_label.setText(f"support: {message['support']}")
        self.Res_label2.setText(f"Resistance: {message['resistance']}")

        new_input1 = get_new_value(message["ltp1"], old_input1)
        new_input2 = get_new_value(message["ltp2"], old_input2)
        new_input3 = get_new_value(message["ltp3"], old_input3)

        self.ltp_input2.setText(str(new_input1))
        self.ltp_input3.setText(str(new_input2))
        self.ltp_input4.setText(str(new_input3))
        self.pnl_input.setText(str(message['pnl']))

        if float(message["pnl"] > 0):
            self.pnl_input.setStyleSheet("color: green")
        elif float(message["pnl"] < 0):
            self.pnl_input.setStyleSheet("color: red")
        else:
            self.pnl_input.setStyleSheet("color: yellow")

        if float(new_input1) > float(old_input1):
            self.ltp_input2.setStyleSheet("color: green")
        elif float(new_input1) < float(old_input1):
            self.ltp_input2.setStyleSheet("color: red")

        if float(new_input2) > float(old_input2):
            self.ltp_input3.setStyleSheet("color: green")
        elif float(new_input2) < float(old_input2):
            self.ltp_input3.setStyleSheet("color: red")

        if float(new_input3) > float(old_input3):
            self.ltp_input4.setStyleSheet("color: green")
        elif float(new_input3) < float(old_input3):
            self.ltp_input4.setStyleSheet("color: red")

        if message["log"] != "":
            self.message_label.append(message["log"])
            self.message_label.verticalScrollBar().setValue(self.message_label.verticalScrollBar().maximum())

    # def set_values(self, newValue, oldValue, new_input1):
    #     if float(newValue) > float(oldValue):
    #         new_input1.setText(newValue)
    #         new_input1.setStyleSheet("color: green")
    #     else:
    #         new_input1.setText(newValue)
    #         new_input1.setStyleSheet("color: red")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
