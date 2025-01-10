from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, QTime
import psutil
from form.form import Ui_loadlevel
from database import DatabaseManager


class Load_Level_Form(QWidget, Ui_loadlevel):
    db: DatabaseManager
    cpu: str
    total_ram: str
    used_ram: str
    percent_ram: str
    total_rom: str
    used_rom: str
    percent_rom: str
    flag: bool
    elapsed_time: int
    timer: QTimer

    def __init__(self):
        super(Load_Level_Form, self).__init__()
        self.setupUi(self)

        self.db = DatabaseManager()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_values)

        self.flag = False

        self.write_to_db.clicked.connect(lambda: self.write_load_manage())

        self.timer.start(1000)

        self.update_values()

        self.initUI()

    def write_load_manage(self):
        self.flag = not self.flag
        if self.flag:
            self.write_to_db.setText('Остановать')
            self.elapsed_time = 0
            self.timer_label.setText(self.format_time(self.elapsed_time))
        else:
            self.write_to_db.setText('Начать запись')
            self.timer_label.setText('')

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

        if self.flag:
            self.elapsed_time += 1
            self.timer_label.setText(self.format_time(self.elapsed_time))
            self.db.insert_data(float(self.cpu[:-1]), float(self.total_ram[:-2]), float(self.used_ram[:-2]),
                                float(self.total_rom[:-2]), float(self.used_rom[:-2]))

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def closeEvent(self, event):
        self.db.close()
        event.accept()
