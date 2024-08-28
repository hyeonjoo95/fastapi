from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 관계 설정
    names = relationship("CompanyName", back_populates="company")
    tags = relationship("CompanyTag", back_populates="company")


class CompanyName(Base):
    __tablename__ = "company_name"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    language = Column(String(255))
    company_name = Column(String(255), index=True)

    # 외래키 설정
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    # 관계 설정
    company = relationship("Company", back_populates="names")


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    language = Column(String(255))
    company_tag = Column(String(255), index=True)

    # 외래키 설정
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    # 관계 설정
    company = relationship("Company", back_populates="tags")
