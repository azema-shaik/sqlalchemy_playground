import re
import os
import json
from uuid import UUID
from zoneinfo import ZoneInfo
from datetime import datetime
from engine import engine, session, config
from models import Base, Department, Employee, Log 


Base.metadata.create_all(bind = engine)

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

    
    session.add_all(data)
    utc_tz = ZoneInfo('UTC')
    

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
                
       
                
    


session.commit()  