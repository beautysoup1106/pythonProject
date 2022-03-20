import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from routers.items import itemRoute
from routers.users import userRoute

# tags_metadata = [
#     {
#         "name": "系统接口",
#         "description": "用户创建和items创建"
#     },
#     {
#         "name": "items",
#         "description": "管理items，你可以查看文档",
#         "externalDocs": {
#             "description": "使用文档",
#             "url": "http://localhost:8000/docs#/Items",
#         },
#     },
# ]
# """
#
# 用户创建和items创建
#
# ## Items
#
# 你可以读他们
#
# ## Users
#
# 你可以做下面的：
#
# * **创建用户**
# * **读取用户**
# """
# app = FastAPI(
#     openapi_tags=tags_metadata,
#     docs_url="/openapi",
#     redoc_url="/apidoc"
# )
#
# app.include_router(userRoute, prefix='/user', tags=["users"])
#
# app.include_router(itemRoute, prefix="/items", tags=["items"])

app = FastAPI()

templates = Jinja2Templates(directory="./templates")

app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "hello.html",
        {
            "request": request
        }
    )

if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1", port=8080)