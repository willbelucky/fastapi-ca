import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container, container, get_user_service
from user.application.user_service import UserService

app = FastAPI()
app.container = container

# 라우터 import (와이어링 대신 직접 dependency 함수 사용)
from user.interface.controllers.user_controller import router as user_router

app.include_router(user_router)




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=exc.errors(),
    )


@app.get("/")
def hello():
    return {"Hello": "FastAPI"}


@app.get("/debug/di-status")
def check_dependency_injection(
    user_service: UserService = Depends(get_user_service),
):
    """의존성 주입 상태를 확인하는 디버깅 엔드포인트"""
    from user.infra.repository.user_repo import UserRepository
    
    # 컨테이너 상태 확인
    container = app.container
    
    # 주입된 서비스 확인
    injected_service = user_service
    injected_repo = injected_service.user_repo if hasattr(injected_service, 'user_repo') else None
    
    result = {
        "container_configured": container is not None,
        "wiring_config_packages": container.wiring_config.packages if hasattr(container, 'wiring_config') else None,
        "service_type": type(injected_service).__name__,
        "service_is_user_service": isinstance(injected_service, UserService),
        "service_has_repo": hasattr(injected_service, 'user_repo'),
    }
    
    if injected_repo:
        result.update({
            "repo_type": type(injected_repo).__name__,
            "repo_is_user_repository": isinstance(injected_repo, UserRepository),
            "repo_injected": injected_repo is not None,
            "service_id": id(injected_service),
            "repo_id": id(injected_repo),
            "status": "✅ 의존성 주입이 정상적으로 작동하고 있습니다!"
        })
    else:
        result["status"] = "⚠️ UserService에 user_repo 속성이 없습니다"
    
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
