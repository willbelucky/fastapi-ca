from database import SessionLocal
from user.domain.repository.user_repo import IUserRepository
from user.domain.user import User as UserV0 # 클래스명
from user.infra.db_models.user import User # 데이터베이스 모델

class UserRepository(IUserRepository):
    def save(self, user: UserV0):
        new_user = User(
            id=user.id,
            email=user.email,
            name=user.name,
            password=user.password,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        with SessionLocal() as db:
            try: # try-finally 구문을 사용해 세션이 자동으로 닫히도록 함
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()

    def find_by_email(self, email: str) -> User:
        pass