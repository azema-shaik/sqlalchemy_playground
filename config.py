import json
from dataclasses import dataclass 

@dataclass
class Config:
    connection_url_sync: str 
    employees_info: str 
    logs: str 
    base_path: str
    connection_url_async: str 
    celery_broker: str 
    celery_backend: str

    @classmethod
    def from_json(cls, filename: str) -> "Config":
        with open(filename) as f:
            dct = json.load(f)
        return cls(**dct)

config = Config.from_json("config.json")