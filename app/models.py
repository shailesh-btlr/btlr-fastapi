from sqlalchemy import TIMESTAMP, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database import Base, engine


class User(Base):
    __tablename__ = "user"
    id = Column(Integer(), primary_key=True)
    email = Column(String())
    password = Column(String()) # OTP
    otp_valid_from = Column(DateTime(), default=func.now(), onupdate=func.now())


class Business(Base):
    __tablename__ = "business"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    prompt = Column(String)
    employees = relationship("Employee", back_populates="employer")


class Employee(Base):
    __tablename__ = "employee"
    id = Column(Integer(), primary_key=True)
    business_id = Column(Integer(), ForeignKey("business.id"))
    user_id = Column(Integer(), ForeignKey("user.id"))
    employer = relationship("Business", back_populates="employees")
    user = relationship("User")


class Department(Base):
    __tablename__ = "department"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    business_id = Column(Integer(), ForeignKey("business.id"))
    parent_id = Column(Integer(), ForeignKey("department.id"))
    parent = relationship(
        "Department",
        remote_side=[id],
        back_populates="children",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )
    children = relationship(
        "Department", back_populates="parent", cascade="all, delete-orphan"
    )


class Role(Base):
    __tablename__ = "role"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    description = Column(String())
    task_list = Column(String())
    business_id = Column(Integer(), ForeignKey("business.id"))
    parent_id = Column(Integer(), ForeignKey("role.id"))
    parent = relationship(
        "Role",
        remote_side=[id],
        back_populates="children",
        cascade="all, delete-orphan",
        passive_deletes=True,
        single_parent=True,
    )
    children = relationship(
        "Role", back_populates="parent", cascade="all, delete-orphan"
    )


class EmployeeFunction(Base):
    __tablename__ = "employee_function"
    id = Column(Integer(), primary_key=True)
    employee_id = Column(Integer(), ForeignKey("employee.id"))
    role_id = Column(Integer(), ForeignKey("role.id"))
    department_id = Column(Integer(), ForeignKey("department.id"))
    role = relationship("Role")
    department = relationship("Department")


class Touchpoint(Base):
    __tablename__ = "touchpoint"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    description = Column(String())
    business_id = Column(Integer(), ForeignKey("business.id"))
    department_id = Column(Integer(), ForeignKey("department.id"))
    business = relationship("Business")
    department = relationship("Department")
    touchpoint_clusters = relationship(
        "TouchpointCluster", cascade="all,delete"
    )  # noqa E501
    touchpoint_roles = relationship("TouchpointRole", cascade="all,delete")


class TouchpointCluster(Base):
    __tablename__ = "touchpoint_cluster"
    id = Column(Integer(), primary_key=True)
    name = Column(String())
    touchpoint_id = Column(Integer(), ForeignKey("touchpoint.id"))


class TouchpointRole(Base):
    __tablename__ = "touchpoint_role"
    id = Column(Integer(), primary_key=True)
    prompt = Column(String())
    touchpoint_id = Column(Integer(), ForeignKey("touchpoint.id"))
    role_id = Column(Integer(), ForeignKey("role.id"))
    role = relationship("Role")


class PreferenceSurvey(Base):
    __tablename__ = "preference_survey"
    id = Column(Integer(), primary_key=True)
    heading = Column(String())
    subheading = Column(String())
    slug = Column(String())
    image_url = Column(String())
    preference_list = Column(String())
    business_id = Column(Integer(), ForeignKey("business.id"))


class UserExperience(Base):
    __tablename__ = "user_experience"
    id = Column(Integer(), primary_key=True)
    business_id = Column(Integer(), ForeignKey("business.id"))
    user_id = Column(Integer(), ForeignKey("user.id"))
    state = Column(String())
    assigned_department_id = Column(Integer(), ForeignKey("department.id"))
    assigned_role_id = Column(Integer(), ForeignKey("role.id"))
    assigned_user_id = Column(Integer(), ForeignKey("user.id"))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())


class UserExperienceMemo(Base):
    __tablename__ = "user_experience_memo"
    id = Column(Integer(), primary_key=True)


Base.metadata.create_all(bind=engine)
