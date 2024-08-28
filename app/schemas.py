from pydantic import BaseModel
from typing import Dict, List


class TagBase(BaseModel):
    tag_name: Dict[str, str]


class CompanyCreate(BaseModel):
    company_name: Dict[str, str]
    tags: List[TagBase]


class Company(BaseModel):
    company_name: str


class CompanyDetail(Company):
    tags: List[str]


class TagSearchResponse(BaseModel):
    companies: List[Company]


class CompanyUpdateTags(BaseModel):
    tags: List[TagBase]
