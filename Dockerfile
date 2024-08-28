# 베이스 이미지로 Python 3.12을 사용합니다.
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install --no-cache-dir poetry

# Poetry 버전 확인 (디버깅용)
RUN poetry --version

# Poetry 설정
ENV POETRY_VERSION=1.8.0
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR="/var/cache/pypoetry"

# Poetry와 의존성 설치
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-dev --no-interaction --no-ansi

# 애플리케이션 소스 코드를 복사합니다.
COPY . .

# PYTHONPATH 환경 변수 설정
ENV PYTHONPATH=/app

# FastAPI 애플리케이션을 실행하는 명령어를 설정합니다.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]