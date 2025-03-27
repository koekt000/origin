import requests
import random as r
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

link1 = 'https://rus-ege.sdamgia.ru/test?a=show_result&stat_id='
link2 = '&retriable=1'
response = requests.get(link1+'87637003'+link2)
html = response.text
DB_URL = "sqlite:///niggers.db"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()
html = html.replace('­', '')
print(html)
class tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    answer = Column(String)

Base.metadata.create_all(engine)


