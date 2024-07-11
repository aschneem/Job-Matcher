"""Data repository for the persisting scripts"""
import os
from pymongo import MongoClient

class ScriptRepository():
    """Data repository for script definitions to interact and return data from a browser"""

    def __init__(self):
        collection_name = "Script"
        connection_string = os.environ.get("MONGODB_CONNECTIONSTRING")
        db = MongoClient(connection_string).get_database('JobMatcher')
        collections = db.list_collection_names()
        if not collection_name in collections:
            db.create_collection(collection_name)
        self.collection = db.get_collection(collection_name)

    def save_script(self, name, data):
        """Save a new script"""
        if not name:
            return False
        data['name'] = name
        result = self.collection.insert_one(data)
        return not result.inserted_id is None

    def get_scripts(self):
        """Get all scripts"""
        result = []
        for resume in self.collection.find():
            del resume['_id']
            result.append(resume)
        return result

    def get_script(self, name):
        """Get a script by name"""
        result = self.collection.find_one({'name': name})
        del result['_id']
        return result

    def update_script(self, name, script):
        """Update a script"""
        return self.collection.update_one({'name': name},
                                           {'$set' : script}).modified_count > 0
