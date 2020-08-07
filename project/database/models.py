from .db import database
import uuid
import asyncio

class Device(object):
    db = database['list_devices']
    def __init__(self, call_number= None, unique_id=None):
        self.call_number = call_number
        self.unique_id = unique_id
        self._id = uuid.uuid4().hex

    def json(self):
        return {
            '_id':self._id,
            'call_number':self.call_number,
            'unique_id':self.unique_id,
            'contact_devices':[]
        }
    def save_to_mongo(self):
        print(self.json())
        Device.db.insert(self.json())
        
    @staticmethod
    async def search_by_call_number(call_number):
        data = Device.db.find_one({'call_number':call_number})
        if data is not None:
            return data

    @staticmethod
    async def search_by_unique_id(unique_id):
        data = Device.db.find_one({'unique_id': unique_id})
        if data is not None:
            return data

    @classmethod
    async def update_contact_device(cls, unique_id, list_contact_device):
        device = cls.search_by_unique_id(unique_id)
        device_id = device['_id']
        Device.db.update_one({
            '_id':device_id
        },{
            '$set':{
                'contact_devices':list_contact_device
            }
        }, upsert=False)
        
    @classmethod
    async def register(cls, call_number, unique_id):
        device = cls.search_by_unique_id(unique_id)
        if device is None:
            new_device = cls(call_number, unique_id)
            new_device.save_to_mongo()
            return True
        else:
            return False