"""Analyzes the parts of speach in the text"""
from analyzers.analyzer import Analyzer
import spacy
import helpers.vector_helpers

class PoSAnalyzer(Analyzer):
    """Analyzes the parts of speach in the text"""
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def analyze(self, text, meta):
        """Extracts data about the parts of speach of the tokens in the text"""
        nlp_result = self.nlp(helpers.vector_helpers.normalize(text))
        pos_map = {}
        for token in nlp_result:
            pos = pos_map.get(token.pos_, [])
            pos.append({'text': token.text, 'lemma': token.lemma_})
            pos_map[token.pos_] = pos
        meta['pos_data'] = pos_map
        return meta
