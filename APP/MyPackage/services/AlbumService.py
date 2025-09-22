# import sys
# from database.AlbumDAL import AlbumDAL
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
# from MyPackage import AlbumDAL 
from ..database.AlbumDAL import AlbumDAL

class AlbumService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_Albums_artists(self):
        try:
            dal = AlbumDAL(self.db_manager)
            album_list = dal.fetch_Albums_artists()
            return album_list
        except Exception as e:
            print(f"خطا: {e}")
            return []
