from PyQt5.QtWidgets import QApplication
from sys import exit
from ui_file_func import *

if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MainWindow()
    window.config = get_config(CONFIG_PATH)
    winThread = WindowUpdateThread(window)
    winThread.start()
    window.submitButton.clicked.connect(lambda: window.getConfigValues())
    try:
        with open("./style.qss", "r") as file:
            _style = file.read()
            app.setStyleSheet(_style)
    except:
        pass

    window.show()
    exit(app.exec_())
