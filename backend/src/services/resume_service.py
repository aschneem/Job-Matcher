"""Service for initializing resume data"""
import io
from threading import Thread
from PyPDF2 import PdfReader
from repositories.resume_mongo_repository import ResumeRepository

class ResumeService():
    """Service for initializing resume data"""

    def __init__(self, analyzer, matcher, repo: ResumeRepository, synonym_service):
        self.analyzer = analyzer
        self.matcher = matcher
        self.repo = repo
        self.synonym_service = synonym_service

    def process_resume_file(self, name, file_data):
        """Processes a resume file and saves it"""
        if not name.endswith(".pdf"):
            return {}
        name = name[:-4]
        resume_stream = io.BytesIO(file_data)
        reader = PdfReader(resume_stream)
        text = ''
        for page in reader.pages:
            text = text + ' ' + page.extract_text()
        data = { 'name': name, 'file': file_data, 'text': text, 'compareStatus': 'initializing'}
        data = self.analyzer.analyze(text, data)
        self.cache_synonyms(data)
        if len(self.repo.get_all_resumes()) < 1:
            data['default'] = True
        self.repo.save_resume(name, data)
        self.matcher.run()
        return self.repo.get_resume_data(name)

    def cache_synonyms(self, resume):
        """Cache the synonyms for a resume since lookups can be time intensive"""
        words = set(map(lambda token: token['lemma'], resume.get('pos_data', {}).get('ADJ', [])))
        words = words | set(map(lambda token: token['text'],
                                resume.get('pos_data', {}).get('ADJ', [])))
        words = words | set(map(lambda token: token['lemma'],
                                resume.get('pos_data', {}).get('ADV', [])))
        words = words | set(map(lambda token: token['text'],
                                resume.get('pos_data', {}).get('ADV', [])))
        words = words | set(map(lambda token: token['lemma'],
                                resume.get('pos_data', {}).get('NOUN', [])))
        words = words | set(map(lambda token: token['text'],
                                resume.get('pos_data', {}).get('NOUN', [])))
        words = words | set(map(lambda token: token['lemma'],
                                resume.get('pos_data', {}).get('PROPN', [])))
        words = words | set(map(lambda token: token['text'],
                                resume.get('pos_data', {}).get('PROPN', [])))
        words = words | set(map(lambda token: token['lemma'],
                                resume.get('pos_data', {}).get('VERB', [])))
        words = words | set(map(lambda token: token['text'],
                                resume.get('pos_data', {}).get('VERB', [])))
        words = words | set(map(lambda keyword: keyword['keyword'], resume.get('text_rank', [])))
        words = words | set(map(lambda keyword: keyword['keyword'], resume.get('rakeResults', [])))
        thread = Thread(target=cache_synonyms_async,
                        args=(words, self.synonym_service, resume['name'], self.repo))
        thread.start()

def cache_synonyms_async(words, synonym_service, name, repo):
    """Cache the synonyms for a resume since lookup can be time intensive"""
    for word in words:
        synonym_service.get_synonyms(word)
    repo.update_resume(name, {'compareStatus': 'ready'})
