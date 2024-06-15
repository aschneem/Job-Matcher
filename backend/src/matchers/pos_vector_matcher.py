"""Matches posts to resumes based on the cosine similarity of parts of speach vectors"""
from matchers.matcher import Matcher
import helpers.vector_helpers

class PosVectorMatcher(Matcher):
    """Matches posts to resumes based on the cosine similarity of parts of speach vectors"""
    def __init__(self, pos, name, default=False):
        self.pos = pos
        self.name = name
        self.default = default

    def initialize(self):
        """Performs any necessary one time initialization"""

    def match(self, post_data, resume_data):
        """Calculates the match score between a post and resume using the 
        cosine similarity of a particular part of speach vector"""
        post_vector = helpers.vector_helpers.pos_list_to_named_vector(
            post_data['pos_data'].get(self.pos, []))
        resume_vector = helpers.vector_helpers.pos_list_to_named_vector(
            resume_data['pos_data'].get(self.pos, []))
        return helpers.vector_helpers.cosine_sim_named_vector(post_vector, resume_vector)

    def get_matcher_name(self):
        """The name to store the score under"""
        return self.name

    def is_default_matcher(self):
        """Whether the score should be used as the default when displaying to the user"""
        return self.default
