"""Matches a post to a resume based on the cosine similarity of their entity vectors"""
from matchers.matcher import Matcher
import helpers.vector_helpers

class EntityMatcher(Matcher):
    """Matches a post to a resume based on the cosine similarity of their entity vectors"""
    def __init__(self, default=False):
        self.default = default

    def initialize(self):
        """Performs any necessary one time initialization"""

    def match(self, post_data, resume_data):
        """Calculates the match between the post and resume"""
        post_vector = helpers.vector_helpers.entity_vector_to_named_vector(post_data['entities'])
        resume_vec = helpers.vector_helpers.entity_vector_to_named_vector(resume_data['entities'])
        return helpers.vector_helpers.cosine_sim_named_vector(post_vector, resume_vec)

    def get_matcher_name(self):
        """Provides the name to store the match data under"""
        return 'entity_matcher_scores'

    def is_default_matcher(self):
        """Indicates if the score from this matcher should be considered the default for display"""
        return self.default
