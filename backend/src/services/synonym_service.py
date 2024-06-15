"""Service for getting Synonyms for words"""
import os
import time
from wordhoard import Synonyms
from pymongo import MongoClient

class SynonymService():
    """Service for getting Synonyms for words"""

    def __init__(self):
        self.cache = {}
        connection_string = os.environ.get("MONGODB_CONNECTIONSTRING")
        db = MongoClient(connection_string).get_database('JobMatcher')
        collections = db.list_collection_names()
        if not 'Cache' in collections:
            db.create_collection('Cache')
        self.collection = db.get_collection('Cache')

    def get_synonyms(self, word):
        """Gets synonyms for a word if they exist"""
        # pylint: disable=C0201
        if word in self.cache.keys():
            return self.cache[word]
        if self.in_persistant_cache(word):
            word_data = self.collection.find_one({'word': word})
            self.cache[word] = word_data['synonyms']
            return self.cache[word]
        synonym_lookup = Synonyms(word)
        result = synonym_lookup.find_synonyms()
        self.cache[word] = result
        self.collection.insert_one({'word': word, 'synonyms': result})
        print('LOOKUP')
        time.sleep(5)
        return result

    def in_persistant_cache(self, word):
        """Returns whether the word has synonyms stored in persistent cache"""
        return self.collection.count_documents({'word': word,
                                                'synonyms': { '$exists': True}}, limit=1) > 0
