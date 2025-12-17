def test_create_user_success(client, mock_email_service):
    """유저 생성 성공 테스트"""
    user_data = {
        "name": "테스트유저",
        "email": "test@example.com",
        "password": "testpassword123",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "created_at" in data
    assert "updated_at" in data
    # password는 응답에 포함되지 않아야 함
    assert "password" not in data

    # 이메일 서비스가 호출되었는지 확인
    mock_email_service.assert_called_once()


def test_create_user_duplicate_email(client, mock_email_service):
    """중복 이메일로 유저 생성 시도 테스트"""
    user_data = {
        "name": "테스트유저",
        "email": "duplicate@example.com",
        "password": "testpassword123",
    }

    # 첫 번째 유저 생성
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == 201

    # 동일한 이메일로 두 번째 유저 생성 시도
    response2 = client.post("/users", json=user_data)
    assert response2.status_code == 422
    response_data = response2.json()
    # detail이 문자열이거나 딕셔너리일 수 있음
    detail_str = str(response_data.get("detail", "")).lower()
    assert (
        "already exists" in detail_str or "already exists" in str(response_data).lower()
    )


def test_create_user_invalid_name_too_short(client, mock_email_service):
    """이름이 너무 짧은 경우 테스트"""
    user_data = {
        "name": "A",  # 최소 2자
        "email": "test@example.com",
        "password": "testpassword123",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400  # Validation error


def test_create_user_invalid_name_too_long(client, mock_email_service):
    """이름이 너무 긴 경우 테스트"""
    user_data = {
        "name": "A" * 33,  # 최대 32자
        "email": "test@example.com",
        "password": "testpassword123",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400  # Validation error


def test_create_user_invalid_password_too_short(client, mock_email_service):
    """비밀번호가 너무 짧은 경우 테스트"""
    user_data = {
        "name": "테스트유저",
        "email": "test@example.com",
        "password": "short",  # 최소 8자
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400  # Validation error


def test_create_user_invalid_email(client, mock_email_service):
    """잘못된 이메일 형식 테스트"""
    user_data = {
        "name": "테스트유저",
        "email": "invalid-email",  # 잘못된 이메일 형식
        "password": "testpassword123",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400  # Validation error


def test_create_user_missing_fields(client, mock_email_service):
    """필수 필드 누락 테스트"""
    user_data = {
        "name": "테스트유저",
        # email과 password 누락
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 400  # Validation error
