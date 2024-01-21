from settings import *
import requests
from requests.exceptions import RequestException
import pandas as pd
from storage import DBStorage
def search_api(query, pages =int(RESULT_COUNT/10)):
    """As per the API, each 'page' contains 10 results, and we set our result count to 20, so for every
    query we want 2 pages of results"""
    results = []
    for i in range(0,pages):
        start = i * 10 + i #rank the results from one through 20
