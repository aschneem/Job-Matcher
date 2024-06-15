"""Analyzes named entities in the text"""
from analyzers.analyzer import Analyzer
import spacy

class EntityAnalyzer(Analyzer): # pylint: disable=R0903
    """Analyzer named entities in the text"""
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def analyze(self, text, meta):
        """Extracts named entities from the text"""
        nlp_result = self.nlp(text)
        entities = []
        for entity in nlp_result.ents:
            entities.append({"text": entity.text, "label": entity.label_})
        meta['entities'] = entities
        return meta
