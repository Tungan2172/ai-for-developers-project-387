from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError

from app.api.schemas import ApiError


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:  # noqa: RUF029
        return JSONResponse(
            status_code=422,
            content=ApiError(code="validation_error", message=str(exc)).model_dump(),
        )

    @app.exception_handler(DataError)
    async def data_error_handler(request: Request, exc: DataError) -> JSONResponse:  # noqa: RUF029
        return JSONResponse(
            status_code=422,
            content=ApiError(
                code="validation_error", message=f"Database data error: {exc}"
            ).model_dump(),
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:  # noqa: RUF029
        return JSONResponse(
            status_code=409,
            content=ApiError(
                code="conflict", message=f"Database integrity error: {exc}"
            ).model_dump(),
        )


def api_error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=ApiError(code=code, message=message).model_dump(),
    )
