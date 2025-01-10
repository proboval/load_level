import sqlite3


class DatabaseManager:
    def __init__(self, db_name='system_monitor.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                cpu REAL,
                total_ram REAL,
                used_ram REAL,
                total_rom REAL,
                used_rom REAL
            )
        ''')
        self.conn.commit()

    def insert_data(self, cpu: float, total_ram: float, used_ram: float, total_rom: float, used_rom: float):
        self.cursor.execute('''
            INSERT INTO system_stats (cpu, total_ram, used_ram, total_rom, used_rom)
            VALUES (?, ?, ?, ?, ?)
        ''', (cpu, total_ram, used_ram, total_rom, used_rom))
        self.conn.commit()

    def close(self):
        self.conn.close()
