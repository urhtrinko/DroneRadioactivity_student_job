# GUI
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#Import the automatically generated file
from r2d2_sound_control import Ui_Dialog

# ROS
import rospy
from std_msgs.msg import String


class Test(QDialog):
    def __init__(self,parent=None):
        # GUI
        super(Test, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # ROS pub settings
        self.r2d2_sound_controller_String = String()
        self.pub_r2d2_sound_controller_speak = rospy.Publisher('/ros2d2_node/speak',String,queue_size=10)

    def speak_content(self):
        self.input = string(lineEdit_speak)
        self.lineEdit_speak.setText(self.text())
        

    def clicked_speak(self):
        """
        The slot name specified in Qt Designer.
        Write the process you want to execute with the "Say Out" button.
        """
        self.r2d2_sound_controller_String.data = text()
        self.pub_r2d2_sound_controller_speak.publish(self.r2d2_sound_controller_String)
        self.r2d2_sound_controller_String.data = ''

if __name__ == '__main__':
    rospy.init_node('r2d2_sound_talker')
    app = QApplication(sys.argv)
    window = Test()
    window.show()
    sys.exit(app.exec_())