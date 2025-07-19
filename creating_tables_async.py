import re
import os
import json
import asyncio
from uuid import UUID
from zoneinfo import ZoneInfo
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker

from engine import config
from models import Base, Department, Employee, Log 


def get_data():
    with open(os.path.join(config.base_path,config.employees_info)) as emp_f:
    
    
        employees = json.load(emp_f)
        data = [Department(id = idx, name = dep,
                employees = [ Employee(
                    emp_id = emp["emp_id"], first_name = emp["first_name"], last_name = emp["last_name"], 
                    gender = emp["gender"][0].upper(), department_id = idx)
                    for emp in employees
                ]) 
        
        for idx, (dep, employees) in enumerate(employees.items(), start = 1)
        ]
        return data

async def log_data(async_session: AsyncSession):
    utc_tz = ZoneInfo('UTC')
    async with async_session() as session:
        async with session.begin():
            log_path = os.path.join(config.base_path,config.logs)
            for log_file in os.listdir(log_path):
                log_file_path = os.path.join(log_path, log_file)
                with open(log_file_path) as log_f:
                    for log in log_f:
                        log = json.loads(log)
                        employee_id = re.search('(^[A-Z]+) ',log['msg']).group(1)
                        session.add(Log(
                                log_id = UUID(log["id"]), employee_id = employee_id,
                                dt = datetime.strptime(log["dt"],"%Y-%m-%d %H:%M:%S %z").astimezone(tz = utc_tz), 
                                level = log["level"],
                                ip = log["ip"], msg = log["msg"]
                            ))

async def insert(async_session: AsyncSession):
    async with async_session() as session:
        async with session.begin():
            session.add_all(get_data())

    await log_data(async_session)

        

async def create_async_table():
    async_engine = create_async_engine(config.connection_url_async, echo=True)
    # async_session = AsyncSession(bind = async_engine)
    async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_engine.begin() as conn:
        print("Creating tables")
        await conn.run_sync(Base.metadata.create_all)

    await insert(async_session)

    await async_engine.dispose()


asyncio.run(create_async_table())




    