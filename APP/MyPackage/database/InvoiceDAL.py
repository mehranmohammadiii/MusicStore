import pyodbc
# from database.Db_Connection import DatabaseConnection
# from MyPackage import pyodbc

class InvoiceDAL:
    def __init__(self,db_manager):
        self.db_conn_manager=db_manager

    def fetch_Customer_invoice(self,Customercode):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            str1="exec Usp_GetCustomerInvoices "
            str1+=Customercode
            cursor.execute(str1)
            rows = cursor.fetchall()
            return rows
        
        except pyodbc.Error as db_err:
            print(f"خطای دیتابیس در Invoice رخ داد: {db_err}")
            return [] 
        
        except Exception as e:
            print(f"خطا در Invoice: {e}")
            return [] 

        finally :
            if cursor:
                cursor.close()

    def create_invoice(self,Customercode,BillingAddress,BillingCity,BillingCountry):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            sql_command = "exec Usp_CreateInvoice ?, ?, ?, ?"
            params = (Customercode, BillingAddress, BillingCity, BillingCountry)
            cursor.execute(sql_command,params)
            conn.commit()
            return True, "فاکتور با موفقیت ثبت شد."
        
        except pyodbc.Error as db_err:
            error_message = str(db_err)
            print(f"خطای دیتابیس از تریگر دریافت شد: {error_message}")
            if conn: # اگر اتصال برقرار بود
                conn.rollback()
            return False,error_message
        
        except Exception as e:
            print(f"خطا در Invoice: {e}")
            if conn:
                conn.rollback()
            return False, f"یک خطای پیش‌بینی نشده رخ داد: {e}" 

        finally :
            if cursor:
                cursor.close()