import yaml
from PyQt5.QtWidgets import  QWidget, QGroupBox, QLineEdit,  QLabel, QCheckBox, QPushButton, QMainWindow, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication, Qt, QSize, QThread
from time import sleep

CONFIG_PATH = "../config/config.yml"

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
        self.setGroupBox.setGeometry(QRect(20, 20, 341, 351))

        self.setGroupBox.setFont(font1)
        self.setGroupBox.setAlignment(Qt.AlignCenter)

        self.setIpspaceLine = QLineEdit(self.setGroupBox)
        self.setIpspaceLine.setObjectName(u"setIpspaceLine")
        self.setIpspaceLine.setGeometry(QRect(40, 50, 261, 21))
        self.setIpspaceLine.setText(u"")
        self.setIpspaceLine.setMaxLength(15)
        self.setIpspaceLine.setFont(font3)
        self.setIpspaceLine.setAlignment(Qt.AlignCenter)

        self.setIpspaceLabel = QLabel(self.setGroupBox)
        self.setIpspaceLabel.setObjectName(u"setIpspaceLabel")
        self.setIpspaceLabel.setGeometry(QRect(40, 30, 261, 20))
        self.setIpspaceLabel.setFont(font2)
        self.setIpspaceLabel.setAlignment(Qt.AlignCenter)

        self.setSubnetLine = QLineEdit(self.setGroupBox)
        self.setSubnetLine.setObjectName(u"setSubnetLine")
        self.setSubnetLine.setGeometry(QRect(140, 100, 61, 20))
        self.setSubnetLine.setMaxLength(3)
        self.setSubnetLine.setFont(font3)
        self.setSubnetLine.setAlignment(Qt.AlignCenter)
        
        self.setSubnetLabel = QLabel(self.setGroupBox)
        self.setSubnetLabel.setObjectName(u"setSubnetLabel")
        self.setSubnetLabel.setGeometry(QRect(130, 80, 81, 20))
        self.setSubnetLabel.setFont(font2)
        self.setSubnetLabel.setAlignment(Qt.AlignCenter)

        self.setVulndiscBox = QCheckBox(self.setGroupBox)
        self.setVulndiscBox.setObjectName(u"setVulndiscBox")
        self.setVulndiscBox.setGeometry(QRect(80, 250, 20, 41))
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
        self.showSubnetLine.setGeometry(QRect(140, 100, 61, 20))
        self.showSubnetLine.setMaxLength(3)
        self.showSubnetLine.setFont(font3)
        self.showSubnetLine.setAlignment(Qt.AlignCenter)
        self.showSubnetLine.setReadOnly(True)

        self.showSubnetLabel = QLabel(self.showGroupBox)
        self.showSubnetLabel.setObjectName(u"showSubnetLabel")
        self.showSubnetLabel.setGeometry(QRect(130, 80, 81, 20))
        self.showSubnetLabel.setFont(font2)
        self.showSubnetLabel.setAlignment(Qt.AlignCenter)

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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)


        QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Heimdall", None))

        self.setGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"New configuration", None))
        self.setIpspaceLabel.setText(QCoreApplication.translate("MainWindow", u"IP Space", None))
        self.setSubnetLine.setText("")
        self.setSubnetLabel.setText(QCoreApplication.translate("MainWindow", u"Subnet", None))
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
        self.showVulndiscBox.setText("")
        self.showPortscanBox.setText("")
        self.showVulndiscLabel.setText(QCoreApplication.translate("MainWindow", u"Vulnerability discovery", None))
        self.showPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Port scan", None))
        self.showPortscanGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Ports to scan", None))
        self.showStartPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.showEndPortscanLabel.setText(QCoreApplication.translate("MainWindow", u"End", None))
    
    def updateCurrentConfig(self, config: dict):
        """Set the values into the 'current' box of the window

        Args:
            config (dict): dict with the data to set into the window
        """
        conf = config["CONFIG"]
        ip_space = str(conf["ip_space"])
        subnet = str(conf["subnet"])
        vuln_disc = bool(conf["vuln_discovery"])
        port_scan = bool(conf["port_scan"])
        ports = (str(conf["ports"]["start"]), str(conf["ports"]["end"]))

        self.showIpspaceLine.setText(ip_space)
        self.showSubnetLine.setText(subnet)
        self.showVulndiscBox.setChecked(vuln_disc)
        self.showPortscanBox.setChecked(port_scan)
        self.showStartPortscanLine.setText(ports[0])
        self.showEndPortscanLine.setText(ports[1])

    def getConfigValues(self):
        """Get data from window and write into config file
        """
        conf = self.config["CONFIG"]

        ip_space = self.setIpspaceLine.text()
        if (len(ip_space) == 0) or (ip_space.count(".") != 3):
            ip_space = conf["ip_space"]

        try:
            subnet = str(int(self.setSubnetLine.text()))
        except:
            subnet = conf["subnet"]
        if len(subnet) == 0:
            subnet = conf["subnet"]

        vuln_disc = self.setVulndiscBox.isChecked()
        port_scan = self.setPortscanBox.isChecked()
        try:
            portscan_start = int(self.setStartPortscanLine.text())
        except ValueError:
            portscan_start = conf["ports"]["start"]
            
        try:
            portscan_end = int(self.setEndPortscanLine.text())
        except ValueError:
            portscan_end = conf["ports"]["end"]

        if (portscan_start > portscan_end) or (portscan_start<0) or (portscan_end<0):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Invalid port values!\nStart: {portscan_start} End: {portscan_end}")
            msg.exec_()
            return
        
        conf["ip_space"] = ip_space
        conf["subnet"] = subnet
        conf["vuln_discovery"] = vuln_disc
        conf["port_scan"] = port_scan
        conf["ports"]["start"] = portscan_start
        conf["ports"]["end"] = portscan_end

        self.config["CONFIG"] = conf

        update_config_file(CONFIG_PATH, self.config)
        
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
            sleep(1)