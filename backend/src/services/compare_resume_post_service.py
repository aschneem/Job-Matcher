from repositories.job_post_mongo_repository import JobPostRepository
from repositories.resume_mongo_repository import ResumeRepository
from services.synonym_service import SynonymService
import helpers.vector_helpers

class CompareResumePostService():
    """Facilitates comparison between a resume and a job post"""

    def __init__(self, post_repo: JobPostRepository, resume_repo: ResumeRepository):
        self.post_repo = post_repo
        self.resume_repo = resume_repo
        self.synonym_service = SynonymService()

    def compare(self, resume_name, content_id):
        """Compares a resume and a job post"""
        resume_data = self.resume_repo.get_resume_data(resume_name)
        post_data = self.post_repo.get_post_data(content_id)
        result = {
            'postID': content_id,
            'resume': resume_name,
            'searchName': post_data.get('searchName', ''),
            'postUrl': post_data.get('url', ''),
            'postTitle': post_data.get('postLink', ''),
            'postText': post_data.get('text', ''),
            'resumeText': resume_data.get('text', ''),
            'entities': self.compare_entities(resume_data, post_data),
            'nounCompare': self.compare_pos(resume_data, post_data, 'NOUN'),
            'properNounCompare': self.compare_pos(resume_data, post_data, 'PROPN'),
            'verbCompare': self.compare_pos(resume_data, post_data, 'VERB'),
            'adverbCompare': self.compare_pos(resume_data, post_data, 'ADV'),
            'adjectiveCompare': self.compare_pos(resume_data, post_data, 'ADJ'),
            'textRankCompare': self.compare_keywords(resume_data, post_data, 'text_rank'),
            'rakeCompare': self.compare_keywords(resume_data, post_data, 'rakeResults'),
            'match_data': post_data.get('match_data', {})  
        }
        return result

    def compare_vectors(self, resume_vec, post_vec):
        """Compares a resume vector with a post vector"""
        res_results = []
        intersection = []
        post_results = []
        for entity in resume_vec.keys():
            if entity in post_vec.keys():
                intersection.append(entity)
            else:
                res_results.append(entity)
        for entity in post_vec.keys():
            if not entity in resume_vec.keys():
                post_results.append(entity)
        result = {
            'resumeOnly': res_results,
            'intersection': intersection,
            'postOnly': post_results,
        }
        return result

    def get_score_for_type(self, post_data, score_type, resume_data):
        """Gets the score for the type"""
        key = self.get_score_key_for_type(score_type)
        return post_data.get('match_data', {}).get(key, {}).get(resume_data['name'], '')

    def get_score_key_for_type(self, score_type):
        """Gets the key that the type of score is stored with"""
        if score_type == 'entities':
            return 'entity_matcher_scores'
        elif score_type == 'rakeResults':
            return 'rake_score'
        elif score_type == 'text_rank':
            return 'text_rank'
        elif score_type == 'VERB':
            return 'verb_alignment'
        elif score_type == 'NOUN':
            return 'noun_alignment'
        elif score_type == 'PROPN':
            return 'pnoun_alignment'
        elif score_type == 'ADJ':
            return 'adjective_alignment'
        elif score_type == 'ADV':
            return 'adverb_alignment'
        return score_type

    def compare_keywords(self, resume_data, post_data, keyword_type):
        """Compares keywords between a resume and job post"""
        resume_vec = helpers.vector_helpers.keyword_vector_to_named_vector(
            resume_data.get(keyword_type, []))
        post_vec = helpers.vector_helpers.keyword_vector_to_named_vector(
            post_data.get(keyword_type, []))
        result = self.compare_vectors(resume_vec, post_vec)
        result['score'] = self.get_score_for_type(post_data, keyword_type, resume_data)
        result['suggestions'] = self.get_suggestions(result)
        return result

    def compare_entities(self, resume_data, post_data):
        """Compares entities between a resume and job post"""
        resume_vec = helpers.vector_helpers.entity_vector_to_named_vector(
            resume_data.get('entities', []))
        post_vec = helpers.vector_helpers.entity_vector_to_named_vector(
            post_data.get('entities', []))
        result = self.compare_vectors(resume_vec, post_vec)
        result['score'] = self.get_score_for_type(post_data, 'entities', resume_data)
        return result
    
    def compare_pos(self, resume_data, post_data, pos):
        """Compares parts of speach between a resume and job post"""
        resume_vec = helpers.vector_helpers.pos_list_to_named_vector(
            resume_data.get('pos_data', {}).get(pos, []))
        post_vec = helpers.vector_helpers.pos_list_to_named_vector(
            post_data.get('pos_data', {}).get(pos, []))
        result = self.compare_vectors(resume_vec, post_vec)
        result['score'] = self.get_score_for_type(post_data, pos, resume_data)
        result['suggestions'] = self.get_suggestions(result)
        return result

    def get_suggestions(self, compare_object):
        """Gets suggestions for a resume based off of the differences"""
        suggestions = []
        for word in compare_object['resumeOnly']:
            synonyms = self.synonym_service.get_synonyms(word)
            for synonym in synonyms:
                if synonym.strip() in compare_object['postOnly']:
                    suggestions.append(word + ' -> ' + synonym )
                    break
        return suggestions
