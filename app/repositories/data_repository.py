from pymongo import MongoClient
from datetime import datetime
import json

class MongoRepository:
    def __init__(self, uri, db_name, collection_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        # Create indexes for faster queries
        self.collection.create_index([("topic", 1)])
        self.collection.create_index([("timestamp", -1)])
    
    def get_latest_item(self, topic=None):
        query = {"topic": topic} if topic else {}
        return self.collection.find_one(query, sort=[('timestamp', -1)])
    
    def get_latest_items(self, limit=100, topic=None):
        if topic:
            topic_end = topic + '\ufff0'
        query = {"topic": {"$gte": topic, "$lt": topic_end}} if topic else {}
        return self.collection.find(query).sort([('timestamp', -1)]).limit(limit)
    
    def get_items_by_timerange(self, start_time, end_time, topic=None):
        query = {
            "timestamp": {"$gte": start_time, "$lte": end_time}
        }
        if topic:
            query["topic"] = topic
        return self.collection.find(query).sort([('timestamp', -1)])
    
    def insert_item(self, item):
        # Parse the payload if it's a string
        if "payload" in item and isinstance(item["payload"], str):
            try:
                payload_data = json.loads(item["payload"])
                
                # Extract timestamp to top level if present
                if "timestamp" in payload_data:
                    item["timestamp"] = datetime.fromisoformat(payload_data["timestamp"])
                    # Remove timestamp from payload to keep it lean
                    del payload_data["timestamp"]
                
                # Store payload as a document without the timestamp
                item["payload"] = payload_data
                
            except (json.JSONDecodeError, ValueError) as e:
                # Fallback to current time if parsing fails
                item["timestamp"] = datetime.utcnow()
        elif "timestamp" not in item:
            item["timestamp"] = datetime.utcnow()
            
        return self.collection.insert_one(item)
    
    def insert_items(self, items):
        processed_items = []
        for item in items:
            # Parse the payload if it's a string
            if "payload" in item and isinstance(item["payload"], str):
                try:
                    payload_data = json.loads(item["payload"])
                    
                    # Extract timestamp to top level if present
                    if "timestamp" in payload_data:
                        item["timestamp"] = datetime.fromisoformat(payload_data["timestamp"])
                        # Remove timestamp from payload to keep it lean
                        del payload_data["timestamp"]
                    
                    # Store payload as a document without the timestamp
                    item["payload"] = payload_data
                    
                except (json.JSONDecodeError, ValueError):
                    # Fallback to current time if parsing fails
                    item["timestamp"] = datetime.utcnow()
            elif "timestamp" not in item:
                item["timestamp"] = datetime.utcnow()
                
            processed_items.append(item)
            
        return self.collection.insert_many(processed_items)
    
    def close(self):
        self.client.close()