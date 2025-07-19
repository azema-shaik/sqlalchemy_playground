from sqlalchemy import create_engine 
from sqlalchemy.orm import Session
from config import config

engine = create_engine(url = config.connection_url_sync, echo = True)
session = Session(bind = engine)