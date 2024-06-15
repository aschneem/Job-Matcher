"""Analyzes keywords in the text using Text Rank"""
from analyzers.analyzer import Analyzer
from TextRank4Keyword import TextRank4Keyword

class TextRankAnalyzer(Analyzer):
    """Analyzes keywords in the text using Text Rank"""
    def __init__(self):
        self.text_ranker = TextRank4Keyword()

    def analyze(self, text, meta):
        """Analyzes keywords in the text using Text Rank"""
        self.text_ranker.analyze(text)
        keywords = self.text_ranker.get_keywords_list(100)
        keywords_meta = []
        for keyword in keywords:
            keywords_meta.append({'keyword': keyword[0], 'score': keyword[1]})
        meta['text_rank'] = keywords_meta
        return meta
