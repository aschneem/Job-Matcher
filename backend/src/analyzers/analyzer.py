"""Interface for analyzing job post and resume text"""

class Analyzer(): # pylint: disable=R0903
    """Interface class for Analyzers"""

    def analyze(self, text, meta):
        """Analyzes the text"""
        