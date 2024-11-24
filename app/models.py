from pymongo import MongoClient
from datetime import datetime
from uuid import uuid4

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["DNS"]
collection = db["dns_analyses"]

def save_analysis_result(analysis_id: str, domain: str, result: dict):
    data = {
        "_id": analysis_id,
        "domain": domain,
        "result": result,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(data)

def get_analysis_result(analysis_id: str):
    result = collection.find_one({"_id": analysis_id})
    if result:
        # return {
        #     "domain": result["domain"],
        #     "result": result["result"],
        #     "status": result["status"]
        # }
        return {
            "domain": result["domain"],
            "timestamp":result["timestamp"],
            "result": result["result"]
                }
    return None
