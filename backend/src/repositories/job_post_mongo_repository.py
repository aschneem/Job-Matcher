"""Repository class for Job Posts stored in MongoDB"""
import os
import hashlib
import re
from pymongo import MongoClient

class JobPostRepository():
    """Repository class for Job Posts stored in MongoDB"""

    def __init__(self):
        connection_string = os.environ.get("MONGODB_CONNECTIONSTRING")
        db = MongoClient(connection_string).get_database('JobMatcher')
        collections = db.list_collection_names()
        if not 'JobPosts' in collections:
            db.create_collection('JobPosts')
        self.collection = db.get_collection('JobPosts')
        self.post_list_projection = {'contentID': 1, 'entities': 1, 'match_data': 1, 'postLink': 1,
            'search': 1, 'searchName': 1, 'timestamp': 1, 'url': 1}

    def get_post_data(self, content_id):
        """Get the data for a specific job post"""
        result = self.collection.find_one({'contentID': content_id})
        del result['_id']
        return result

    def get_all_posts(self, sort_key=None):
        """Get the data for all job posts"""
        result = []
        cursor = self.collection.find({'status': 'created'}, projection=self.post_list_projection)
        if sort_key:
            cursor = cursor.sort(sort_key, -1)
        for post in cursor:
            del post['_id']
            result.append(post)
        return result
    
    def get_all_posts_for_matcher(self):
        result = []
        cursor = self.collection.find({'status': 'created'})
        for post in cursor:
            del post['_id']
            result.append(post)
        return result

    def get_all_posts_by_status(self, status, sort_key=None):
        """Get all job posts with a particular status"""
        result = []
        cursor = self.collection.find({'status': status}, projection=self.post_list_projection)
        if sort_key:
            cursor = cursor.sort(sort_key, -1)
        for post in cursor:
            del post['_id']
            result.append(post)
        return result

    def get_posts_by_search_name(self, name, sort_key=None):
        """Get all job posts saved by a particular search"""
        result = []
        cursor = self.collection.find({'searchName': name}, projection=self.post_list_projection)
        if sort_key:
            cursor = cursor.sort(sort_key, -1)
        for post in cursor:
            del post['_id']
            result.append(post)
        return result

    def post_exists(self, content_id):
        """Checks to see if a post with the content id has already been saved"""
        return self.collection.count_documents({'contentID': content_id}, limit=1) > 0

    def save_post(self, text, html, meta):
        """Save a job post"""
        text = self.normalize(text)
        content_id = self.sha1_value(text)
        print("save "+content_id)
        meta['text'] = text
        meta['contentID'] = content_id
        meta['html'] = html
        meta['status'] = 'created'
        result = self.collection.insert_one(meta)
        return not result.inserted_id is None

    def update_post(self, content_id, meta):
        """Update a job post"""
        return self.collection.update_one({'contentID': content_id},
                                           {'$set' : meta}).modified_count > 0

    #PRIVATE
    def normalize(self, string):
        """Normalize string content before making an id"""
        string = re.sub(r'\b\d+k?\b', '', string)
        string = re.sub(r'\s+', ' ', string)
        string = re.sub(r'[^\x00-\x7F]+', '', string)
        return string.strip()

    def sha1_value(self, string):
        """Calculates the SHA-1 hash of a string"""
        sha1 = hashlib.sha1()
        sha1.update(string.encode('utf-8'))
        return sha1.hexdigest()

    def remove_non_utf8(self, text):
        """Remove non-utf8 characters from a string"""
        regex = (
            r"[^\x00-\x7F]"
            r"|[^\xC2-\xDF][\x80-\xBF]"
            r"|\xE0-\xEF][\x80-\xBF]{2}"
            r"|\xF0-\xF7][\x80-\xBF]{3}"
        )
        clean_text = re.sub(regex, "", text)
        return clean_text
