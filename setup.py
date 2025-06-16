# setup.py
from setuptools import setup, find_packages

setup(
    name="seo_scraper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "tensorflow>=2.12.0",
        "tensorflow-hub>=0.13.0",
        "fake-useragent>=1.4.0"
    ],
)