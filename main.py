from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
import psutil
from form import Ui_loadlevel
import sys


class load_level_form(QWidget, Ui_loadlevel):
    cpu: str
    total_ram: str
    used_ram: str
    percent_ram: str
    total_rom: str
    used_rom: str
    percent_rom: str

    def __init__(self):
        super(load_level_form, self).__init__()
        self.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)

        self.timer.start(1000)

        self.update_values()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Уровень загруженности системы")
        self.show()

    def update_values(self):
        self.cpu = str(psutil.cpu_percent(interval=1)) + '%'
        self.CPU_value.setText(self.cpu)

        memory_info = psutil.virtual_memory()
        self.total_ram = str(memory_info.total / 1024**3)
        self.total_ram = self.total_ram.split('.')[0] + '.' + self.total_ram.split('.')[1][:1] + 'GB'
        self.used_ram = str(memory_info.used / 1024**3)
        self.used_ram = self.used_ram.split('.')[0] + '.' + self.used_ram.split('.')[1][:1] + 'GB'
        self.percent_ram = str(memory_info.percent)
        self.RAM_value.setText(f'{self.total_ram} / {self.used_ram} ({self.percent_ram}%)')

        memory_info = psutil.disk_usage('/')
        self.total_rom = str(memory_info.total / 1024**3)
        self.total_rom = self.total_rom.split('.')[0] + '.' + self.total_rom.split('.')[1][:1] + 'GB'
        self.used_rom = str(memory_info.used / 1024**3)
        self.used_rom = self.used_rom.split('.')[0] + '.' + self.used_rom.split('.')[1][:1] + 'GB'
        self.percent_rom = str(memory_info.percent)
        self.ROM_value.setText(f'{self.total_rom} / {self.used_rom} ({self.percent_rom}%)')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = load_level_form()

    sys.exit(app.exec())
