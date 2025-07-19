import json 
from dataclasses import dataclass
from sqlalchemy import create_engine 
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine

@dataclass
class Config:
    connection_url_sync: str 
    employees_info: str 
    logs: str 
    base_path: str
    connection_url_async: str 

    @classmethod
    def from_json(cls, filename: str) -> "Config":
        with open(filename) as f:
            dct = json.load(f)
        return cls(**dct)

config = Config.from_json("config.json")
engine = create_engine(url = config.connection_url_sync, echo = True)
session = Session(bind = engine)