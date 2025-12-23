from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base
from database_models import *  # noqa: F403, F401 - 모든 모델 import
from main import app


@pytest.fixture(scope="function")
def test_db():
    """테스트용 데이터베이스 엔진 및 세션 생성"""
    # 메모리 SQLite 데이터베이스 사용 (테스트용)
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # 모든 테이블 삭제 후 재생성 (깨끗한 상태로 시작)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield TestingSessionLocal

    # 테스트 후 정리
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def client(test_db, monkeypatch):
    """테스트용 FastAPI 클라이언트 생성"""
    # SessionLocal을 테스트용 세션으로 교체
    import database

    # UserRepository가 import되기 전에 SessionLocal을 교체해야 함
    monkeypatch.setattr(database, "SessionLocal", test_db)

    # UserRepository 모듈도 다시 import하여 새로운 SessionLocal을 사용하도록 함
    import importlib

    import user.infra.repository.user_repo

    importlib.reload(user.infra.repository.user_repo)

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_send_welcome_email_task():
    """Celery 이메일 태스크 모킹"""
    # user_service에서 SendWelcomeEmailTask().run()을 호출하므로 해당 경로를 모킹
    with patch("user.application.user_service.SendWelcomeEmailTask") as mock_task_class:
        mock_instance = mock_task_class.return_value
        mock_run = mock_instance.run
        yield mock_run


@pytest.fixture(autouse=True)
def cleanup_db(test_db):
    """각 테스트 전에 데이터베이스 정리"""
    from user.infra.db_models.user import User

    # 테스트 전에 모든 데이터 삭제
    session = test_db()
    try:
        session.query(User).delete()
        session.commit()
    finally:
        session.close()
    yield
    # 테스트 후에도 정리
    session = test_db()
    try:
        session.query(User).delete()
        session.commit()
    finally:
        session.close()
