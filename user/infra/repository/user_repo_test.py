from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from user.domain.user import User as UserVO
from user.infra.db_models.user import User
from user.infra.repository.user_repo import UserRepository
from utils.db_utils import row_to_dict


@pytest.fixture
def mock_session_local(monkeypatch):
    mock_session = Mock()
    monkeypatch.setattr(
        "user.infra.repository.user_repo.SessionLocal", lambda: mock_session
    )
    return mock_session


def test_find_by_email_user_exists(mock_session_local):
    mock_user = User(id=1, email="test@example.com", name="Test User")
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    mock_session_local.__enter__ = lambda s: mock_db
    mock_session_local.__exit__ = lambda s, exc_type, exc_val, exc_tb: None

    user_repository = UserRepository()
    result = user_repository.find_by_email("test@example.com")

    assert result == UserVO(**row_to_dict(mock_user))


def test_find_by_email_user_not_exist(mock_session_local):
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None
    mock_session_local.__enter__ = lambda s: mock_db
    mock_session_local.__exit__ = lambda s, exc_type, exc_val, exc_tb: None

    user_repository = UserRepository()
    with pytest.raises(HTTPException) as exception:
        user_repository.find_by_email("test@example.com")

    assert exception.value.status_code == 422
