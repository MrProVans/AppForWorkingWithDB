import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, \
    QTableWidget, QTableWidgetItem, QHBoxLayout

# Конфигурация подключения к базе данных
DB_PARAMS = {
            'dbname': 'FreelanceDB',
            'user': 'freelance_user',
            'password': 'password123',
            'host': 'localhost',
            'port': 5432
        }


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(**DB_PARAMS)
        self.cursor = self.connection.cursor()

    def execute_procedure(self, proc_name, *args):
        query = f"CALL {proc_name}({', '.join(['%s'] * len(args))})"
        self.cursor.execute(query, args)
        self.connection.commit()

    def fetch_table(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def search_by_field(self, table_name, field_name, search_value):
        self.cursor.execute(f"SELECT * FROM search_by_field(%s, %s, %s)", (table_name, field_name, search_value))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Database Management')
        self.setGeometry(100, 100, 800, 600)

        self.db = Database()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Создание кнопок для каждой из функций ТЗ
        self.create_buttons(layout)

        # Таблица для отображения содержимого таблиц
        self.tableWidget = QTableWidget(self)
        layout.addWidget(self.tableWidget)

        # Поля для ввода данных
        self.inputField = QLineEdit(self)
        self.inputField.setPlaceholderText('Enter text for search or other operations')
        layout.addWidget(self.inputField)

        # Основной контейнер
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_buttons(self, layout):
        # Кнопки для создания базы данных и удаления
        self.create_db_button = QPushButton('Create Database', self)
        self.create_db_button.clicked.connect(self.create_database)
        layout.addWidget(self.create_db_button)

        self.delete_db_button = QPushButton('Delete Database', self)
        self.delete_db_button.clicked.connect(self.delete_database)
        layout.addWidget(self.delete_db_button)

        # Кнопки для работы с таблицами
        self.load_table_button = QPushButton('Load Table Data', self)
        self.load_table_button.clicked.connect(self.load_table_data)
        layout.addWidget(self.load_table_button)

        self.clear_table_button = QPushButton('Clear Table', self)
        self.clear_table_button.clicked.connect(self.clear_table)
        layout.addWidget(self.clear_table_button)

        self.add_data_button = QPushButton('Add Data', self)
        self.add_data_button.clicked.connect(self.add_data)
        layout.addWidget(self.add_data_button)

        self.update_data_button = QPushButton('Update Data', self)
        self.update_data_button.clicked.connect(self.update_data)
        layout.addWidget(self.update_data_button)

        self.delete_data_button = QPushButton('Delete Data', self)
        self.delete_data_button.clicked.connect(self.delete_data)
        layout.addWidget(self.delete_data_button)

        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_data)
        layout.addWidget(self.search_button)

    def create_database(self):
        self.db.execute_procedure('create_database')
        print("Database created successfully.")

    def delete_database(self):
        try:
            self.db.execute_procedure('clear_all_tables')
            print("Database cleared successfully.")
        except Exception as e:
            print(f"Error clearing database: {e}")

    def load_table_data(self):
        table_name = 'clients'  # Здесь можно выбрать нужную таблицу
        data = self.db.fetch_table(table_name)

        if not data:  # Проверяем, есть ли данные в таблице
            print(f"Table '{table_name}' is empty.")
            self.tableWidget.clear()  # Очищаем таблицу в GUI
            self.tableWidget.setRowCount(0)  # Устанавливаем нулевое количество строк
            self.tableWidget.setColumnCount(0)  # Устанавливаем нулевое количество столбцов
            return

        self.display_table_data(data)

    def clear_table(self):
        table_name = 'clients'  # Здесь можно выбрать нужную таблицу
        self.db.execute_procedure('clear_table', table_name)
        print(f"Table {table_name} cleared.")

    def add_data(self):
        data = self.inputField.text().split(',')

        if len(data) < 3:
            print("Invalid input. Please enter data in the format: Name,Email,Phone[,Company]")
            return

        # Добавляем значение для компании, если оно отсутствует
        while len(data) < 4:
            data.append("Unknown")

        try:
            self.db.execute_procedure('add_client_proc', *data)
            print("Data added successfully.")
        except Exception as e:
            print(f"Error adding data: {e}")

    def update_data(self):
        # Тут нужно реализовать логику для обновления данных
        pass

    def delete_data(self):
        # Логика для удаления данных
        pass

    def search_data(self):
        table_name = 'clients'  # Здесь можно выбрать нужную таблицу
        field_name = 'name'  # Поле для поиска
        search_value = self.inputField.text()
        results = self.db.search_by_field(table_name, field_name, search_value)
        self.display_table_data(results)

    def display_table_data(self, data):
        if not data:
            return
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.db.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
