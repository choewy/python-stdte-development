from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetricsF, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QLabel, QTextEdit, QVBoxLayout


class Manual(QDialog):
    def __init__(self, central):
        QDialog.__init__(self, central)
        self.central = central

        self.setObjectName("ManualDialog")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedWidth(600)
        self.setFixedHeight(800)

        self.manualSource = None
        self.editFlag = self.central.clientAuth in ["관리자", "개발자"]

        self.buttonEdit = QPushButton()
        self.buttonEdit.mode = "edit"
        self.buttonEdit.setObjectName("ManualButton-edit")
        self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-edit.png").scaledToHeight(30)))
        self.buttonEdit.setFocusPolicy(Qt.NoFocus)

        if not self.editFlag:
            self.buttonEdit.setVisible(False)

        self.buttonEdit.setCursor(Qt.PointingHandCursor)
        self.buttonEdit.clicked.connect(self.handleButtonEditClick)

        self.buttonClose = QPushButton()
        self.buttonClose.setObjectName("ManualButton-close")
        self.buttonClose.setIcon(QIcon(QPixmap("images/close.png").scaledToHeight(12)))
        self.buttonClose.setCursor(Qt.PointingHandCursor)
        self.buttonClose.clicked.connect(self.close)

        layoutButtons = QHBoxLayout()
        layoutButtons.addWidget(QLabel(" "), 10)
        layoutButtons.addWidget(self.buttonEdit)
        layoutButtons.addWidget(self.buttonClose)
        layoutButtons.setContentsMargins(0, 0, 0, 0)

        self.inputManual = QTextEdit()
        self.inputManual.setObjectName("ManualText-contents")

        font = self.inputManual.font()
        fontMetrics = QFontMetricsF(font)
        spaceWidth = fontMetrics.width(' ')

        self.inputManual.setTabStopDistance(spaceWidth * 4)
        self.inputManual.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addLayout(layoutButtons, stretch=0)
        layout.addWidget(self.inputManual, stretch=10)

        self.setLayout(layout)
        self.setManual()

    def setManual(self):
        self.manualSource = self.central.realtimeDB.getManualSource()
        self.inputManual.setPlainText(self.manualSource.replace("\t", " "*4))

    def handleButtonEditClick(self):
        if self.buttonEdit.mode == "edit":
            self.buttonEdit.mode = "save"
            self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-save.png").scaledToHeight(30)))
            self.inputManual.setReadOnly(False)

        else:
            oldManualSource = self.manualSource
            newManualSource = self.inputManual.toPlainText()

            if oldManualSource != newManualSource:
                self.central.realtimeDB.setManualSource(newManualSource)
                self.setManual()

            self.buttonEdit.mode = "edit"
            self.buttonEdit.setIcon(QIcon(QPixmap("images/survey-edit.png").scaledToHeight(30)))
            self.inputManual.setReadOnly(True)
