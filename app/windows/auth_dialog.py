from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from app.ui.auth_dialog import Ui_auth_dialog
from app.windows.dto.user import User


class AuthDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = Ui_auth_dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowSystemMenuHint)

        self.ui.submit.clicked.connect(self._auth)

    def _auth(self):
        if not (last_name := self.ui.last_name_line.text()):
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText("Введите фамилию")
            msg.setWindowTitle("Ошибка")
            msg.exec()
            return
        self.parent().user = User(last_name=last_name)
        self.close()
