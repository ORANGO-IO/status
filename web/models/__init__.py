from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey,
    Enum, Boolean, JSON
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from web.services.utils import generate_uuid, now_utc
from web import db

class Service(db.Model):
    __tablename__ = "services"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    slug = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=now_utc)

    tasks = relationship("Task", back_populates="service", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="service", cascade="all, delete-orphan")


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    service_id = Column(CHAR(36), ForeignKey("services.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum("check", "request", "e2e", "capture", name="task_type"), nullable=False)
    config = Column(JSON, nullable=True)  # parâmetros específicos por tipo
    active = Column(Boolean, default=True)
    last_status = Column(String(32))  # sucesso, erro, timeout etc.
    last_ran_at = Column(DateTime)

    service = relationship("Service", back_populates="tasks")
    results = relationship("TaskResult", back_populates="task", cascade="all, delete-orphan")


class TaskResult(db.Model):
    __tablename__ = "task_results"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    task_id = Column(CHAR(36), ForeignKey("tasks.id"), nullable=False)

    status = Column(String(32))  # ex: success, error, timeout, not_found
    output = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=now_utc)

    task = relationship("Task", back_populates="results")


class Credential(db.Model):
    __tablename__ = "credentials"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    role = Column(Enum("token", "password", name="credential_role"),
                  nullable=False)
    system = Column(Enum("webhook","api","cli","master","external", name="credential_system"),
                    nullable=True)
    service_id = Column(CHAR(36), ForeignKey("services.id"), nullable=True)
    secret = Column(String(128), nullable=False, unique=True) 
    created_at = Column(DateTime, default=now_utc)
    expires_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="credentials")