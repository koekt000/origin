import requests
import re
import random as r
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
def parse(id):
    link1 = 'https://rus-ege.sdamgia.ru/test?a=show_result&stat_id='
    link2 = '&retriable=1'
    response = requests.get(link1+id+link2)
    html = response.text
    engine = create_engine("sqlite:///tasks.db")
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
    html = html.replace('­', '')
    class Task(Base):
        __tablename__ = "task"
        id = Column(Integer, primary_key=True, autoincrement=True)
        number =  Column(Integer)
        task = Column(String)
        answer = Column(String)
        
    Base.metadata.create_all(engine)

    patern_blocks = r'<div style="margin-bottom:25px" class="(?:right|not_right)">.*?(?=<div style="margin-bottom:25px" class="(?:right|not_right)">|<!--np-->|\Z)'
    blocks = re.findall(patern_blocks, html, re.DOTALL)
    patern_tasks = r'<div align="justify" width="100%" class="pbody">(.*?)(?=Пояснение)'
    patern_numbers = r'(?<=тип ).*?(?=<)'
    patern_answers = r'(?<=Правильный ответ:).*?(?=<)'
    session = Session()
    while '' in blocks:
        blocks.remove('')
    for i in blocks:
        tasks = re.findall(patern_tasks, i, re.DOTALL)
        tasks[0] = re.sub(r'<[^>]+>', '', tasks[0])
        tasks[0]= re.sub(r'&[^;]*;', '', tasks[0])
        numbers = re.findall(patern_numbers, i)
        answers = re.findall(patern_answers, i)
        answers.sort()
        print(tasks, answers, numbers)
        new_task = Task(task=tasks[0], answer=answers[-1], number = int(numbers[0]))
        session.add(new_task)

    session.commit()
    session.close()

for i in range(1000000, 9999999):
    try:
        parse('8'+str(i))
    except:
        pass