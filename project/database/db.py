import pymongo
from .. import *


database = pymongo.MongoClient('mongodb://elos:baliteam888@localhost:27017/?authSource=admin&readPreference=primary')
database = database['contacttracing']




