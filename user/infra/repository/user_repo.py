from datetime import datetime

from fastapi import HTTPException

from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserVO  # 클래스명
from user.infra.db_models.user import User  # 데이터베이스 모델
from utils.db_utils import row_to_dict


class UserRepository(IUserRepository):
    def save(self, user: UserVO) -> UserVO:
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            memo=user.memo,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        with SessionLocal() as db:
            try:
                db.add(new_user)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

        # find_by_id는 UserVO를 반환하므로 타입 일치
        saved_user: UserVO = self.find_by_id(user.id)

        return saved_user

    def find_by_email(self, email: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                raise HTTPException(status_code=422, detail="User not found")

            # 세션이 열려있는 동안 row_to_dict 호출
            return UserVO(**row_to_dict(user))

    def find_by_id(self, id: str) -> UserVO:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code=422, detail="User not found")

            # 세션이 열려있는 동안 row_to_dict 호출
            return UserVO(**row_to_dict(user))

    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[UserVO]]:
        with SessionLocal() as db:
            # 전체 개수 조회
            total_count = db.query(User).count()

            # 페이징된 사용자 목록 조회
            offset = (page - 1) * items_per_page
            users = db.query(User).offset(offset).limit(items_per_page).all()

            if not users:
                return (total_count, [])

            return (total_count, [UserVO(**row_to_dict(user)) for user in users])

    def update(self, user_vo: UserVO) -> UserVO:
        with SessionLocal() as db:
            user: User = db.query(User).filter(User.id == user_vo.id).first()

            if not user:
                raise HTTPException(status_code=422, detail="User not found")

            user.name = user_vo.name
            user.password = user_vo.password
            user.updated_at = datetime.now()

            db.add(user)
            db.commit()

            # 세션이 열려있는 동안 row_to_dict 호출 (DetachedInstanceError 방지)
            return UserVO(**row_to_dict(user))

    def delete(self, id: str) -> None:
        with SessionLocal() as db:
            user: User = db.query(User).filter(User.id == id).first()

            if not user:
                raise HTTPException(status_code=422, detail="User not found")

            db.delete(user)
            db.commit()
