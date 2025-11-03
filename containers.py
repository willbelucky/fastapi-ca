from dependency_injector import containers, providers

from user.infra.repository.user_repo import UserRepository
from user.application.user_service import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["user"],
    )

    user_repo = providers.Factory(UserRepository)
    user_service = providers.Factory(UserService, user_repo=user_repo)


# 전역 컨테이너 인스턴스 생성
container = Container()


# FastAPI Depends를 위한 의존성 함수들
def get_user_service() -> UserService:
    """UserService를 컨테이너에서 직접 가져오는 함수"""
    return container.user_service()