import time

from fastapi import FastAPI, Request

from common.auth import CurrentUser, decode_access_token
from common.logger import logger
from context_vars import user_context


def create_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response

    @app.middleware("http")
    def get_current_user_middleware(request: Request, call_next):
        authorization = request.headers.get("Authorization")
        if authorization:
            splits = authorization.split(" ")
            if splits[0] == "Bearer":
                token = splits[1]
                payload = decode_access_token(token)
                user_id = payload.get("user_id")
                user_role = payload.get("role")

                user_context.set(CurrentUser(user_id, user_role))

        logger.info(request.url)

        response = call_next(request)

        return response
