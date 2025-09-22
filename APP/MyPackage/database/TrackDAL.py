import pyodbc
# from database.Db_Connection import DatabaseConnection
# from MyPackage import pyodbc

class TrackDAL:
    def __init__(self,db_manager):
        
        # self.db_conn_manager = DatabaseConnection()
        self.db_conn_manager=db_manager
        
    def fetch_top_selling_tracks(self):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            cursor.execute("select * from V_TopSellingTracks")
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
        
    def fetch_tracks(self):
        try:
            conn = self.db_conn_manager.connect()
            if conn is None:
                raise Exception("اتصال به دیتابیس برقرار نیست.")
            cursor = conn.cursor()
            cursor.execute("select * from V_AlbumTrackList")
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


  