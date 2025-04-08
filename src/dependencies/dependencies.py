from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.auth_service import AuthService
from core.config import config
# from core.sync_database import create_session
from core.database import create_async_session
from users.users_schema import UsersSchema


get_current_user_dependency = Annotated[
    UsersSchema, Depends(AuthService.get_current_user)
]
# create_session_dependency = Annotated[Session, Depends(create_session)]
create_async_session_dependency = Annotated[Session, Depends(create_async_session)]
get_auth_form_dependency = Annotated[OAuth2PasswordRequestForm, Depends()]
get_token_dependency = Annotated[str, Depends(config.oauth2_scheme)]
