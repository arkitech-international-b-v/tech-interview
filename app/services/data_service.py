from datetime import datetime, timedelta
import os
from app.repositories.data_repository import MongoRepository

class DataService:
    def __init__(self):
        self.repository = MongoRepository(
            uri=str(os.getenv("MONGO_URI")),
            db_name=str(os.getenv("MONGO_DB_NAME")),
            collection_name=str(os.getenv("MONGO_COLLECTION_NAME"))
        )
    ## implement all the methods from the repository here
    def get_latest_item(self, topic=None):
        return self.repository.get_latest_item(topic)
    
    def get_latest_items(self, limit=100, topic=None):
        return self.repository.get_latest_items(limit, topic)   
    
    def get_items_by_timerange(self, start_time, end_time, topic=None):
        return self.repository.get_items_by_timerange(start_time, end_time, topic)
    
    def insert_item(self, item):
        return self.repository.insert_item(item)
    
    def insert_items(self, items):
        return self.repository.insert_items(items)
        
    def get_all_data(self, limit=100, topic=None):
        cursor = self.repository.get_latest_items(limit, topic)
        items = list(cursor)
        return items
    