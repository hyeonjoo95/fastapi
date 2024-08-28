# FastAPI 프로젝트

이 프로젝트는 FastAPI를 사용하여 구축된 웹 애플리케이션입니다.

## 디렉토리 및 파일 설명

### `app/`
애플리케이션의 주요 코드가 위치하는 디렉토리입니다.

- **`__init__.py`**: `app` 패키지를 초기화합니다.
- **`main.py`**: FastAPI 애플리케이션의 진입점입니다. FastAPI 인스턴스를 생성하고 라우터를 포함합니다.
- **`models.py`**: 데이터베이스 테이블 구조를 정의합니다.
- **`schemas.py`**: 데이터 검증 및 직렬화/역직렬화 작업을 위한 데이터 모델을 정의합니다.
- **`crud.py`**: 데이터베이스에서 데이터를 생성, 읽기, 업데이트 및 삭제하는 함수들이 포함됩니다.
- **`database.py`**: 데이터베이스 연결 및 세션 관리를 설정합니다.

### `test/`
애플리케이션의 테스트 코드가 위치하는 디렉토리입니다.

### `Dockerfile`
애플리케이션을 Docker 컨테이너로 빌드하기 위한 설정 파일입니다.

### `docker-compose.yml`
Docker 컨테이너를 정의하고 실행하기 위한 설정 파일입니다.

### `pyproject.toml`
Poetry를 사용하여 Python 프로젝트의 의존성 및 설정을 정의하는 파일입니다.

### `poetry.lock`
Poetry가 의존성 버전을 고정하기 위해 사용하는 파일입니다.

## 설치 및 실행 방법

### Docker를 사용한 설치

1. **Docker 및 Docker Compose가 설치되어 있어야 합니다.**

2. **Docker Compose로 컨테이너 빌드 및 실행**

   ```bash
   docker-compose up --build
