from sqlalchemy.orm import Session, selectinload
from app import models, schemas
from typing import List
from sqlalchemy import text


def search_companies(db: Session, query: str, language: str) -> List[models.Company]:
    companies = (
        db.query(models.Company)
        .join(models.Company.names)
        .options(selectinload(models.Company.names))
        .filter(
            models.CompanyName.company_name.like(f"%{query}%"),
            models.CompanyName.language == language,
        )
        .all()
    )

    return companies


def create_company(db: Session, companyCreate: schemas.CompanyCreate) -> models.Company:
    # 1. Company 인스턴스 생성
    company = models.Company()

    # 2. CompanyName 인스턴스 생성
    for lang, name in companyCreate.company_name.items():
        company_name = models.CompanyName(language=lang, company_name=name)
        company.names.append(company_name)

    # 3. 태그를 문자열로 결합
    tag_dict = {}
    for tag_data in companyCreate.tags:
        for lang, tag in tag_data.tag_name.items():
            if lang not in tag_dict:
                tag_dict[lang] = []
            tag_dict[lang].append(tag)

    # 4. CompanyTag 인스턴스 생성 및 추가
    for lang, tags in tag_dict.items():
        combined_tags = "|".join(tags)
        company_tag = models.CompanyTag(language=lang, company_tag=combined_tags)
        company.tags.append(company_tag)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company


def get_company_by_name(
    db: Session, company_name: str, language: str
) -> models.Company:
    company = (
        db.query(models.Company)
        .join(models.Company.names)
        .join(models.Company.tags)
        .options(selectinload(models.Company.names))
        .options(selectinload(models.Company.tags))
        .filter(
            models.CompanyName.company_name == company_name,
        )
        .first()
    )

    return company


def format_company_detail(
    company: models.Company, language: str
) -> schemas.CompanyDetail:
    company_name = ""
    tags = []

    for item in company.names:
        if item.language == language:
            company_name = item.company_name
            break

    for tag in company.tags:
        if tag.language == language:
            tags = tag.company_tag.split("|")
            break

    return schemas.CompanyDetail(company_name=company_name, tags=tags)


def format_company_names(
    companies: List[models.Company], language: str
) -> List[schemas.Company]:
    formatted_companies = []

    for company in companies:
        company_name = None

        for item in company.names:
            if item.language == language:
                company_name = item.company_name
                break

        # 만약 지정된 언어에 맞는 이름이 없다면, 첫 번째 이름을 기본값으로 사용
        if company_name is None and company.names:
            company_name = company.names[0].company_name

        formatted_companies.append({"company_name": company_name})

    return formatted_companies


def search_companies_by_tag(db: Session, tag: str) -> models.Company:

    query = text(
        """
        SELECT DISTINCT c.id
        FROM company c
        JOIN company_tag ct ON c.id = ct.company_id
        WHERE FIND_IN_SET(:tag, REPLACE(ct.company_tag, '|', ',')) > 0
    """
    )

    result = db.execute(query, {"tag": tag}).scalars().all()

    company = (
        db.query(models.Company)
        .join(models.Company.names)
        .options(selectinload(models.Company.names))
        .filter(models.Company.id.in_(result))
        .all()
    )

    return company


def update_company_tags(
    db: Session,
    company_name: str,
    new_tags: schemas.CompanyUpdateTags,
    language: str,
) -> models.Company:
    company = (
        db.query(models.Company)
        .join(models.Company.names)
        .options(selectinload(models.Company.names))
        .filter(
            models.CompanyName.company_name == company_name,
        )
        .first()
    )

    if not company:
        return None

    # 새로운 태그들을 추가
    tag_dict = {}
    for tag_data in new_tags:
        for lang, tag in tag_data.tag_name.items():
            if lang not in tag_dict:
                tag_dict[lang] = []
            tag_dict[lang].append(tag)

    # CompanyTag 업데이트
    for lang, tags in tag_dict.items():
        combined_tags = "|".join(tags)
        # 기존 태그를 찾거나 새로 추가
        company_tag = (
            db.query(models.CompanyTag)
            .filter(
                models.CompanyTag.company_id == company.id,
                models.CompanyTag.language == lang,
            )
            .first()
        )
        if company_tag:
            company_tag.company_tag += f"|{combined_tags}"
        else:
            new_tag = models.CompanyTag(language=lang, company_tag=combined_tags)
            company.tags.append(new_tag)

    db.commit()

    return company


def delete_company_tags(
    db: Session, company_name: str, language: str, tag: str
) -> models.Company:
    company = (
        db.query(models.Company)
        .join(models.Company.names)
        .join(models.Company.tags)
        .filter(
            models.CompanyName.company_name == company_name,
        )
        .first()
    )

    if not company:
        return None

    for company_tag in company.tags:
        if company_tag.language == language:
            tags = company_tag.company_tag.split("|")
            if tag in tags:
                tags.remove(tag)
                company_tag.company_tag = "|".join(tags)

    db.commit()
    db.refresh(company)

    return company
