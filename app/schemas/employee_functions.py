from pydantic import BaseModel
from app.schemas.departments import Department
from app.schemas.roles import Role


class EmployeeFunctionBase(BaseModel):
    employee_id: int
    role_id: int
    department_id: int


class EmployeeFunction(EmployeeFunctionBase):
    id: int


class EmployeeFunctionPopulated(EmployeeFunction):
    department: Department
    role: Role


class EmployeeFunctionCreate(EmployeeFunctionBase):
    pass


class EmployeeFunctionUpdate(EmployeeFunctionBase):
    pass


EmployeeFunctionList = list[EmployeeFunction]
EmployeeFunctionPopulatedList = list[EmployeeFunctionPopulated]
