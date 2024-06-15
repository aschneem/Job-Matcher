"""Analyzes the text for keywords using RAKE"""
import os
from analyzers.analyzer import Analyzer
import RAKE

class RakeAnalyzer(Analyzer):
    """Analyzes the text for keywords using RAKE"""
    def __init__(self):
        stop_words_path = os.path.join(os.path.dirname(__file__), "stop.txt")
        self.rake_analyzer = RAKE.Rake(stop_words_path)

    def analyze(self, text, meta):
        """Extracts keywords from the text using RAKE"""
        results = self.rake_analyzer.run(text)
        rake_meta = []
        for keyword in results:
            rake_meta.append({'keyword': keyword[0], 'score': keyword[1]})
        meta['rakeResults']=rake_meta
        return meta
