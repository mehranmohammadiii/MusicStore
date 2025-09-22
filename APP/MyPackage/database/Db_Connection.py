import pyodbc
# from MyPackage import pyodbc
import configparser
import os

class DatabaseConnection:
    _instance = None  
    def __new__(cls): 
        if cls._instance is None: 
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None 
        return cls._instance 
    
    def connect(self): 
        if self.connection is None or self.connection.closed: 
            try:
                # خواندن اطلاعات از فایل config.ini
                config = configparser.ConfigParser()
                # آدرس فایل کانفیگ را به صورت دینامیک پیدا می‌کنیم
                config_path = os.path.join(os.path.abspath("."), 'config.ini')
                config.read(config_path)

                db_config = config['Database']
                server = db_config['Server']
                database = db_config['Database']
                driver = db_config['Driver']

                # ساختن رشته اتصال به صورت دینامیک
                conn_str = (
                    f"DRIVER={{{driver}}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                )
                self.connection = pyodbc.connect(conn_str)

                # self.connection = pyodbc.connect(
                #         "DRIVER={ODBC Driver 17 for SQL Server};"
                #         "SERVER=DESKTOP-M9UCNTP;"      # یا اسم سرور خودت
                #         "DATABASE=Chinook;"       # اسم دیتابیس
                #         "Trusted_Connection=yes;"  # اتصال با ویندوز
                #                 ) 
                

                print("اتصال به دیتابیس با موفقیت برقرار شد.")
            except pyodbc.Error as ex: 
                print("اتصال به دیتابیس ناموفق بود.")
                self.connection = None
        return self.connection 
    
    def disconnect(self): 
        if self.connection and not self.connection.closed:
            self.connection.close()
            print("اتصال به دیتابیس بسته شد.")
# -------------------------------------------------------------
# import pyodbc

# def ConnectSQL() :
#     try :
#         with pyodbc.connect(
        # "DRIVER={ODBC Driver 17 for SQL Server};"
        # "SERVER=DESKTOP-M9UCNTP;"      # یا اسم سرور خودت
        # "DATABASE=Chinoook;"       # اسم دیتابیس
        # "Trusted_Connection=yes;"  # اتصال با ویندوز
#             ) as db :
#             return db
#     except pyodbc.Error as eror:
#         return 0
