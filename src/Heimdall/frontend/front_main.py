from ui_file_func import *
from PyQt5.QtWidgets import QApplication
from sys import exit
from webbrowser import open as web_open


if __name__ == "__main__":
    app = QApplication([])
    window = Ui_MainWindow()
    window.config = get_config(CONFIG_PATH)
    winThread = WindowUpdateThread(window)
    winThread.start()
    window.submitButton.clicked.connect(window.getConfigValues)
    window.dashboardButton.clicked.connect(lambda: web_open(DASHBOARD_URL))
    window.scanButton.clicked.connect(lambda: call_process(['sh', str(PATH_TO_START_SCRIPT)]))
    try:
        
        with open(str(STYLEPATH), "r") as file:
            _style = file.read()
            app.setStyleSheet(_style)
    except:
        pass

    window.show()
    exit(app.exec_())
