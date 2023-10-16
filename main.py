# main.py
from PyQt5.QtWidgets import QApplication
from app import FacebookRegistrationApp
import sys
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FacebookRegistrationApp()
    window.show()
    sys.exit(app.exec_())
