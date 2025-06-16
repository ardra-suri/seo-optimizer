# tests/test_content_analyzer.py
import pytest
from scraper.analysis.content_analyzer import ContentAnalyzer

@pytest.fixture
def analyzer():
    return ContentAnalyzer()

def test_similarity_score_range(analyzer):
    score = analyzer.generate_gap_report("cats", "dogs")['similarity_score']
    assert 0 <= score <= 1

def test_keyword_detection(analyzer):
    report = analyzer.generate_gap_report(
        "Python is great", 
        "Machine learning is awesome"
    )
    assert isinstance(report['top_missing_keywords'], list)
    assert "machine" in report['top_missing_keywords']