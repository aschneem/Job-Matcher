"""Class to facilitate analyzers"""
from analyzers.analyzer_engine import AnalyzerEngine
from analyzers.entity_analyzer import EntityAnalyzer
from analyzers.pos_analyzer import PoSAnalyzer
from analyzers.text_rank_analyzer import TextRankAnalyzer
from analyzers.rake_analyzer import RakeAnalyzer

class AnalyzerService():
    """Class to facilitate analyzers"""

    def __init__(self):
        self.analyzer_engine = AnalyzerEngine(
            [ EntityAnalyzer(),
              PoSAnalyzer(),
              TextRankAnalyzer(),
              RakeAnalyzer()]
        )

    def analyze(self, text, meta):
        """Analyzes the text"""
        return self.analyzer_engine.analyze(text, meta)
