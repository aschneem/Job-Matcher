"""Data repository for resumes in MongoDB"""
import os
from pymongo import MongoClient

class ResumeRepository():
    """Data repository for resumes in MongoDB"""

    def __init__(self):
        connection_string = os.environ.get("MONGODB_CONNECTIONSTRING")
        db = MongoClient(connection_string).get_database('JobMatcher')
        collections = db.list_collection_names()
        if not 'Resume' in collections:
            db.create_collection('Resume')
        self.collection = db.get_collection('Resume')

    def get_resume_data(self, name):
        """Gets the data for a resume with a particular name"""
        result = self.collection.find_one({'name': name})
        del result['_id']
        del result['file']
        return result

    def get_resume_file(self, name):
        """Gets the PDF file bytes for a resume with a particular name"""
        result = self.collection.find_one({'name': name})
        return result['file']

    def get_all_resumes(self):
        """Gets all resumes"""
        result = []
        for resume in self.collection.find():
            del resume['_id']
            del resume['file']
            result.append(resume)
        return result

    def get_default_resume(self):
        """Get the resume marked as the default"""
        result = self.collection.find_one({'default': True})
        del result['_id']
        del result['file']
        return result

    def set_default_resume(self, name):
        """Set a resume as the default"""
        for resume in self.collection.find({'default': True}):
            self.update_resume(resume['name'], {'default': False})
        return self.update_resume(name, {'default': True})

    def save_resume(self, name, data):
        """Save a new resume"""
        data['name'] = name
        result = self.collection.insert_one(data)
        return not result.inserted_id is None

    def update_resume(self, name, meta):
        """Update a resume"""
        return self.collection.update_one({'name': name}, {'$set' : meta}).modified_count > 0
