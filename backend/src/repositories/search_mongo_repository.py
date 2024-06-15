"""Data repository for search definitions to find new job posts"""
import os
from pymongo import MongoClient

class SearchRepository():
    """Data repository for search definitions to find new job posts"""

    def __init__(self):
        connection_string = os.environ.get("MONGODB_CONNECTIONSTRING")
        db = MongoClient(connection_string).get_database('JobMatcher')
        collections = db.list_collection_names()
        if not 'Search' in collections:
            db.create_collection('Search')
        self.collection = db.get_collection('Search')

    def save_search(self, name, data):
        """Save a new search definition"""
        if not name:
            return False
        data['name'] = name
        result = self.collection.insert_one(data)
        return not result.inserted_id is None

    def get_search_configs(self):
        """Get all search definitions"""
        result = []
        for resume in self.collection.find():
            del resume['_id']
            result.append(resume)
        return result

    def get_search_config(self, name):
        """Get a search definition by name"""
        result = self.collection.find_one({'name': name})
        del result['_id']
        return result

    def save_search_run_data(self, name, data):
        """Save data about the run of a particular search"""
        return self.collection.update_one({'name': name},
                                          {'$set' : {'runData': data}}).modified_count > 0
