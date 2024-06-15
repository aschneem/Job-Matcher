"""Matches resumes and posts using term frequency inverse document frequency TfIdf"""
from matchers.matcher import Matcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfIdfMatcher(Matcher):
    """Matches resumes and posts using term frequency inverse document frequency TfIdf"""

    def __init__(self, resume_repo, post_repo, default=False):
        self.resume_repo = resume_repo
        self.post_repo = post_repo
        self.similarity_matrix = None
        self.content_tuples = None
        self.feature_names = None
        self.default = default

    def initialize(self):
        """Performs one time initialization"""
        resume_data = self.resume_repo.get_all_resumes()
        post_data = self.post_repo.get_all_posts_for_matcher()
        self.content_tuples = []
        for post in post_data:
            self.content_tuples.append((post['contentID'], post['text']))
        for resume in resume_data:
            self.content_tuples.append((resume['name'], resume['text']))
        content_vec = []
        for content_tuple in self.content_tuples:
            content_vec.append(content_tuple[1])
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(content_vec)
        self.feature_names = vectorizer.get_feature_names_out()
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def match(self, post_data, resume_data):
        """Gets the match score between the given post and resume"""
        content_id = post_data['contentID']
        resume_name = resume_data['name']
        post_index = 0
        resume_index = 0
        for i, content_tuple in enumerate(self.content_tuples):
            if content_tuple[0] == content_id:
                post_index = i
            if content_tuple[0] == resume_name:
                resume_index = i
        return self.similarity_matrix[post_index][resume_index]

    def get_matcher_name(self):
        """The name to store the score under"""
        return 'TfIdf_scores'

    def is_default_matcher(self):
        """Whether to use this score as the default when displaying to the user"""
        return self.default
