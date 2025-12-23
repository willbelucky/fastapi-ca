# fastapi-ca

```bash
poetry install
Invoke-Expression (poetry env activate)
poetry add fastapi[all]
poetry add "uvicorn[standard]" # ASGI(Asynchronous server gateway interface) 서버
poetry add colorama # 윈도우 사용자의 경우 로그 색상을 표시
poetry add python-dotenv # --env-file 옵션을 사용
poetry add pyyaml # --log-config에 .yaml 파일을 제공
poetry add py-ulid # ULID를 생성해주는 py-ulid 패키지를 사용
poetry add "passlib[bcrypt]" # PassLib 패키지와 Bcrypt 암호화 알고리즘을 사용
poetry add sqlalchemy # 객체 관계 매핑 패키지
poetry add alembic # SQLAlchemy와 함께 사용되는 데이터베이스 마이그레이션 도구
poetry add mysqlclient # MySQL과의 연결을 위해 필요
poetry add dependency-injector # 의존성 주입에 사용
poetry add --group dev mypy # mypy 사용
poetry add "pydantic[email]" # pydantic 이메일 타입 추가
poetry add "python-jose[cryptography]" python-multipart # JWT를 다루는 라이브러리와 form-data를 다루기 위한 python-multipart 라이브러리
poetry add celery # 비동기 작업을 처리하고 관리하는 celery 설치
poetry add pytest-mock freezegun # 테스트 코드에서 사용할 pytest-mock 패키지와 시간 객체를 다룰 때 항상 일정한 시각의 객체를 얻을 수 있는 freezegun 패키지 다운로드드

poetry run alembic init migrations # Alembic의 초기화를 수행
poetry run alembic revision --autogenerate -m "add User Table" # 자동으로 리비전 파일을 생성(User 테이블 생성)
poetry run alembic revision --autogenerate -m "user - add memo" # 자동으로 리비전 파일을 생성(User 테이블에 memo 열 추가)
poetry run alembic upgrade head # 가장 최신의 리비전파일까지 수행

docker run -d --name mysql-local -p 3306:3306/tcp -e MYSQL_ROOT_PASSWORD=test mysql:8 # MySQL docker 백그라운드 실행
docker run -d --hostname my-rabbit --name my-rabbit -e RABBITMQ_DEFAULT_USER=root -e RABBITMQ_DEFAULT_PASS=test -p 5672:5672 -p 15672:15672 rabbitmq:3-management # RabbitMQ docker 백그라운드 실행

# Windows에서는 solo 풀 사용 (prefork는 Windows에서 작동하지 않음)
celery -A common.messaging.celery worker -n worker1 --loglevel=info --pool=solo # Windows용
# Linux/Mac에서는 prefork 풀 사용 (기본값)
# celery -A common.messaging.celery worker -n worker1 --loglevel=info # Linux/Mac용

poetry run uvicorn main:app --reload --port 8080 # 유비콘으로 서버를 구동(포트는 8080 사용)
```