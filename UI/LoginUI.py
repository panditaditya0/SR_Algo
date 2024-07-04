import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtCore import QThread, Signal, Slot, QSize
import Auth
from MainAppUI import MainApp

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")

        self.layout = QVBoxLayout()

        self.client_name_label = QLabel("Client Name:")
        self.layout.addWidget(self.client_name_label)

        self.client_name_input = QLineEdit(self)
        self.layout.addWidget(self.client_name_input)
        self.client_name_input.setText("")

        self.secret_label = QLabel("Secret:")
        self.layout.addWidget(self.secret_label)

        self.secret_input = QLineEdit(self)
        self.layout.addWidget(self.secret_input)
        self.secret_input.setText("")

        self.enter_button = QPushButton("Enter", self)
        self.enter_button.clicked.connect(self.on_enter)
        self.layout.addWidget(self.enter_button)

        self.message_label = QTextEdit(self)
        self.message_label.setReadOnly(True)
        self.layout.addWidget(self.message_label)

        self.multiply_input = QLineEdit(self)
        self.multiply_input.setPlaceholderText("Enter number * 3")
        self.layout.addWidget(self.multiply_input)
        self.multiply_input.setVisible(False)

        self.validate_button = QPushButton("Validate", self)
        self.validate_button.clicked.connect(self.on_validate)
        self.layout.addWidget(self.validate_button)
        self.validate_button.setVisible(False)

        self.setLayout(self.layout)

    def on_enter(self):
        global session
        response, session = Auth.get_access_token(self.client_name_input.text(), self.secret_input.text(), self)
        self.message_label.setText(response)
        self.multiply_input.setVisible(True)
        self.validate_button.setVisible(True)

    def on_validate(self):
        Auth.get_access_token2(self.multiply_input.text(), session)
        self.main_app = MainApp()
        self.main_app.show()
        self.close()


    @Slot(str)
    def display_message(self, message):
        self.message_label.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginApp()
    login.show()
    sys.exit(app.exec())