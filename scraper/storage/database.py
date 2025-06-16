# scraper/storage/database.py
import sqlite3
import os
import json
from datetime import datetime

class ScrapeDB:
    """
    A class for storing and retrieving scraped page data and analysis results using SQLite.
    """
    def __init__(self, db_path: str):
        """
        Initialize the database connection and create tables if they don't exist.
        :param db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        # Ensure that the database directory exists (e.g., data/ directory)
        directory = os.path.dirname(db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        # Create tables if they don't exist
        self._ensure_tables()

    def _ensure_tables(self):
        """
        Create the scrapes and analyses tables if they don't already exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scrapes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    content TEXT,
                    timestamp TEXT,
                    word_count INTEGER,
                    char_count INTEGER
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url1 TEXT NOT NULL,
                    url2 TEXT NOT NULL,
                    similarity REAL,
                    missing_keywords TEXT,
                    timestamp TEXT
                )
            """)
            # Optional: indexes for performance on frequently queried fields
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_scrapes_url ON scrapes(url)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyses_timestamp ON analyses(timestamp)")
            conn.commit()

    def save_scrape(self, url: str, content: str, word_count: int = None, char_count: int = None):
        """
        Save a scraped page's content and metadata to the database.
        :param url: URL of the scraped page.
        :param content: Text content of the page.
        :param word_count: (Optional) Number of words in the content.
        :param char_count: (Optional) Number of characters in the content.
        """
        # Compute word and character count if not provided
        if word_count is None:
            word_count = len(content.split())
        if char_count is None:
            char_count = len(content)
        # Use UTC timestamp for consistency
        timestamp = datetime.utcnow().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scrapes (url, content, timestamp, word_count, char_count)
                VALUES (?, ?, ?, ?, ?)
            """, (url, content, timestamp, word_count, char_count))
            # Changes are committed automatically when exiting the with-block

    def save_analysis(self, url1: str, url2: str, similarity: float, missing_keywords=None):
        """
        Save a content comparison analysis between two URLs.
        :param url1: First URL (e.g., target page).
        :param url2: Second URL (e.g., competitor page).
        :param similarity: Similarity score between the contents.
        :param missing_keywords: (Optional) List of keywords missing from url1 that appear in url2.
        """
        # Convert missing_keywords to JSON string if it's a list or tuple
        if isinstance(missing_keywords, (list, tuple)):
            missing_str = json.dumps(missing_keywords)
        else:
            # If it's already a string or None, handle accordingly
            missing_str = missing_keywords if missing_keywords else ""
        timestamp = datetime.utcnow().isoformat()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analyses (url1, url2, similarity, missing_keywords, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (url1, url2, similarity, missing_str, timestamp))

    def get_recent_analyses(self, limit: int = 5):
        """
        Retrieve recent analysis results, ordered by most recent timestamp.
        :param limit: Maximum number of results to return.
        :return: List of dicts, each representing an analysis row.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT url1, url2, similarity, missing_keywords, timestamp
                FROM analyses
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

        # Convert rows to a list of dicts for easy consumption (e.g. in a UI)
        results = []
        for row in rows:
            entry = dict(row)
            # Convert missing_keywords from JSON string to Python list if needed
            if entry.get("missing_keywords"):
                try:
                    entry["missing_keywords"] = json.loads(entry["missing_keywords"])
                except json.JSONDecodeError:
                    # If not valid JSON, leave as raw string
                    pass
            results.append(entry)
        return results
