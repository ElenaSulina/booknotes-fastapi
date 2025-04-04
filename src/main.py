import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from fastapi import FastAPI

import uvicorn

from core.config import config
from core.router import router

app = FastAPI(title=config.APP_NAME)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
