# scraper/anaysis/content_analyzer.py
import tensorflow_hub as hub
import numpy as np
from typing import Dict
from collections import Counter
import re

class ContentAnalyzer:
    def __init__(self):
        self.model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    
    def _preprocess_text(self, text: str) -> str:
        """Basic text cleaning"""
        return re.sub(r'[^\w\s]', '', text.lower())
    
    def _get_keywords(self, text: str, top_n=5) -> list:
        """Extract top keywords"""
        words = self._preprocess_text(text).split()
        return [word for word, count in Counter(words).most_common(top_n)]
    
    def generate_gap_report(self, your_text: str, competitor_text: str) -> Dict:
        """Comprehensive content analysis"""
        your_clean = self._preprocess_text(your_text)
        competitor_clean = self._preprocess_text(competitor_text)
        
        # Calculate embeddings
        embeddings = self.model([your_clean, competitor_clean])
        similarity = float(np.inner(embeddings[0], embeddings[1]))
        
        # Keyword analysis
        your_kw = set(self._get_keywords(your_clean))
        competitor_kw = set(self._get_keywords(competitor_clean))
        
        return {
            'similarity_score': similarity,
            'word_count_diff': len(competitor_clean.split()) - len(your_clean.split()),
            'top_missing_keywords': list(competitor_kw - your_kw),
            'unique_keywords': list(your_kw - competitor_kw)
        }