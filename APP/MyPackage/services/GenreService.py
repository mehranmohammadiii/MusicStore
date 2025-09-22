# import sys
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
from ..database.GenreDAL import GenreDAL



class GenreSrvice:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_Genre(self):
        try:
            GE1= GenreDAL(self.db_manager)
            Genre_list = GE1.fetch_Genre()
            return Genre_list
        except Exception as e:
            print(f"خطا: {e}")
            return []