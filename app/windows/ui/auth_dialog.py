# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'auth_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class Ui_auth_dialog(object):
    def setupUi(self, auth_dialog):
        if not auth_dialog.objectName():
            auth_dialog.setObjectName(u"auth_dialog")
        auth_dialog.resize(400, 294)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(auth_dialog.sizePolicy().hasHeightForWidth())
        auth_dialog.setSizePolicy(sizePolicy)
        auth_dialog.setMinimumSize(QSize(400, 294))
        auth_dialog.setMaximumSize(QSize(400, 294))
        self.gridLayout = QGridLayout(auth_dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.last_name_line = QLineEdit(auth_dialog)
        self.last_name_line.setObjectName(u"last_name_line")

        self.gridLayout.addWidget(self.last_name_line, 0, 1, 1, 1)

        self.label = QLabel(auth_dialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.submit = QPushButton(auth_dialog)
        self.submit.setObjectName(u"submit")

        self.gridLayout.addWidget(self.submit, 1, 0, 1, 2)


        self.retranslateUi(auth_dialog)

        QMetaObject.connectSlotsByName(auth_dialog)
    # setupUi

    def retranslateUi(self, auth_dialog):
        auth_dialog.setWindowTitle(QCoreApplication.translate("auth_dialog", u"\u0412\u043e\u0439\u0442\u0438 \u043a\u0430\u043a", None))
        self.label.setText(QCoreApplication.translate("auth_dialog", u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f", None))
        self.submit.setText(QCoreApplication.translate("auth_dialog", u"\u0412\u043e\u0439\u0442\u0438", None))
    # retranslateUi

