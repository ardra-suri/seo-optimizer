# tests/test_database.py
import os
import sqlite3
import tempfile
import json
from scraper.storage.database import ScrapeDB

def test_save_and_load_scrape():
    # Create a temporary database file
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = ScrapeDB(db_path)
        url = "http://example.com"
        content = "Hello world"
        word_count = 2
        char_count = 11

        # Save scrape data
        db.save_scrape(url, content, word_count, char_count)

        # Connect directly to SQLite to verify the data was saved correctly
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, content, word_count, char_count FROM scrapes")
        row = cursor.fetchone()
        conn.close()

        assert row == (url, content, word_count, char_count)
    finally:
        # Clean up the temporary database file
        os.remove(db_path)

def test_save_and_load_analysis():
    # Create a temporary database file
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = ScrapeDB(db_path)
        url1 = "http://example.com/page1"
        url2 = "http://example.com/page2"
        similarity = 0.85
        missing_keywords = ["key1", "key2", "key3"]

        # Save analysis data
        db.save_analysis(url1, url2, similarity, missing_keywords)

        # Verify data in the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url1, url2, similarity, missing_keywords FROM analyses")
        row = cursor.fetchone()
        conn.close()

        # The missing_keywords is stored as a JSON string in the database
        stored_url1, stored_url2, stored_sim, stored_missing_json = row
        assert (stored_url1, stored_url2, stored_sim) == (url1, url2, similarity)
        # Parse the JSON string to verify contents
        stored_missing = json.loads(stored_missing_json)
        assert stored_missing == missing_keywords
    finally:
        os.remove(db_path)

def test_get_recent_analyses():
    # Create a temporary database file
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        db = ScrapeDB(db_path)
        # Save multiple analysis entries
        db.save_analysis("urlA", "urlB", 0.5, ["x"])
        db.save_analysis("urlC", "urlD", 0.9, ["y", "z"])

        # Fetch recent analyses (default limit=5)
        recent = db.get_recent_analyses()
        # Should return a list of dicts with at most 5 items
        assert isinstance(recent, list)
        assert len(recent) == 2

        # The first returned entry should be the most recent (highest timestamp)
        first_entry = recent[0]
        assert first_entry["url1"] == "urlC"
        assert first_entry["url2"] == "urlD"
        assert first_entry["similarity"] == 0.9
        # Check that missing_keywords is returned as a list
        assert isinstance(first_entry["missing_keywords"], list)
    finally:
        os.remove(db_path)
