from datetime import datetime

import pytest
from freezegun import freeze_time
from ulid import ULID

from user.application.email_service import EmailService
from user.application.send_welcome_email_task import SendWelcomeEmailTask
from user.application.user_service import UserService
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User
from utils.crypto import Crypto


@pytest.fixture
def user_service_dependencies(mocker):
    user_repo_mock = mocker.Mock(spec=IUserRepository)
    email_service_mock = mocker.Mock(spec=EmailService)
    ulid_mock = mocker.Mock(spec=ULID)
    crypto_mock = mocker.Mock(spec=Crypto)
    send_welcome_email_task_mock = mocker.Mock(spec=SendWelcomeEmailTask)

    return (
        user_repo_mock,
        email_service_mock,
        ulid_mock,
        crypto_mock,
        send_welcome_email_task_mock,
    )


@freeze_time("2024-01-19")
def test_create_user_success(user_service_dependencies):
    (
        user_repo_mock,
        email_service_mock,
        ulid_mock,
        crypto_mock,
        send_welcome_email_task_mock,
    ) = user_service_dependencies

    user_service = UserService(
        user_repo=user_repo_mock,
        email_service=email_service_mock,
        ulid=ulid_mock,
        crypto=crypto_mock,
        send_welcome_email_task=send_welcome_email_task_mock,
    )

    id = "TEST_ID"
    name = "Dexter Han"
    email = "dexter.han@gmail.com"
    password = "password"
    memo = "Some memo"
    now = datetime.now()

    ulid_mock.generate.return_value = id
    user_repo_mock.find_by_email.return_value = None
    user_repo_mock.save.return_value = None
    crypto_mock.encrypt.return_value = password
    send_welcome_email_task_mock.delay.return_value = None
    send_welcome_email_task_mock.run.return_value = None

    user = user_service.create_user(
        name=name,
        email=email,
        password=password,
        memo=memo,
    )

    assert isinstance(user, User)
    assert user.id == id
    assert user.name == name
    assert user.email == email
    assert user.password == password
    assert user.memo == memo
    assert user.created_at == now
    assert user.updated_at == now

    user_repo_mock.find_by_email.assert_called_once_with(email)
    user_repo_mock.save.assert_called_once_with(user)
    crypto_mock.encrypt.assert_called_once_with(password)
    send_welcome_email_task_mock.delay.assert_called_once_with(email)
