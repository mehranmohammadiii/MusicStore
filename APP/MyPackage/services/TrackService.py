# import sys
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
from ..database.TrackDAL import TrackDAL


class TrackService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_top_selling_tracks(self):
        try:
            dal = TrackDAL(self.db_manager)
            top_track_list = dal.fetch_top_selling_tracks()
            return top_track_list
        except Exception as e:
            print(f"خطا: {e}")
            return []
    
    def get_tracks(self):
        try:
            dal = TrackDAL(self.db_manager)
            track_list = dal.fetch_tracks()
            return track_list
        except Exception as e:
            print(f"خطا: {e}")
            return []


