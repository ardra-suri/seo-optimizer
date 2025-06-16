# scraper/core.py

import time
import os
import sys
from typing import Dict, Optional
from scraper.storage.database import ScrapeDB
# Initialize the database
db = ScrapeDB("data/seo_optimizer.db")

try:
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd

    # Setup path for importing internal modules
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, PROJECT_ROOT)

    try:
        from scraper.analysis.content_analyzer import ContentAnalyzer
        TF_ANALYSIS_AVAILABLE = True
    except ImportError as e:
        print(f"TF Analysis Import Failed: {str(e)}")
        TF_ANALYSIS_AVAILABLE = False
        ContentAnalyzer = None

    # User agent rotation
    try:
        from fake_useragent import UserAgent
        ua = UserAgent()
        DEFAULT_HEADERS = {'User-Agent': ua.chrome}
    except Exception:
        # Fallback
        DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0'}

    print("All libraries loaded successfully!")

except ImportError as e:
    print(f"Critical import missing: {e}")
    print("Run: pip install requests beautifulsoup4 pandas fake-useragent tensorflow tensorflow-hub")
    TF_ANALYSIS_AVAILABLE = False
    DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0'}


def compare_with_competitor(your_url: str, competitor_url: str) -> dict:
    """
    Compare your content with a competitor's using semantic analysis.
    Saves results to the database on success.
    """
    if not TF_ANALYSIS_AVAILABLE:
        return {
            'error': 'TensorFlow analysis unavailable',
            'python_path': sys.path,
            'installed_packages': os.popen("pip list").read()
        }

    try:
        analyzer = ContentAnalyzer()
        # Perform scraping of both URLs
        your_data = scraper(your_url)
        competitor_data = scraper(competitor_url)

        # If either scrape failed, return an error without running analysis
        if your_data.get('status') != 'success' or competitor_data.get('status') != 'success':
            return {
                'error': f"Scraping failed: yours={your_data.get('status')}, competitor={competitor_data.get('status')}",
                'details': {'yours': your_data, 'competitor': competitor_data}
            }

        # Both scrapes succeeded: run semantic analysis
        raw_analysis = analyzer.generate_gap_report(your_data['text'], competitor_data['text'])
        # Extract fields (handle possible naming differences)
        similarity = raw_analysis.get('similarity_score', raw_analysis.get('similarity', 0.0))
        missing = raw_analysis.get('top_missing_keywords', raw_analysis.get('missing_keywords', []))
        word_diff = raw_analysis.get('word_count_diff', 0)

        # Save analysis summary to the database
        db.save_analysis(
            url1=your_url,
            url2=competitor_url,
            similarity=similarity,
            missing_keywords=missing
        )

        # Return the detailed result
        return {
            'your_content': your_data,
            'competitor_content': competitor_data,
            'analysis': {
                'similarity_score': similarity,
                'word_count_diff': word_diff,
                'top_missing_keywords': missing
            }
        }

    except Exception as e:
        # Any unexpected error is caught and reported
        return {'error': str(e)}


def scraper(url, timeout=10, retries=3, headers=None):
    """
    Web scraping function with retry logic.
    """
    final_headers = headers if headers is not None else DEFAULT_HEADERS

    last_error = None
    last_status = None

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=final_headers, timeout=timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            for element in soup(['script', 'style', 'iframe', 'nav', 'footer']):
                element.decompose()

            text = soup.get_text(separator=' ', strip=True)

            time.sleep(1.5)
            
            if response.ok and text:
                db.save_scrape(url, text, word_count=len(text.split()), char_count=len(text))

            return {
                'status': 'success',
                'url': url,
                'text': text,
                'chars': len(text),
                'words': len(text.split()),
                'attempt': attempt + 1
            }

        except requests.exceptions.HTTPError as e:
            last_error = str(e)
            last_status = e.response.status_code
            print(f"Attempt {attempt + 1} failed: {type(e).__name__} {last_status}")
            time.sleep(2 ** attempt)
        except requests.exceptions.RequestException as e:
            last_error = str(e)
            print(f"Attempt {attempt + 1} failed: {type(e).__name__}")
            time.sleep(2 ** attempt)

    return {
        'status': 'failed',
        'url': url,
        'error': f"HTTP {last_status} - All {retries} attempts failed" if last_status else f"All {retries} attempts failed",
        'last_error': last_error,
        'http_status': last_status
    }

