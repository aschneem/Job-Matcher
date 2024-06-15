"""Matches resume and job posts based on keyword data"""
from matchers.matcher import Matcher
import helpers.vector_helpers

class KeywordVectorMatcher(Matcher):
    """Matches resume and job posts based on keyword data"""
    def __init__(self, name, vector_key, default=False):
        self.name = name
        self.vector_key = vector_key
        self.default = default

    def initialize(self):
        """Perform any necessary one time initialization"""

    def match(self, post_data, resume_data):
        """Matches the post to the resume based on the cosine similarity between keyword vectors"""
        post_keywords = post_data[self.vector_key]
        resume_keywords = resume_data[self.vector_key]
        post_vector = helpers.vector_helpers.keyword_vector_to_named_vector(post_keywords)
        resume_vector = helpers.vector_helpers.keyword_vector_to_named_vector(resume_keywords)
        return helpers.vector_helpers.cosine_sim_named_vector(post_vector, resume_vector)

    def get_matcher_name(self):
        """The name to store the match data under"""
        return self.name

    def is_default_matcher(self):
        """Whether the matcher should be displayed a the default match score"""
        return self.default
