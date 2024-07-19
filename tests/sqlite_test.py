import unittest

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
from helpers import tmp_storage,tmp_sql_storage

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

class SqliteStix(unittest.TestCase):
    def test_loader(self):
        vn = MyVanna(config={'api_key': 'sk-...', 'model': 'gpt-4-...'})
        tmp_sql_storage("stix.sqlite","stix")
        vn.connect_to_sqlite("stix.sqlite")


if __name__ == '__main__':
    unittest.main()
