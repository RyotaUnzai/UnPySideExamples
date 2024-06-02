import sys
import time

from PySide6 import QtWidgets
from QAbstractProgressCircular import QAbstractProgressCircular


class Example(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(Example, self).__init__()

        self.initUI()

    def initUI(self) -> None:
        self.apc = QAbstractProgressCircular(self)
        self.apc.resize(100, 100)

        self.resize(500, 300)
        self.setWindowTitle("Statusbar")

    def progress_start(self) -> None:
        "Initiates a progress simulation for a given progress widget."
        value: int = 0
        while value <= 100:
            time.sleep(0.1)
            self.apc.value = value
            value += 5


def main() -> None:
    app = QtWidgets.QApplication([])
    ex = Example()
    ex.show()
    ex.progress_start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
