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
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm


from dotenv import load_dotenv

load_dotenv()
from users.queries import query
from users.schemas import user_sch


user_router = APIRouter()



@user_router.post("/login", summary="Create access and refresh tokens for user",tags=["User"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db),
):
    user = query.get_user(db, form_data.username)
    if user is None or user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password or user is inactive",
        )


    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }



@user_router.post("/refresh",response_model=user_sch.User, summary="Refresh access token",tags=["User"])
async def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    username = verify_refresh_token(refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token",
        )
    return {"access_token": create_access_token(username)}



@user_router.post("/register",response_model=user_sch.Users, summary="Register a new user",tags=["User"])
async def register(
    form_data: user_sch.UserCreate,
    db: Session = Depends(get_db)):
    #get_user = query.get_user_byphone(db, email=form_data.email,phone_number=form_data.phone)
    #if get_user:
    user = query.user_create(db=db, user=form_data)

    #current_user: user_sch.User = Depends(get_current_user)
    return user

@user_router.get("/me", response_model=user_sch.User, summary="Get current user",tags=["User"])
async def current_user(db:Session=Depends(get_db),current_user: user_sch.User = Depends(get_current_user)):
    
    return current_user


@user_router.put('/update',summary="Reset password",tags=["User"])
async def reset_password(
    form_data:user_sch.UserUpdate,

    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query.user_update(db=db, id=form_data.id, password=form_data.password, phone_number=form_data.phone_number, name=form_data.name, role_id=form_data.role_id, status=form_data.status)
    return {"message":"Updated successfully",'success':True}


@user_router.get('/users',summary="Get all users",tags=["User"],response_model=Page[user_sch.Users])
async def get_users(name: Optional[str]=None,
                    id: Optional[int]=None,
                    phone_number: Optional[str]=None,
                    status: Optional[int]=None,
                    role_id: Optional[int]=None,
                    db: Session = Depends(get_db),
                    current_user: user_sch.User = Depends(get_current_user)):
    users = query.get_users(db, name=name, id=id, phone_number=phone_number, status=status, role_id=role_id)
    return paginate(users)


@user_router.post('/roles',summary="Create a new role",tags=["User"],response_model=user_sch.RoleGet)
async def create_role(
    form_data:user_sch.RoleCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    
    return query.create_role(db=db, form_data=form_data)



@user_router.get('/roles',summary="Get all roles",tags=["User"],response_model=Page[user_sch.RoleGet])
async def get_roles(
    name:Optional[str]=None,
    status:Optional[int]=None,
    id:Optional[int]=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    roles = query.get_roles(db, name=name, status=status, id=id)
    return paginate(roles)


@user_router.put('/roles',summary="Update role",tags=["User"],response_model=user_sch.RoleGet)
async def update_role(
    form_data:user_sch.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    
    if form_data.permissions is not None:
        query.delete_permissions(db=db, role_id=form_data.id)
        for permission in form_data.permissions:
            query.create_permissions(db=db, role_id=form_data.id, action_id=permission)
    role_update = query.update_role(db=db, form_data=form_data)
    return role_update


@user_router.get('/permissions',summary="Get all permissions",tags=["User"],response_model=Page[user_sch.Pages])
async def get_permissions(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    permissions = query.get_pages(db)
    return paginate(permissions)












