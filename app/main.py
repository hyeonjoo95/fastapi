from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import FastAPI, Header, HTTPException
from typing import Optional, List
from app import models, schemas, crud
from app.database import SessionLocal, engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/search", response_model=List[schemas.Company])
def search_companies(
    query: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    회사 목록을 검색합니다.

    - **query**: 검색할 문자열 (예: 회사명)
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    companies = crud.search_companies(db, query, x_wanted_language)
    return crud.format_company_names(companies, x_wanted_language)


@app.post("/companies", response_model=schemas.CompanyDetail)
def create_company(
    company: schemas.CompanyCreate,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    새로운 회사를 생성합니다.

    - **company**: 생성할 회사의 상세 정보
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    company = crud.create_company(db, company)
    return crud.format_company_detail(company, x_wanted_language)


@app.get("/companies/{company_name}", response_model=schemas.CompanyDetail)
def search_company(
    company_name: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    특정 회사의 상세 정보를 조회합니다.

    - **company_name**: 검색할 회사 이름
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    company = crud.get_company_by_name(db, company_name, x_wanted_language)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    return crud.format_company_detail(company, x_wanted_language)


@app.get("/tags", response_model=List[schemas.Company])
def search_tag(
    query: str, x_wanted_language: str = Header(...), db: Session = Depends(get_db)
):
    """
    특정 태그를 가진 회사를 검색합니다.

    - **query**: 검색할 태그
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    companies = crud.search_companies_by_tag(db, query)
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found")

    return crud.format_company_names(companies, x_wanted_language)


@app.put("/companies/{company_name}/tags", response_model=schemas.CompanyDetail)
def update_company_tags(
    company_name: str,
    tags: List[schemas.TagBase],
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    특정 회사의 태그를 업데이트합니다.

    - **company_name**: 태그를 업데이트할 회사 이름
    - **tags**: 새로운 태그들
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    company = crud.update_company_tags(db, company_name, tags, x_wanted_language)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return crud.format_company_detail(company, x_wanted_language)


@app.delete(
    "/companies/{company_name}/tags/{tag}", response_model=schemas.CompanyDetail
)
def delete_company_tag(
    company_name: str,
    tag: str,
    x_wanted_language: str = Header(...),
    db: Session = Depends(get_db),
):
    """
    특정 회사에서 태그를 삭제합니다.

    - **company_name**: 태그를 삭제할 회사 이름
    - **tag**: 삭제할 태그
    - **x_wanted_language**: 요청 헤더에서 언어 정보를 가져옵니다 (필수)
    """
    company = crud.delete_company_tags(db, company_name, x_wanted_language, tag)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    return crud.format_company_detail(company, x_wanted_language)
