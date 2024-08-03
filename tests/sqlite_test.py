import os
import unittest
import ujson
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from firepit import BundleManager

from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
from helpers import tmp_storage,tmp_sql_storage
import stix2
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

class SqliteStix(unittest.TestCase):
    def test_loader(self):

        store = tmp_sql_storage("stix.sqlite","stix")

        with open("./test_bundle.json", 'r') as fp:
            data = ujson.loads(fp.read())

            bundle_in = stix2.parse(data, allow_custom=True)
            BundleManager.write_bundle(store, bundle_in)

            # list all bundles
            bundle_ids = BundleManager.read_bundle_ids(store)

            assert len(bundle_ids) == 1

            store.delete()


    def test_vanna(self):
        vn = MyVanna(config={'api_key': os.getenv("OPEN_AI"), 'model': 'gpt-4o'})

        from stix2 import Indicator
        from stix2 import Bundle

        indicator = Indicator(name="File hash for malware variant",
                              pattern="[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
                              pattern_type="stix")

        store = tmp_sql_storage("stix.sqlite", "stix",clear=True)

        bundle = Bundle(indicator)

        BundleManager.write_bundle(store, bundle)

        vn.connect_to_sqlite("stix.sqlite")

        vn.train(
            question="How many indicators are in total?",
            sql="SELECT COUNT(*) FROM indicator"
        )

        sql = vn.generate_sql("How many indicators do we have?")

        result = vn.run_sql(sql)

        print(result)
        #store.delete()

    def test_info_schema(self):
        # The information schema query may need some tweaking depending on your database. This is a good starting point.
        vn = MyVanna(config={'api_key': os.getenv("OPEN_AI"), 'model': 'gpt-4o'})

        vn.connect_to_sqlite("stix.sqlite")

        df_info = vn.run_sql("SELECT * FROM sqlite_master")

        for idx,row in df_info.iterrows():
            if row['type']=="table":
                if row['sql']: vn.train(ddl=row['sql'])

if __name__ == '__main__':
    unittest.main()
