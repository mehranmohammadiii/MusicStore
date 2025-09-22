import pyodbc
# from database.Db_Connection import DatabaseConnection
# from MyPackage import pyodbc

class InvoiceLineDAL:
    def __init__(self,db_manager):
        self.db_conn_manager=db_manager

    def create_invoiceLine(self,Artistcode,number,trackkode):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            sql_command = "exec Usp_CreateInvoiceline ?, ?"
            params = (trackkode,number)
            cursor.execute(sql_command,params)
            conn.commit()
            return True, "سفارش با موفقیت ثبت شد."
        
        except pyodbc.Error as db_err:
            error_message = str(db_err)
            print(f"خطای دیتابیس : {error_message}")
            if conn: # اگر اتصال برقرار بود
                conn.rollback()
            return False,error_message
        
        except Exception as e:
            print(f"خطا در Invoicline: {e}")
            if conn:
                conn.rollback()
            return False, f"یک خطای پیش‌بینی نشده رخ داد: {e}" 

        finally :
            if cursor:
                cursor.close()