import logging

import uvicorn
from fastapi import FastAPI

from api.auth_router import router as auth_router
from api.user_router import router as user_router

# TODO: Implement uvicorn logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)15s][%(funcName)10s][%(lineno)4s][%(levelname)7s]: %(message)s",
)

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
