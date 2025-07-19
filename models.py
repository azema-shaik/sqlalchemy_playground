from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, DateTime,Uuid, String

from sqlalchemy.ext.asyncio import AsyncAttrs

class ReprMixin:
    def __create_repr__(self, attribute):
        return f'<{self.__class__.__name__}({attribute} = {getattr(self,attribute)!r})>'

class JSONMixin:
    def json(self):
        return {k:v for k,v in self.__dict__.items() if not k.startswith('_')}

class Base(DeclarativeBase):
    ...

class Department(Base, JSONMixin,ReprMixin):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key = True, autoincrement= True)
    name: Mapped[str] = mapped_column(nullable = False)
    employees: Mapped[list["Employee"]] = relationship(back_populates = "department")

    def __repr__(self):
        return self.__create_repr__('name')


class Employee(Base, JSONMixin,ReprMixin):
    __tablename__ = "employees"
    emp_id: Mapped[str] = mapped_column(primary_key = True, nullable = False)
    first_name: Mapped[str]
    last_name: Mapped[str]
    gender: Mapped[str] = mapped_column(String(1), nullable = False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable = False)
    department: Mapped[Department] = relationship(back_populates = "employees")
    logs: Mapped[list["Log"]] = relationship(back_populates = "employee")

    def __repr__(self):
        return self.__create_repr__('emp_id')

class Log(Base, JSONMixin,ReprMixin):
    __tablename__ = "logs"
    log_id: Mapped[str] = mapped_column(Uuid, primary_key = True, nullable = False)
    employee_id: Mapped[str] = mapped_column(ForeignKey("employees.emp_id"), nullable = False)
    dt: Mapped[datetime] = mapped_column(DateTime)
    level: Mapped[str]
    ip: Mapped[str]
    msg: Mapped[str] = mapped_column(Text)
    employee:Mapped["Employee"] = relationship(back_populates = "logs")

    def __repr__(self):
        return self.__create_repr__('level')



# {
#       "gender": "male",
#       "first_name": "David",
#       "last_name": "Garcia",
#       "emp_id": "GARVID"
#     },

# {'id': 'f4ceb45f-6466-47a4-ac3c-9e4556a9f134', 
#  'dt': '2025-07-19 17:21:47 IST+0530', 
#  'level': 'WARNING', 'dep': 'Storage', 
#  'ip': '24.246.108.77', 
#  'msg': 'RODRIE temperature threshold nearing limit on Disk Array'}