import logging

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import EmailStr

from model.schema import UserCreate, UserResponse, UserUpdate
from service.database import SessionLocal, get_db
from service.user_service import UserService

# TODO: Implement uvicorn logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)15s][%(funcName)10s][%(lineno)4s][%(levelname)7s]: %(message)s",
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/user", response_model=UserResponse)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db=db, user=user)


@app.get("/user/{email}", response_model=UserResponse)
def get_user(email: EmailStr, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    return existing_user


@app.delete("/user/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(email: EmailStr, db: SessionLocal = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    existing_user = UserService.delete_user(db=db, user=existing_user)


@app.put("/user/{email}", response_model=UserResponse)
def update_user(
    email: EmailStr, updated_fields: UserUpdate, db: SessionLocal = Depends(get_db)
):
    existing_user = UserService.get_user_by_email(db=db, email=email)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User not found for email: {email}"
        )
    return UserService.update_user(
        db=db, updated_fields=updated_fields, existing_user=existing_user
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
