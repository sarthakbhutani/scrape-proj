from fastapi import APIRouter
router = APIRouter()

from fastapi import Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from app.settings import ACCESS_TOKEN_EXPIRY_HOURS
from app.utils.user_db import db
from app.model.user_model import Token,User
from app.utils.auth import authenticate_user,create_access_token


@router.post("/token", response_model=Token)
async def __login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRY_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

