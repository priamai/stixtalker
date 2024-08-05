import argparse
import glob
import stix2
import os
import ujson
__import__('pysqlite3')
import sys
from helpers import tmp_sql_storage
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from firepit import BundleManager
from dotenv import load_dotenv
from dbagent import StixVanna
load_dotenv()  # take environment variables from .env.

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("-t","--train",action="store_true")
args = parser.parse_args()

if args.train:
    print("Training...")

    store = tmp_sql_storage("train.sqlite", "stix", clear=True)
    for file in glob.glob("./data/examples/*.json"):
        with open(file, 'r') as fp:
            data = ujson.loads(fp.read())

            print("Parsing stix bundle... %s" % file)
            bundle_in = stix2.parse(data, allow_custom=True)
            BundleManager.write_bundle(store, bundle_in)

            print("Bundle loaded...")

    for file in glob.glob("./data/standard/*.json"):
        with open(file, 'r') as fp:
            print("Parsing stix objects... %s" % file)
            data = ujson.loads(fp.read())

            objects = [stix2.parse(obj, allow_custom=True) for obj in data]

            bundle_in = stix2.Bundle(objects)
            BundleManager.write_bundle(store, bundle_in)

            print("Bundle loaded...")

    for file in glob.glob("./data/appendix_b/*.json"):
        with open(file, 'r') as fp:
            print("Parsing stix objects... %s" % file)
            data = ujson.loads(fp.read())

            objects = [stix2.parse(obj, allow_custom=True) for obj in data]

            bundle_in = stix2.Bundle(objects)
            BundleManager.write_bundle(store, bundle_in)

            print("Bundle loaded...")

    vn = StixVanna(config={'api_key': os.getenv("OPEN_AI"), 'model': 'gpt-4o'})

    vn.connect_to_sqlite("train.sqlite")

    df_ddl = vn.run_sql("SELECT type, sql FROM sqlite_master WHERE sql is not null")

    for ddl in df_ddl['sql'].to_list():
        vn.train(ddl=ddl)

    training_data = vn.get_training_data()
    print("Total DDL statements: %d" % training_data.shape[0])



