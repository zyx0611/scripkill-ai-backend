import json
import datetime as dt
import hashlib
from uuid import uuid4
import sys
sys.path.append("..")

from app.logger import getLogger
logger = getLogger(__name__)

# 用于保存到MongoDB的文档类，通用的
class Document:

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            if key == "_id":
                continue
            setattr(self, key, value)
            
        self.uuid = kwargs.get("uuid") or str(uuid4())
        
        self.created_at = kwargs.get("created_at") or dt.datetime.now().isoformat()
        self.updated_at = kwargs.get("updated_at") or dt.datetime.now().isoformat()
        if kwargs.get("text") is not None:
            self.text_sha1 = kwargs.get("text_sha1") or hashlib.sha1(str(kwargs.get("text")).encode("utf-8")).hexdigest()

    def put(self, key, value):
        self.updated_at = dt.datetime.now().isoformat()
        if key in self.__dict__:
            delattr(self,key)
        setattr(self, key, value)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def to_dict(self):
        if "_id" in self.__dict__:
            delattr(self, "_id")
        return self.__dict__

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_bytes(self):
        return self.to_json().encode("utf-8")
    
    def remove_keys(self, keys):
        for key in keys:
            if key in self.__dict__:
                self.__dict__.pop(key)
        return self