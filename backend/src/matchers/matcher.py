"""Matcher interface class"""

class Matcher():
    """Matcher interface class"""

    def initialize(self):
        """Performs any one time initialization"""

    def match(self, post_data, resume_data):
        """Calculates the match between the post and resume"""

    def get_matcher_name(self):
        """The name to store the match data under"""

    def is_default_matcher(self):
        """Whether this match should be used as a display default"""
