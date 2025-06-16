# tests/test_scraper.py
from scraper.core import scraper
import pytest

def test_successful_scrape():
    result = scraper("https://en.wikipedia.org/wiki/Python")
    assert result['status'] == 'success'
    assert result['chars'] > 1000

def test_failed_scrape():
    result = scraper("https://httpbin.org/status/404")
    assert result['status'] == 'failed'
    assert "404" in result['error']