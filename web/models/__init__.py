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
    tokens = relationship("Token", back_populates="service", cascade="all, delete-orphan")


class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    service_id = Column(CHAR(36), ForeignKey("services.id"), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(Enum("crawler", "request", "e2e", "capture", name="task_type"), nullable=False)
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
    output = Column(Text, nullable=True)  # resultado principal: string, versão, link, erro, etc.
    timestamp = Column(DateTime, default=now_utc)

    task = relationship("Task", back_populates="results")


class Token(db.Model):
    __tablename__ = "tokens"

    id = Column(CHAR(36), primary_key=True, default=generate_uuid)
    service_id = Column(CHAR(36), ForeignKey("services.id"), nullable=False)
    token = Column(String(128), unique=True, nullable=False)
    type = Column(Enum("webhook", "api", "cli", "master", name="token_type"), nullable=False)
    created_at = Column(DateTime, default=now_utc)
    expires_at = Column(DateTime, nullable=True)

    service = relationship("Service", back_populates="tokens")