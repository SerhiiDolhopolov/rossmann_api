from fastapi import APIRouter, Depends, HTTPException
from pydantic import EmailStr
from sqlalchemy.orm import Session
from rossmann_oltp.models import Employee

from app.schemas import EmployeeSchema
from app.oltp_db import get_db


router = APIRouter(prefix="/employees", tags=["employees"])


@router.get('/authorize', response_model=EmployeeSchema)
async def authorize_employee(email: EmailStr, 
                             password: str, 
                             db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.email == email).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if employee.password != password:
        raise HTTPException(status_code=401, detail="Invalid password")
    employee_schema = EmployeeSchema(employee_uuid=employee.employee_uuid,
                                     first_name=employee.first_name,
                                     last_name=employee.last_name,
                                     role=employee.role)
    return employee_schema
