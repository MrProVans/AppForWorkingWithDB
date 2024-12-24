import psycopg2
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FreelanceDB GUI")
        self.setGeometry(200, 200, 800, 600)

        # Соединение с БД
        self.connection = psycopg2.connect(
            dbname="FreelanceDB", user="freelance_user", password="password123", host="localhost", port="5432"
        )
        self.cursor = self.connection.cursor()

        # Создание вкладок
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.clients_tab = QWidget()
        self.orders_tab = QWidget()
        self.payments_tab = QWidget()
        self.projects_tab = QWidget()
        self.services_tab = QWidget()

        self.tabs.addTab(self.clients_tab, "Clients")
        self.tabs.addTab(self.orders_tab, "Orders")
        self.tabs.addTab(self.payments_tab, "Payments")
        self.tabs.addTab(self.projects_tab, "Projects")
        self.tabs.addTab(self.services_tab, "Services")

        # Заполнение вкладок
        self.init_clients_tab()
        self.init_orders_tab()
        self.init_payments_tab()
        self.init_projects_tab()
        self.init_services_tab()

    # Функции для работы с базой данных
    def call_add_service(self, service_name, service_description, service_price):
        try:
            self.cursor.callproc('add_service_proc', [service_name, service_description, service_price])
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding service: {str(e)}")

    def call_update_service(self, service_id, service_name, service_description, service_price):
        try:
            self.cursor.callproc('update_service_proc', [service_id, service_name, service_description, service_price])
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating service: {str(e)}")

    def call_delete_service(self, service_id):
        try:
            self.cursor.callproc('delete_service_proc', [service_id])
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting service: {str(e)}")

    # Функции для каждой вкладки
    def init_clients_tab(self):
        layout = QVBoxLayout()

        # Таблица для отображения клиентов
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(5)
        self.clients_table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Company"])
        self.load_clients_data()

        # Кнопки
        self.add_client_button = QPushButton("Add Client")
        self.add_client_button.clicked.connect(self.add_client)

        layout.addWidget(self.clients_table)
        layout.addWidget(self.add_client_button)

        self.clients_tab.setLayout(layout)

    def init_orders_tab(self):
        layout = QVBoxLayout()

        # Таблица для отображения заказов
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["Order ID", "Client ID", "Project ID", "Service ID", "Order Date"])
        self.load_orders_data()

        # Кнопки
        self.add_order_button = QPushButton("Add Order")
        self.add_order_button.clicked.connect(self.add_order)

        layout.addWidget(self.orders_table)
        layout.addWidget(self.add_order_button)

        self.orders_tab.setLayout(layout)

    def init_payments_tab(self):
        layout = QVBoxLayout()

        # Таблица для отображения платежей
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(5)
        self.payments_table.setHorizontalHeaderLabels(
            ["Payment ID", "Order ID", "Amount", "Payment Date", "Payment Method"])
        self.load_payments_data()

        # Кнопки
        self.add_payment_button = QPushButton("Add Payment")
        self.add_payment_button.clicked.connect(self.add_payment)

        layout.addWidget(self.payments_table)
        layout.addWidget(self.add_payment_button)

        self.payments_tab.setLayout(layout)

    def init_projects_tab(self):
        layout = QVBoxLayout()

        # Таблица для отображения проектов
        self.projects_table = QTableWidget()
        self.projects_table.setColumnCount(5)
        self.projects_table.setHorizontalHeaderLabels(
            ["Project ID", "Project Name", "Description", "Status", "Start Date"])
        self.load_projects_data()

        # Кнопки
        self.add_project_button = QPushButton("Add Project")
        self.add_project_button.clicked.connect(self.add_project)

        layout.addWidget(self.projects_table)
        layout.addWidget(self.add_project_button)

        self.projects_tab.setLayout(layout)

    def init_services_tab(self):
        layout = QVBoxLayout()

        # Таблица для отображения сервисов
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(4)
        self.services_table.setHorizontalHeaderLabels(["Service ID", "Service Name", "Description", "Price"])
        self.load_services_data()

        # Кнопки
        self.add_service_button = QPushButton("Add Service")
        self.add_service_button.clicked.connect(self.add_service)

        layout.addWidget(self.services_table)
        layout.addWidget(self.add_service_button)

        self.services_tab.setLayout(layout)

    # Загрузка данных в таблицы
    def load_clients_data(self):
        self.cursor.execute("SELECT clientid, name, email, phone, companyname FROM clients")
        rows = self.cursor.fetchall()
        self.clients_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.clients_table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def load_orders_data(self):
        self.cursor.execute("SELECT orderid, clientid, projectid, serviceid, orderdate FROM orders")
        rows = self.cursor.fetchall()
        self.orders_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.orders_table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def load_payments_data(self):
        self.cursor.execute("SELECT paymentid, orderid, amount, paymentdate, paymentmethod FROM payments")
        rows = self.cursor.fetchall()
        self.payments_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.payments_table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def load_projects_data(self):
        self.cursor.execute("SELECT projectid, projectname, description, status, startdate FROM projects")
        rows = self.cursor.fetchall()
        self.projects_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.projects_table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def load_services_data(self):
        self.cursor.execute("SELECT serviceid, servicename, description, price FROM services")
        rows = self.cursor.fetchall()
        self.services_table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.services_table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    # Обработчики кнопок
    def add_client(self):
        # Вставляем данные клиента через форму
        client_name = "John Doe"  # Пример данных (их можно получить из текстовых полей формы)
        client_email = "john.doe@example.com"
        client_phone = "123-456-7890"
        client_company = "Company ABC"

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('add_client_proc', [client_name, client_email, client_phone, client_company])
            self.connection.commit()
            self.load_clients_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding client: {str(e)}")

    def add_order(self):
        # Пример данных (их можно получить из формы)
        client_id = 1
        project_id = 1
        service_id = 1
        order_date = '2024-12-24'

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('add_order_proc', [client_id, project_id, service_id, order_date])
            self.connection.commit()
            self.load_orders_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding order: {str(e)}")

    def add_payment(self):
        # Пример данных (их можно получить из формы)
        order_id = 1
        amount = 100.00
        payment_date = '2024-12-24'
        payment_method = "Credit Card"

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('add_payment_proc', [order_id, amount, payment_date, payment_method])
            self.connection.commit()
            self.load_payments_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding payment: {str(e)}")

    def add_project(self):
        # Пример данных (их можно получить из формы)
        project_name = "New Project"
        description = "Description of the project"
        status = "in progress"
        start_date = '2024-12-24'
        end_date = '2025-12-24'

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('add_project_proc', [project_name, description, status, start_date, end_date])
            self.connection.commit()
            self.load_projects_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding project: {str(e)}")

    def add_service(self):
        # Пример данных (их можно получить из формы)
        service_name = "Web Design"
        description = "Designing and developing websites"
        price = 500.00

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('add_service_proc', [service_name, description, price])
            self.connection.commit()
            self.load_services_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding service: {str(e)}")

    def update_client(self, client_id):
        # Пример данных (их можно получить из формы)
        client_name = "John Smith"
        client_email = "john.smith@example.com"
        client_phone = "987-654-3210"
        client_company = "Company XYZ"

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('update_client_proc',
                                 [client_id, client_name, client_email, client_phone, client_company])
            self.connection.commit()
            self.load_clients_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating client: {str(e)}")

    def update_order(self, order_id):
        # Пример данных (их можно получить из формы)
        client_id = 1
        project_id = 1
        service_id = 1
        order_date = '2024-12-24'

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('update_order_proc', [order_id, client_id, project_id, service_id, order_date])
            self.connection.commit()
            self.load_orders_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating order: {str(e)}")

    def update_payment(self, payment_id):
        # Пример данных (их можно получить из формы)
        amount = 150.00
        payment_date = '2024-12-25'
        payment_method = "Bank Transfer"

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('update_payment_proc', [payment_id, amount, payment_date, payment_method])
            self.connection.commit()
            self.load_payments_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating payment: {str(e)}")

    def update_project(self, project_id):
        # Пример данных (их можно получить из формы)
        project_name = "Updated Project"
        description = "Updated description"
        status = "completed"
        start_date = '2024-12-24'
        end_date = '2025-12-25'

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('update_project_proc',
                                 [project_id, project_name, description, status, start_date, end_date])
            self.connection.commit()
            self.load_projects_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating project: {str(e)}")

    def update_service(self, service_id):
        # Пример данных (их можно получить из формы)
        service_name = "Web Development"
        description = "Developing and deploying websites"
        price = 800.00

        # Вызов хранимой процедуры
        try:
            self.cursor.callproc('update_service_proc', [service_id, service_name, description, price])
            self.connection.commit()
            self.load_services_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating service: {str(e)}")

    def delete_client(self, client_id):
        try:
            self.cursor.callproc('delete_client_proc', [client_id])
            self.connection.commit()
            self.load_clients_data()  # Перезагружаем данные в таблице
        except Exception as e:
            self.connection.rollback()
            print(f"Error deleting client: {str(e)}")

