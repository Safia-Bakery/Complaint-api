
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi_pagination import paginate, Page
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
)

from users.queries import query

from users.schemas import user_sch
from users.queries import v2roles
from users.schemas.v2role import GetHastStamRoles,GetStampUsers







roles_router = APIRouter()


@roles_router.get("/roles/has_stamp", summary="Get all roles",response_model=list[GetHastStamRoles])
async def get_roles(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get all roles
    """
    return v2roles.get_has_stamp(db=db)


@roles_router.get("/users/has_stamp/{id}", summary="Get role by id",response_model=list[GetStampUsers])
async def get_users(
    role_id:int,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),
):
    """
    Get role by id
    """
    return v2roles.get_users(db=db,role_id=role_id)










