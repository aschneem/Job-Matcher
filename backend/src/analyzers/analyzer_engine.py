"""Module for analyzing job post and resume text"""

class AnalyzerEngine(): # pylint: disable=R0903
    """Engine responsible for running various analyzers and 
    compiling the analyzer data for job post or resume text"""
    def __init__(self, analyzers):
        self.analyzers = analyzers

    def analyze(self, text, meta):
        """analyzes the given text"""
        for analyzer in self.analyzers:
            meta = analyzer.analyze(text, meta)
        return meta
