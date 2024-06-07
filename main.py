import sys
import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QLineEdit
from ui_auth import Ui_Form as Auth_Ui_Form
from ui_main import Ui_MainWindow


class Auth(QWidget, Auth_Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()

        self.auth_is_complete = 0

    def init_ui(self):
        self.setLayout(self.verticalLayout)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.ok_btn.clicked.connect(self.buttons)

    def buttons(self):
        if self.sender() == self.ok_btn:
            with open('db.json') as db:
                data = json.load(db)
                if self.user.text() in data.keys():
                    if self.password.text() == data[self.user.text()]:
                        self.auth_is_complete = 1
                        self.main = MainWindow(self.user.text())
                        self.main.show()
                        self.close()
                    else:
                        self.user.clear()
                        self.password.clear()
                        QMessageBox.warning(self, "Сообщение об ошибке", "Неверный логин или пароль.")
                else:
                    self.user.clear()
                    self.password.clear()
                    QMessageBox.warning(self, "Сообщение об ошибке", "Неверный логин или пароль.")

    # действие при закрытии
    def closeEvent(self, event):
        if self.auth_is_complete == 1:
            event.accept()
        else:
            answer = QMessageBox.question(self,
                                          'Выход',
                                          'Хотите прервать операцию?'
                                          )
            if answer == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, login: str):
        super().__init__()
        self.setupUi(self)
        self.init_ui(login)

    def init_ui(self, login):
        self.blueprints_tab.setLayout(self.verticalLayout)

        os.chdir('blueprints')
        self.file_list.addItems(os.listdir())

        self.open_btn.clicked.connect(self.buttons)

    def buttons(selfd):
        if self.sender() == self.open_btn:
            self.setpix(self.file_list.currentItem().text())

    # ставит изображение по названию
    def setpix(self, filename):
        self.filename = filename
        self.pixmap = QPixmap(filename)
        self.image.setPixmap(self.pixmap.scaled(self.pixmap.size(), Qt.AspectRatioMode.IgnoreAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Auth()
    ex.show()
    sys.exit(app.exec())
