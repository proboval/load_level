from PyQt5.QtWidgets import QApplication
import sys
from form import Load_Level_Form


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = Load_Level_Form.Load_Level_Form()

    sys.exit(app.exec())
