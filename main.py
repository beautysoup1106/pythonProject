import time

import uvicorn
from fastapi import FastAPI
from starlette.background import BackgroundTasks
from starlette.responses import Response

from routers.items import itemRoute
from routers.users import userRoute

app = FastAPI(
    docs_url="/openapi",
    redoc_url="/apidoc"
)

app.include_router(userRoute, prefix="/user", tags=["users"])
app.include_router(itemRoute, prefix="/items", tags=["items"])



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8020)
