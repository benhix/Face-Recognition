import sys
from PySide6.QtWidgets import QApplication
from mainScreen import MainWindow


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
