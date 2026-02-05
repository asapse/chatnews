import os

import pytest
from pymongo import MongoClient


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    client = MongoClient()
    client.drop_database(os.getenv("MONGODB_DATABASE"))
