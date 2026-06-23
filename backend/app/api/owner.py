from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from app.api.dependencies import get_owner_repository
from app.api.errors import api_error_response
from app.api.schemas import OwnerOut
from app.domain.interfaces import OwnerRepository

router = APIRouter(prefix="/owner", tags=["Owner"])


@router.get("")
def get_owner(
    repo: OwnerRepository = Depends(get_owner_repository),
) -> Response:
    owner = repo.get()
    if owner is None:
        return api_error_response(404, "owner_not_found", "Owner profile not found")
    return JSONResponse(content=OwnerOut.model_validate(owner).model_dump(by_alias=True))
