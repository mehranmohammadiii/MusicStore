import pyodbc
# import sys
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
# from MyPackage import pyodbc

class AlbumDAL:
    def __init__(self,db_manager):
        
        # self.db_conn_manager = DatabaseConnection()
        self.db_conn_manager=db_manager

    def fetch_Albums_artists(self):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM V_ArtistAlbumCount")
            rows = cursor.fetchall()
            return rows
        
        except pyodbc.Error as db_err:
            print(f"خطای دیتابیس در AlbumDAL رخ داد: {db_err}")
            return [] 
        
        except Exception as e:
            print(f"خطا در AlbumDAL: {e}")
            return [] 

        finally :
            if cursor:
                cursor.close()

    def a(self):
        pass  
# -------------------------------------------------------------
# def fetch_Albums_artists():
#     db=ConnectSQL()
#     mycursor=db.cursor()  
#     mycursor.execute("select * from V_ArtistAlbumCount")
#     rows =mycursor.fetchall()
#     mycursor.close()   
#     db.close()     
#     return rows 