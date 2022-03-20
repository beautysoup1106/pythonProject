import time

import uvicorn
from fastapi import FastAPI
from starlette.background import BackgroundTasks

from routers.items import itemRoute
from routers.users import userRoute

app = FastAPI(
    docs_url="/openapi",
    redoc_url="/apidoc"
)

app.include_router(userRoute, prefix="/user", tags=["users"])
app.include_router(itemRoute, prefix="/items", tags=["items"])


def write_notification(email: str, message=""):
    time.sleep(200)
    with open("log.txt", mode="w") as email_file:
        content = f"name {email}: {message}"
        email_file.write(content)


@app.post("/sendtxt/")
async def sendtxt(email: str, backgroud_tasks: BackgroundTasks):
    backgroud_tasks.add_task(write_notification, email, message="不关注")
    return {"message": "在后台读写"}


if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1", port=8020)