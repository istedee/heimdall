import yaml
from PyQt5.QtWidgets import  QWidget, QGroupBox, QLineEdit,  QLabel, QCheckBox, QPushButton, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, Qt, QSize, QThread
from time import sleep
from os import path
from pathlib import Path
from re import compile
from subprocess import call as process_call

CONFIG_PATH = Path(path.dirname(__file__)).parent.joinpath("config", "config.yml")
PATH_TO_SRC = Path(path.dirname(__file__)).parent.parent.absolute()
PATH_TO_START_SCRIPT = PATH_TO_SRC.joinpath("start_heimdall.sh")
STYLEPATH = Path(path.dirname(__file__)).absolute().joinpath("style.qss")
DASHBOARD_URL = "http://localhost:5601/app/dashboards#"

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config = get_config(CONFIG_PATH)

    def setupUi(self, MainWindow):
        """Setup UI for window

        Args:
            MainWindow (QMainWindow): Main window to init UI into
        """
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        
        self.setFixedSize(QSize(780, 400))

        font = QFont()
        font.setPointSize(8)
        font.setFamily("Consolas")

        font1 = QFont()
        font1.setPointSize(12)
        font1.setFamily("Consolas")

        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setWeight(50)
        font2.setFamily("Consolas")

        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setWeight(50)
        font3.setFamily("Consolas")

        MainWindow.setFont(font)

        self.setWindowIcon(QIcon("img/icon.png"))

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.setGroupBox = QGroupBox(self.centralwidget)
        self.setGroupBox.setObjectName(u"setGroupBox")
        self.setGroupBox.setGeometry(QRect(20, 20, 340, 360))

        self.setGroupBox.setFont(font1)
        self.setGroupBox.setAlignment(Qt.AlignCenter)

        self.setIpspaceLine = QLineEdit(self.setGroupBox)
        self.setIpspaceLine.setObjectName(u"setIpspaceLine")
        self.setIpspaceLine.setGeometry(QRect(40, 50, 260, 20))
        self.setIpspaceLine.setText(u"")
        self.setIpspaceLine.setMaxLength(15)
        self.setIpspaceLine.setFont(font3)
        self.setIpspaceLine.setAlignment(Qt.AlignCenter)

        self.setIpspaceLabel = QLabel(self.setGroupBox)
        self.setIpspaceLabel.setObjectName(u"setIpspaceLabel")
        self.setIpspaceLabel.setGeometry(QRect(40, 30, 260, 20))
        self.setIpspaceLabel.setFont(font2)
        self.setIpspaceLabel.setAlignment(Qt.AlignCenter)

        self.setSubnetLine = QLineEdit(self.setGroupBox)
        self.setSubnetLine.setObjectName(u"setSubnetLine")
        self.setSubnetLine.setGeometry(QRect(70, 100, 61, 20))
        self.setSubnetLine.setMaxLength(3)
        self.setSubnetLine.setFont(font3)
        self.setSubnetLine.setAlignment(Qt.AlignCenter)
        
        self.setSubnetLabel = QLabel(self.setGroupBox)
        self.setSubnetLabel.setObjectName(u"setSubnetLabel")
        self.setSubnetLabel.setGeometry(QRect(60, 80, 80, 20))
        self.setSubnetLabel.setFont(font2)
        self.setSubnetLabel.setAlignment(Qt.AlignCenter)

        self.setSleeptimeLine = QLineEdit(self.setGroupBox)
        self.setSleeptimeLine.setObjectName(u"setSleeptimeLine")
        self.setSleeptimeLine.setGeometry(QRect(210, 100, 60, 20))
        self.setSleeptimeLine.setFont(font3)
        self.setSleeptimeLine.setAlignment(Qt.AlignCenter)
        self.setSleeptimeLine.setMaxLength(7)

        self.setSleeptimeLabel = QLabel(self.setGroupBox)
        self.setSleeptimeLabel.setObjectName(u"setSleeptimeLabel")
        self.setSleeptimeLabel.setGeometry(QRect(196, 80, 90, 20))
        self.setSleeptimeLabel.setFont(font2)
        self.setSleeptimeLabel.setAlignment(Qt.AlignCenter)

        self.setVulndiscBox = QCheckBox(self.setGroupBox)
        self.setVulndiscBox.setObjectName(u"setVulndiscBox")
        self.setVulndiscBox.setGeometry(QRect(80, 250, 20, 40))
        self.setVulndiscBox.setLayoutDirection(Qt.RightToLeft)

        self.setPortscanBox = QCheckBox(self.setGroupBox)
        self.setPortscanBox.setObjectName(u"setPortscanBox")
        self.setPortscanBox.setGeometry(QRect(246, 260, 20, 21))
        self.setPortscanBox.setLayoutDirection(Qt.RightToLeft)
        self.setPortscanBox.setIconSize(QSize(16, 16))
        self.setPortscanBox.setCheckable(True)
        self.setPortscanBox.setTristate(False)

        self.setVulndiscLabel = QLabel(self.setGroupBox)
        self.setVulndiscLabel.setObjectName(u"setVulndiscLabel")
        self.setVulndiscLabel.setGeometry(QRect(0, 240, 171, 21))
        self.setVulndiscLabel.setFont(font2)
        self.setVulndiscLabel.setAlignment(Qt.AlignCenter)

        self.setPortscanLabel = QLabel(self.setGroupBox)
        self.setPortscanLabel.setObjectName(u"setPortscanLabel")
        self.setPortscanLabel.setGeometry(QRect(170, 240, 171, 20))
        self.setPortscanLabel.setFont(font2)
        self.setPortscanLabel.setAlignment(Qt.AlignCenter)

        self.setPortscanGroupBox = QGroupBox(self.setGroupBox)
        self.setPortscanGroupBox.setObjectName(u"setPortscanGroupBox")
        self.setPortscanGroupBox.setGeometry(QRect(19, 139, 301, 71))
        self.setPortscanGroupBox.setFont(font2)
        self.setPortscanGroupBox.setAlignment(Qt.AlignCenter)

        self.setStartPortscanLine = QLineEdit(self.setPortscanGroupBox)
        self.setStartPortscanLine.setObjectName(u"setStartPortscanLine")
        self.setStartPortscanLine.setGeometry(QRect(60, 30, 61, 20))
        self.setStartPortscanLine.setFont(font2)
        self.setStartPortscanLine.setMaxLength(6)

        self.setEndPortscanLine = QLineEdit(self.setPortscanGroupBox)
        self.setEndPortscanLine.setObjectName(u"setEndPortscanLine")
        self.setEndPortscanLine.setGeometry(QRect(212, 30, 71, 20))
        self.setEndPortscanLine.setFont(font2)
        self.setEndPortscanLine.setMaxLength(6)

        self.setStartPortscanLabel = QLabel(self.setPortscanGroupBox)
        self.setStartPortscanLabel.setObjectName(u"setStartPortscanLabel")
        self.setStartPortscanLabel.setGeometry(QRect(10, 30, 51, 16))
        self.setStartPortscanLabel.setFont(font2)
        self.setStartPortscanLabel.setAlignment(Qt.AlignCenter)

        self.setEndPortscanLabel = QLabel(self.setPortscanGroupBox)
        self.setEndPortscanLabel.setObjectName(u"setEndPortscanLabel")
        self.setEndPortscanLabel.setGeometry(QRect(170, 30, 41, 16))
        self.setEndPortscanLabel.setFont(font2)
        self.setEndPortscanLabel.setAlignment(Qt.AlignCenter)

        self.submitButton = QPushButton(self.setGroupBox)
        self.submitButton.setObjectName(u"submitButton")
        self.submitButton.setGeometry(QRect(124, 302, 91, 31))
        self.submitButton.setFont(font3)

        self.showGroupBox = QGroupBox(self.centralwidget)
        self.showGroupBox.setObjectName(u"showGroupBox")
        self.showGroupBox.setGeometry(QRect(410, 20, 341, 291))
        self.showGroupBox.setFont(font1)
        self.showGroupBox.setAlignment(Qt.AlignCenter)
        self.showGroupBox.setFlat(False)

        self.showIpspaceLine = QLineEdit(self.showGroupBox)
        self.showIpspaceLine.setObjectName(u"showIpspaceLine")
        self.showIpspaceLine.setEnabled(False)
        self.showIpspaceLine.setGeometry(QRect(40, 50, 261, 21))
        self.showIpspaceLine.setText(u"")
        self.showIpspaceLine.setMaxLength(15)
        self.showIpspaceLine.setAlignment(Qt.AlignCenter)
        self.showIpspaceLine.setReadOnly(True)
        self.showIpspaceLine.setFont(font3)
        self.showIpspaceLine.setClearButtonEnabled(False)
        
        self.showIpspaceLabel = QLabel(self.showGroupBox)
        self.showIpspaceLabel.setObjectName(u"showIpspaceLabel")
        self.showIpspaceLabel.setGeometry(QRect(40, 30, 261, 20))
        self.showIpspaceLabel.setFont(font2)
        self.showIpspaceLabel.setAlignment(Qt.AlignCenter)

        self.showSubnetLine = QLineEdit(self.showGroupBox)
        self.showSubnetLine.setObjectName(u"showSubnetLine")
        self.showSubnetLine.setEnabled(False)
        self.showSubnetLine.setGeometry(QRect(70, 100, 61, 20))
        self.showSubnetLine.setMaxLength(3)
        self.showSubnetLine.setFont(font3)
        self.showSubnetLine.setAlignment(Qt.AlignCenter)
        self.showSubnetLine.setReadOnly(True)

        self.showSubnetLabel = QLabel(self.showGroupBox)
        self.showSubnetLabel.setObjectName(u"showSubnetLabel")
        self.showSubnetLabel.setGeometry(QRect(60, 80, 81, 20))
        self.showSubnetLabel.setFont(font2)
        self.showSubnetLabel.setAlignment(Qt.AlignCenter)

        self.showSleeptimeLine = QLineEdit(self.showGroupBox)
        self.showSleeptimeLine.setObjectName(u"showSleeptimeLine")
        self.showSleeptimeLine.setGeometry(QRect(210, 100, 60, 20))
        self.showSleeptimeLine.setEnabled(False)
        self.showSleeptimeLine.setFont(font3)
        self.showSleeptimeLine.setAlignment(Qt.AlignCenter)
        self.showSleeptimeLine.setMaxLength(7)
        self.showSleeptimeLine.setReadOnly(True)

        self.showSleeptimeLabel = QLabel(self.showGroupBox)
        self.showSleeptimeLabel.setObjectName(u"showSleeptimeLabel")
        self.showSleeptimeLabel.setGeometry(QRect(196, 80, 90, 20))
        self.showSleeptimeLabel.setFont(font2)
        self.showSleeptimeLabel.setAlignment(Qt.AlignCenter)

        self.showVulndiscBox = QCheckBox(self.showGroupBox)
        self.showVulndiscBox.setObjectName(u"showVulndiscBox")
        self.showVulndiscBox.setEnabled(False)
        self.showVulndiscBox.setGeometry(QRect(70, 260, 30, 20))
        self.showVulndiscBox.setLayoutDirection(Qt.RightToLeft)
        self.showVulndiscBox.setCheckable(True)

        self.showPortscanBox = QCheckBox(self.showGroupBox)
        self.showPortscanBox.setObjectName(u"showPortscanBox")
        self.showPortscanBox.setEnabled(False)
        self.showPortscanBox.setGeometry(QRect(242, 260, 30, 20))
        self.showPortscanBox.setLayoutDirection(Qt.RightToLeft)
        self.showPortscanBox.setIconSize(QSize(16, 16))
        self.showPortscanBox.setCheckable(True)
        self.showPortscanBox.setTristate(False)

        self.showVulndiscLabel = QLabel(self.showGroupBox)
        self.showVulndiscLabel.setObjectName(u"showVulndiscLabel")
        self.showVulndiscLabel.setGeometry(QRect(0, 240, 171, 21))
        self.showVulndiscLabel.setFont(font2)
        self.showVulndiscLabel.setAlignment(Qt.AlignCenter)

        self.showPortscanLabel = QLabel(self.showGroupBox)
        self.showPortscanLabel.setObjectName(u"showPortscanLabel")
        self.showPortscanLabel.setGeometry(QRect(170, 240, 171, 20))
        self.showPortscanLabel.setFont(font2)
        self.showPortscanLabel.setAlignment(Qt.AlignCenter)

        self.showPortscanGroupBox = QGroupBox(self.showGroupBox)
        self.showPortscanGroupBox.setObjectName(u"showPortscanGroupBox")
        self.showPortscanGroupBox.setGeometry(QRect(19, 139, 301, 71))
        self.showPortscanGroupBox.setFont(font2)
        self.showPortscanGroupBox.setAlignment(Qt.AlignCenter)

        self.showStartPortscanLine = QLineEdit(self.showPortscanGroupBox)
        self.showStartPortscanLine.setObjectName(u"showStartPortscanLine")
        self.showStartPortscanLine.setEnabled(False)
        self.showStartPortscanLine.setGeometry(QRect(60, 30, 61, 20))
        self.showStartPortscanLine.setFont(font2)
        self.showStartPortscanLine.setMaxLength(6)
        self.showStartPortscanLine.setReadOnly(True)

        self.showEndPortscanLine = QLineEdit(self.showPortscanGroupBox)
        self.showEndPortscanLine.setObjectName(u"showEndPortscanLine")
        self.showEndPortscanLine.setEnabled(False)
        self.showEndPortscanLine.setGeometry(QRect(212, 30, 71, 20))
        self.showEndPortscanLine.setFont(font2)
        self.showEndPortscanLine.setMaxLength(6)
        self.showEndPortscanLine.setReadOnly(True)

        self.showStartPortscanLabel = QLabel(self.showPortscanGroupBox)
        self.showStartPortscanLabel.setObjectName(u"showStartPortscanLabel")
        self.showStartPortscanLabel.setGeometry(QRect(10, 30, 51, 16))
        self.showStartPortscanLabel.setAlignment(Qt.AlignCenter)

        self.showEndPortscanLabel = QLabel(self.showPortscanGroupBox)
        self.showEndPortscanLabel.setObjectName(u"showEndPortscanLabel")
        self.showEndPortscanLabel.setGeometry(QRect(170, 30, 41, 16))
        self.showEndPortscanLabel.setAlignment(Qt.AlignCenter)

        self.dashboardButton = QPushButton(MainWindow)
        self.dashboardButton.setObjectName(u"dashboardButton")
        self.dashboardButton.setGeometry(QRect(444, 332, 100, 30))
        self.dashboardButton.setFont(font3)

        self.scanButton = QPushButton(MainWindow)
        self.scanButton.setObjectName(u"scanButton")
        self.scanButton.setGeometry(QRect(624, 332, 100, 30))
        self.scanButton.setFont(font3)

        self.scanLabel = QLabel(MainWindow)
        self.scanLabel.setObjectName(u"scanLabel")
        self.scanLabel.setGeometry(QRect(608, 358, 140, 30))
        self.scanLabel.setFont(font2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)


        QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Heimdall", None))

        self.setGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"New configuration", None))
        self.setIpspaceLabel.setText(QCoreApplication.translate("MainWindow", u"IP Space", None))
        self.setSubnetLine.setText("")
        self.setSubnetLabel.setText(QCoreApplication.translate("MainWindow", u"Subnet", None))
        self.setSleeptimeLabel.setText(QCoreApplication.translate("MainWindow", u"Sleep time (s)", None))
        self.setVulndiscBox.setText("")
        self.setPortscanBox.setText("")
        self.setVulndiscLabel.setText(QCoreApplication.translate("MainWindow", u"Vulnerability discovery", None))
        self.setPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Port scan", None))
        self.setPortscanGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Ports to scan", None))
        self.setStartPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.setEndPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"End", None))

        self.submitButton.setText(QCoreApplication.translate("MainWindow", u"Submit", None))

        self.showGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Current configuration", None))
        self.showIpspaceLabel.setText(QCoreApplication.translate("MainWindow", u"IP Space", None))
        self.showSubnetLine.setText("")
        self.showSubnetLabel.setText(QCoreApplication.translate("MainWindow", u"Subnet", None))
        self.showSleeptimeLabel.setText(QCoreApplication.translate("MainWindow", u"Sleep time (s)", None))
        self.showVulndiscBox.setText("")
        self.showPortscanBox.setText("")
        self.showVulndiscLabel.setText(QCoreApplication.translate("MainWindow", u"Vulnerability discovery", None))
        self.showPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Port scan", None))
        self.showPortscanGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Ports to scan", None))
        self.showStartPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.showEndPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"End", None))

        self.dashboardButton.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.scanButton.setText(QCoreApplication.translate("MainWindow", "Start scan", None))
        self.scanLabel.setText(QCoreApplication.translate("MainWindow", u"(Works only on Linux)", None))

    def updateCurrentConfig(self, config: dict):
        """Set the values into the 'current' box of the window

        Args:
            config (dict): dict with the data to set into the window
        """
        conf = config["CONFIG"]
        ip_space = str(conf["ip_space"])
        subnet = str(conf["subnet"])
        sleeptime = str(conf["sleeptime"])
        vuln_disc = bool(conf["vuln_discovery"])
        port_scan = bool(conf["port_scan"])
        ports = (str(conf["ports"]["start"]), str(conf["ports"]["end"]))

        self.showIpspaceLine.setText(ip_space)
        self.showSubnetLine.setText(subnet)
        self.showSleeptimeLine.setText(sleeptime)
        self.showVulndiscBox.setChecked(vuln_disc)
        self.showPortscanBox.setChecked(port_scan)
        self.showStartPortscanLine.setText(ports[0])
        self.showEndPortscanLine.setText(ports[1])

    def getConfigValues(self):
        """Get data from window and write into config file
        """
        conf = self.config["CONFIG"]

        # check ip space input
        ip_space = self.setIpspaceLine.text()
        ip_regex_pattern = compile("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if not ip_regex_pattern.match(ip_space):
            ip_space = conf["ip_space"]

        # check subnet input
        try:
            subnet_int = int(self.setSubnetLine.text())
            print(subnet_int)
            if subnet_int >= 0:
                subnet = str(subnet_int)
            else:
                error_message("Subnet cannot be negative!")
                subnet = conf["subnet"]
        except:
            subnet = conf["subnet"]
        

        # check sleep time input
        try:
            sleeptime_int = int(self.setSleeptimeLine.text())
            if sleeptime_int > 0:
                sleeptime = str(sleeptime_int)
            else:
                error_message("Sleep time cannot be negative or zero!")
                sleeptime = conf["sleeptime"]
        except:
            sleeptime = conf["sleeptime"]

        # get vuln discovery and port scan booleans
        vuln_disc = self.setVulndiscBox.isChecked()
        port_scan = self.setPortscanBox.isChecked()
        
        # check portscan values
        try:
            portscan_start = int(self.setStartPortscanLine.text())
        except ValueError:
            portscan_start = conf["ports"]["start"]
            
        try:
            portscan_end = int(self.setEndPortscanLine.text())
        except ValueError:
            portscan_end = conf["ports"]["end"]

        if (portscan_start > portscan_end) or (portscan_start<0) or (portscan_end<0):
            error_message(f"Invalid port values!\nStart: {portscan_start} End: {portscan_end}")
            return
        
        conf["ip_space"] = ip_space
        conf["subnet"] = subnet
        conf["sleeptime"] = sleeptime
        conf["vuln_discovery"] = vuln_disc
        conf["port_scan"] = port_scan
        conf["ports"]["start"] = portscan_start
        conf["ports"]["end"] = portscan_end

        self.config["CONFIG"] = conf

        update_config_file(CONFIG_PATH, self.config)
        
class WindowUpdateThread(QThread):
    def __init__(self, window: Ui_MainWindow):
        QThread.__init__(self)
        self.window = window
    
    def run(self):
        """Loop for value update thread
        """
        while True:
            current_config = get_config(CONFIG_PATH)
            self.window.updateCurrentConfig(current_config)
            sleep(0.5)

def get_config(path: str):
    """Get config data from yaml file

    Args:
        path (str): path to file in string format

    Returns:
        data: if file read successful, return data
    """
    with open(path, "r") as config:
        try:
            data = yaml.safe_load(config)
            return data
        except yaml.YAMLError as e:
            print(e)

def update_config_file(path: str, newConf: dict):
    """Update config data with provided values

    Args:
        path (str): path to file in string format
        newConf (dict): dictionary with data to write into yaml
    """
    with open(path, "w") as file:
        yaml.dump(newConf, file)

def call_process(list_args: list):
    """Calls subprocess.call on with the args given.
    Error handling included

    Args:
        list_args (list): list of command line arguments to execute
    """
    try:
        process_call(list_args)
    except:
        error_message(f"Scan execute failed!\nCheck if your system can open .sh files")

def error_message(message: str):
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec_()
