import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QSettings

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.getSettingValues()

        height = self.setting_window.value('window_height')
        width = self.setting_variable.value("window_width")
        print(height, width)

        self.resize(width, height)
        
        self.textvalue = self.setting_variable.value("text box")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit()
        self.textbox.setText(self.textvalue)
        layout.addWidget(self.textbox)

    def getSettingValues(self):
        self.setting_window = QSettings('My app', 'Window Size')
        self.setting_variable = QSettings('My app', "Variable")

    def closeEvent(self, event):
        self.setting_window.setValue('window_height', self.rect().height())
        self.setting_variable.setValue('window_width', self.rect().width())

        self.setting_variable.setValue('text box', self.textbox.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''Qwidget {
        font-size: 60 px
        }
        QLineEdit { 
        height: 200px
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window')