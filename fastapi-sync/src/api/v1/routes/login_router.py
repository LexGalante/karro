from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.dependency_injection import get_dbcontext
from api.v1.schemas.auth_schema import AuthRequestSchema, AuthResponseSchema
from resources.dbcontext import DbContext
from services.auth_service import AuthService


router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=AuthResponseSchema)
def index(
    schema: AuthRequestSchema,
    dbcontext: DbContext = Depends(get_dbcontext)
):
    try:
        token: str = AuthService(dbcontext).authenticate(schema.username, schema.password)

        return AuthResponseSchema(token_type="Bearer", access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
